"""FAISS retrieval engine with explainability for recipe search."""

from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np

from pantry.embedder import GloVeEmbedder


class RecipeRetriever:
    """Retrieve recipes from a FAISS index using ingredient and mood vectors.

    Design note: constraints (time, effort) are echoed in the explanation but
    do NOT hard-filter results, because the Epicurious dataset lacks structured
    time/effort fields.
    """

    INGREDIENT_WEIGHT = 0.7
    MOOD_WEIGHT = 0.3
    INGREDIENT_OVERLAP_BOOST = 0.15  # Per matched ingredient, added to FAISS score

    def __init__(self, index_path: str, recipes_path: str) -> None:
        self._index = faiss.read_index(str(Path(index_path)))
        with open(recipes_path, encoding="utf-8") as fh:
            self._recipes: list[dict] = json.load(fh)
        self._embedder = GloVeEmbedder()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def search(
        self,
        ingredient_tokens: list[str],
        mood_vector: np.ndarray | None,
        constraints: dict,
        top_k: int = 100,
    ) -> list[dict]:
        """Search for recipes matching ingredients, mood, and constraints.

        Parameters
        ----------
        ingredient_tokens:
            List of ingredient words (e.g. ["chicken", "garlic"]).
        mood_vector:
            A unit-length 100-d numpy vector, or None.
        constraints:
            Dict of user constraints (e.g. {"time": "quick"}).  Noted in
            the explanation but not used for hard filtering.
        top_k:
            Maximum number of results to return.

        Returns
        -------
        list[dict]
            Each dict has keys: id, title, ingredients, instructions,
            image_name, score, explanation.
        """
        query_vector = self._build_query_vector(ingredient_tokens, mood_vector)
        if query_vector is None:
            return []

        # Normalize to unit length (index uses IndexFlatIP on normalized vecs)
        norm = np.linalg.norm(query_vector)
        if norm > 0:
            query_vector = query_vector / norm

        # Over-fetch then trim
        over_fetch = top_k * 3
        query_matrix = query_vector.reshape(1, -1).astype(np.float32)
        scores, indices = self._index.search(query_matrix, over_fetch)

        candidates: list[dict] = []
        for rank in range(over_fetch):
            idx = int(indices[0][rank])
            if idx < 0:
                continue  # FAISS returns -1 for missing entries
            recipe = self._recipes[idx]
            explanation = self._build_explanation(
                recipe, ingredient_tokens, mood_vector, constraints
            )
            # Skip recipes that don't contain all queried ingredients
            overlap_count = len(explanation["matched_ingredients"])
            if ingredient_tokens and overlap_count < len(ingredient_tokens):
                continue
            # Re-rank: boost score for recipes that contain queried ingredients
            base_score = float(scores[0][rank])
            boosted_score = base_score + overlap_count * self.INGREDIENT_OVERLAP_BOOST
            candidates.append(
                {
                    "id": recipe["id"],
                    "title": recipe["title"],
                    "ingredients": recipe["ingredients"],
                    "instructions": recipe["instructions"],
                    "image_name": recipe.get("image_name"),
                    "score": boosted_score,
                    "explanation": explanation,
                }
            )

        # Sort by boosted score and return top_k
        candidates.sort(key=lambda r: r["score"], reverse=True)
        return candidates[:top_k]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _build_query_vector(
        self,
        ingredient_tokens: list[str],
        mood_vector: np.ndarray | None,
    ) -> np.ndarray | None:
        """Weighted-average ingredient and mood vectors into a query vector."""
        has_ingredients = bool(ingredient_tokens)
        has_mood = mood_vector is not None

        if not has_ingredients and not has_mood:
            return None

        ingredient_vec = None
        if has_ingredients:
            text = " ".join(ingredient_tokens)
            ingredient_vec = self._embedder.embed_text(text)

        # Re-check: embedding might fail if no tokens have GloVe vectors
        has_ingredients = ingredient_vec is not None
        has_mood = mood_vector is not None

        if not has_ingredients and not has_mood:
            return None

        if has_ingredients and has_mood:
            return (
                self.INGREDIENT_WEIGHT * ingredient_vec
                + self.MOOD_WEIGHT * mood_vector
            )
        if has_ingredients:
            return ingredient_vec
        return mood_vector

    @staticmethod
    def _build_explanation(
        recipe: dict,
        ingredient_tokens: list[str],
        mood_vector: np.ndarray | None,
        constraints: dict,
    ) -> dict:
        """Build an explanation dict for a single result."""
        # Check which query ingredients appear in the recipe's ingredient list
        recipe_ingredients_lower = " ".join(
            ing.lower() for ing in recipe.get("ingredients", [])
        )
        matched = [
            tok for tok in ingredient_tokens if tok.lower() in recipe_ingredients_lower
        ]

        return {
            "matched_ingredients": matched,
            "mood_match": mood_vector is not None,
            "constraints_met": constraints,
        }
