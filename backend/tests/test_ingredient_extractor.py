"""Tests for the IngredientExtractor module."""

import pytest

from pantry.ingredient_extractor import IngredientExtractor


@pytest.fixture(scope="module")
def extractor():
    """Create a shared extractor instance (vocab loading is expensive)."""
    return IngredientExtractor()


class TestExtractKnownIngredients:
    """Extracts known ingredients from natural text."""

    def test_single_ingredient(self, extractor):
        result = extractor.extract("I need some garlic for the recipe")
        assert "garlic" in result

    def test_multiple_ingredients(self, extractor):
        result = extractor.extract("I have chicken, garlic, and salt in my pantry")
        assert "chicken" in result
        assert "garlic" in result
        assert "salt" in result

    def test_sentence_with_several_ingredients(self, extractor):
        result = extractor.extract(
            "Tonight I'm making pasta with butter, basil, and lemon"
        )
        assert "butter" in result
        assert "basil" in result
        assert "lemon" in result


class TestNoIngredients:
    """Returns empty list when no ingredients are found."""

    def test_empty_string(self, extractor):
        assert extractor.extract("") == []

    def test_no_ingredients_in_text(self, extractor):
        result = extractor.extract("The weather is nice today, let's go for a walk")
        assert result == []

    def test_whitespace_only(self, extractor):
        assert extractor.extract("   ") == []


class TestPluralNormalization:
    """Normalizes plural forms to match vocab entries."""

    def test_simple_plural(self, extractor):
        # vocab has "tomato" not "tomatoes"
        result = extractor.extract("I bought fresh tomatoes at the store")
        assert "tomato" in result

    def test_plural_onions(self, extractor):
        # vocab has "onion" not "onions"
        result = extractor.extract("Dice the onions finely")
        assert "onion" in result

    def test_plural_carrots(self, extractor):
        result = extractor.extract("Chop the carrots into small pieces")
        assert "carrot" in result


class TestCompoundIngredients:
    """Handles multi-word ingredients like 'olive oil' and 'soy sauce'."""

    def test_olive_oil(self, extractor):
        result = extractor.extract("Drizzle some olive oil over the salad")
        assert "olive oil" in result

    def test_soy_sauce(self, extractor):
        result = extractor.extract("Add a splash of soy sauce to the stir fry")
        assert "soy sauce" in result

    def test_coconut_milk(self, extractor):
        result = extractor.extract("Pour in the coconut milk and simmer")
        assert "coconut milk" in result

    def test_sesame_oil(self, extractor):
        result = extractor.extract("Finish with a drizzle of sesame oil")
        assert "sesame oil" in result

    def test_bay_leaf(self, extractor):
        result = extractor.extract("Add a bay leaf to the soup")
        assert "bay leaf" in result


class TestSortedOutput:
    """Returns results as a sorted list."""

    def test_results_are_sorted(self, extractor):
        result = extractor.extract(
            "I need salt, butter, garlic, and olive oil"
        )
        assert result == sorted(result)

    def test_returns_list_type(self, extractor):
        result = extractor.extract("garlic and salt")
        assert isinstance(result, list)


class TestDeduplication:
    """Does not return duplicate ingredients."""

    def test_no_duplicates(self, extractor):
        result = extractor.extract(
            "Add garlic, then more garlic, and even more garlic"
        )
        assert result.count("garlic") == 1
