"""Pipeline orchestrator that ties all NLP stages together for recipe search."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pantry.ingredient_extractor import IngredientExtractor
from pantry.constraint_extractor import ConstraintExtractor
from pantry.mood_embedder import MoodEmbedder
from pantry.retrieval import RecipeRetriever


class PantryPipeline:
    """Orchestrates ingredient extraction, constraint extraction, mood
    embedding, and FAISS retrieval into a single end-to-end search pipeline.

    Three stage methods mirror the API endpoints:
      1. parse   - extract ingredients, constraints, and mood from text
      2. embed   - build a weighted query vector from parsed signals
      3. recommend - run FAISS retrieval with the query vector

    The convenience method ``search`` chains all three stages.
    """

    def __init__(
        self,
        vocab_path: str = "data/processed/ingredient_vocab.json",
        index_path: str = "data/processed/recipes.index",
        recipes_path: str = "data/processed/recipes.json",
    ) -> None:
        self._ingredient_extractor = IngredientExtractor(vocab_path)
        self._constraint_extractor = ConstraintExtractor()
        self._mood_embedder = MoodEmbedder()
        self._retriever = RecipeRetriever(index_path, recipes_path)

    # ------------------------------------------------------------------
    # Stage 1: Parse
    # ------------------------------------------------------------------

    def parse(self, text: str) -> dict:
        """Run all three extractors on *text*.

        Returns
        -------
        dict
            ``ingredients``  - list[str]
            ``constraints``  - {"time": str|None, "effort": str|None}
            ``mood_tokens``  - list[str]
            ``_mood_vector`` - ndarray|None  (internal, not sent to frontend)
        """
        ingredients = self._ingredient_extractor.extract(text)
        constraints = self._constraint_extractor.extract(text)
        mood_result = self._mood_embedder.embed(text)

        return {
            "ingredients": ingredients,
            "constraints": constraints,
            "mood_tokens": mood_result["mood_tokens"],
            "_mood_vector": mood_result["vector"],
        }

    # ------------------------------------------------------------------
    # Stage 2: Embed
    # ------------------------------------------------------------------

    def embed(self, parsed: dict) -> dict:
        """Build a weighted query vector from the parsed signals.

        Parameters
        ----------
        parsed:
            Output of :meth:`parse`.

        Returns
        -------
        dict
            ``query_vector``     - list[float]|None  (JSON-safe)
            ``weights``          - dict describing active signals and weights
            ``_query_vector_np`` - ndarray  (internal, for FAISS search)
            ``_constraints``     - dict  (passed through for retrieval)
        """
        ingredient_tokens = parsed["ingredients"]
        mood_vector = parsed["_mood_vector"]

        has_ingredients = bool(ingredient_tokens)
        has_mood = mood_vector is not None

        # Build the query vector using the retriever's internal logic
        query_vector_np = self._retriever._build_query_vector(
            ingredient_tokens, mood_vector
        )

        # Determine active weights for transparency
        weights: dict = {}
        if has_ingredients and has_mood:
            weights = {
                "ingredients": {
                    "active": True,
                    "weight": RecipeRetriever.INGREDIENT_WEIGHT,
                    "tokens": ingredient_tokens,
                },
                "mood": {
                    "active": True,
                    "weight": RecipeRetriever.MOOD_WEIGHT,
                },
            }
        elif has_ingredients:
            weights = {
                "ingredients": {
                    "active": True,
                    "weight": 1.0,
                    "tokens": ingredient_tokens,
                },
                "mood": {"active": False, "weight": 0.0},
            }
        elif has_mood:
            weights = {
                "ingredients": {"active": False, "weight": 0.0},
                "mood": {"active": True, "weight": 1.0},
            }
        else:
            weights = {
                "ingredients": {"active": False, "weight": 0.0},
                "mood": {"active": False, "weight": 0.0},
            }

        query_vector_list = (
            query_vector_np.tolist() if query_vector_np is not None else None
        )

        return {
            "query_vector": query_vector_list,
            "weights": weights,
            "_query_vector_np": query_vector_np,
            "_constraints": parsed["constraints"],
        }

    # ------------------------------------------------------------------
    # Stage 3: Recommend
    # ------------------------------------------------------------------

    def recommend(self, embedded: dict, top_k: int = 10) -> dict:
        """Run FAISS retrieval using the embedded query vector.

        Parameters
        ----------
        embedded:
            Output of :meth:`embed`.
        top_k:
            Maximum number of results to return.

        Returns
        -------
        dict
            ``results`` - list[dict] with id, title, score, explanation, etc.
        """
        query_vector = embedded["_query_vector_np"]
        if query_vector is None:
            return {"results": []}

        # Normalize before search (matching retriever logic)
        norm = np.linalg.norm(query_vector)
        if norm > 0:
            query_vector = query_vector / norm

        constraints = embedded["_constraints"]

        # Use the retriever's internal embedding to infer ingredient tokens
        # from the weights info so we can pass them for explanations
        weights = embedded["weights"]
        ingredient_tokens = (
            weights["ingredients"].get("tokens", [])
            if weights["ingredients"]["active"]
            else []
        )

        # Build query matrix for FAISS
        query_matrix = query_vector.reshape(1, -1).astype(np.float32)
        over_fetch = top_k * 3
        scores, indices = self._retriever._index.search(query_matrix, over_fetch)

        candidates: list[dict] = []
        for rank in range(over_fetch):
            idx = int(indices[0][rank])
            if idx < 0:
                continue
            recipe = self._retriever._recipes[idx]
            explanation = RecipeRetriever._build_explanation(
                recipe, ingredient_tokens, embedded["_query_vector_np"], constraints
            )
            # Re-rank: boost recipes that contain queried ingredients
            base_score = float(scores[0][rank])
            overlap_count = len(explanation["matched_ingredients"])
            boosted_score = base_score + overlap_count * RecipeRetriever.INGREDIENT_OVERLAP_BOOST
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
        return {"results": candidates[:top_k]}

    # ------------------------------------------------------------------
    # Convenience: end-to-end search
    # ------------------------------------------------------------------

    def search(self, text: str, top_k: int = 10) -> dict:
        """Chain parse -> embed -> recommend end-to-end.

        Returns
        -------
        dict
            ``parsed``  - {ingredients, constraints, mood_tokens}
            ``weights`` - signal weight info
            ``results`` - list of recipe dicts
        """
        parsed = self.parse(text)
        embedded = self.embed(parsed)
        recommended = self.recommend(embedded, top_k=top_k)

        return {
            "parsed": {
                "ingredients": parsed["ingredients"],
                "constraints": parsed["constraints"],
                "mood_tokens": parsed["mood_tokens"],
            },
            "weights": embedded["weights"],
            "results": recommended["results"],
        }
