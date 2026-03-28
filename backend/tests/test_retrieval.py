"""Tests for the FAISS retrieval engine."""

import numpy as np
import pytest

from pantry.retrieval import RecipeRetriever

INDEX_PATH = "data/processed/recipes.index"
RECIPES_PATH = "data/processed/recipes.json"


@pytest.fixture(scope="module")
def retriever():
    return RecipeRetriever(INDEX_PATH, RECIPES_PATH)


def test_search_returns_results_for_ingredient_query(retriever):
    """Ingredient-only query should return a non-empty list."""
    # Simulate ingredient tokens and no mood
    ingredient_tokens = ["chicken", "garlic", "lemon"]
    results = retriever.search(
        ingredient_tokens=ingredient_tokens,
        mood_vector=None,
        constraints={},
        top_k=5,
    )
    assert isinstance(results, list)
    assert len(results) > 0


def test_results_have_explanation_with_expected_keys(retriever):
    """Each result should carry an explanation dict with required keys."""
    results = retriever.search(
        ingredient_tokens=["pasta", "tomato"],
        mood_vector=None,
        constraints={"time": "quick"},
        top_k=3,
    )
    assert len(results) > 0
    explanation = results[0]["explanation"]
    assert "matched_ingredients" in explanation
    assert "mood_match" in explanation
    assert "constraints_met" in explanation


def test_results_capped_at_top_k(retriever):
    """Number of results should not exceed top_k."""
    top_k = 4
    results = retriever.search(
        ingredient_tokens=["rice", "soy"],
        mood_vector=None,
        constraints={},
        top_k=top_k,
    )
    assert len(results) <= top_k


def test_empty_query_returns_empty_list(retriever):
    """No ingredients and no mood vector should return an empty list."""
    results = retriever.search(
        ingredient_tokens=[],
        mood_vector=None,
        constraints={},
        top_k=10,
    )
    assert results == []


def test_results_have_score_field(retriever):
    """Every result dict should include a numeric score."""
    results = retriever.search(
        ingredient_tokens=["butter", "sugar", "flour"],
        mood_vector=None,
        constraints={},
        top_k=5,
    )
    assert len(results) > 0
    for r in results:
        assert "score" in r
        assert isinstance(r["score"], float)
