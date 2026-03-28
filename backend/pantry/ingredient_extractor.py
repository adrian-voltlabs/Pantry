"""Ingredient extractor using spaCy NER and vocabulary matching."""

from __future__ import annotations

import json
from pathlib import Path

import spacy


class IngredientExtractor:
    """Extract ingredient names from free text.

    Uses two complementary strategies:
    1. Direct vocabulary matching against unigrams and bigrams.
    2. spaCy named-entity recognition checked against the vocabulary.

    Tokens are normalised (lowercased, simple plural stripping) before
    comparison so that "tomatoes" matches the vocab entry "tomato".
    """

    # Common base ingredients that should always be recognized, even if
    # the vocabulary only contains compound forms like "cream cheese, softened".
    _BASE_INGREDIENTS: set[str] = {
        "cheese", "bread", "milk", "butter", "cream", "egg", "flour", "sugar",
        "salt", "pepper", "oil", "rice", "pasta", "chicken", "beef", "pork",
        "fish", "salmon", "shrimp", "onion", "garlic", "tomato", "potato",
        "carrot", "celery", "lemon", "lime", "orange", "apple", "banana",
        "chocolate", "vanilla", "cinnamon", "honey", "vinegar", "mustard",
        "yogurt", "ham", "bacon", "sausage", "turkey", "lamb", "tofu",
        "corn", "bean", "pea", "spinach", "lettuce", "cucumber", "avocado",
        "mushroom", "ginger", "basil", "parsley", "cilantro", "thyme",
        "rosemary", "oregano", "cumin", "paprika", "nutmeg", "coconut",
        "almond", "walnut", "pecan", "cashew", "peanut", "oat", "barley",
        "quinoa", "noodle", "tortilla", "wine", "beer", "broth", "stock",
    }

    def __init__(
        self,
        vocab_path: str = "data/processed/ingredient_vocab.json",
    ) -> None:
        self._vocab: set[str] = self._load_vocab(vocab_path)
        self._vocab |= self._BASE_INGREDIENTS
        self._nlp = spacy.load("en_core_web_sm")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, text: str) -> list[str]:
        """Return a sorted, deduplicated list of ingredients found in *text*."""
        if not text or not text.strip():
            return []

        doc = self._nlp(text.lower())
        found: set[str] = set()

        # Strategy 1: n-gram vocabulary lookup (unigrams + bigrams)
        tokens = [tok.text for tok in doc if not tok.is_punct and not tok.is_space]
        for token in tokens:
            normalised = self._normalise(token)
            if normalised in self._vocab:
                found.add(normalised)

        for a, b in zip(tokens, tokens[1:]):
            bigram = f"{a} {b}"
            if bigram in self._vocab:
                found.add(bigram)
            normalised_bigram = f"{self._normalise(a)} {self._normalise(b)}"
            if normalised_bigram in self._vocab:
                found.add(normalised_bigram)

        # Strategy 2: spaCy NER — check entity text against vocab
        for ent in doc.ents:
            ent_text = ent.text.strip()
            if ent_text in self._vocab:
                found.add(ent_text)
            normalised_ent = self._normalise(ent_text)
            if normalised_ent in self._vocab:
                found.add(normalised_ent)

        return sorted(found)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _load_vocab(path: str) -> set[str]:
        """Load ingredient vocabulary from a JSON file.

        The file is expected to be a JSON object mapping ingredient names
        (strings) to counts (integers).  We only need the keys.
        """
        full_path = Path(path)
        with full_path.open() as fh:
            data: dict[str, int] = json.load(fh)
        return {k.lower() for k in data}

    @staticmethod
    def _normalise(token: str) -> str:
        """Cheap singular-form heuristic for English food words."""
        token = token.lower().strip()
        if token.endswith("ies"):
            # e.g. "berries" -> "berry"  (but don't mangle 2-letter stems)
            candidate = token[:-3] + "y"
            if len(candidate) > 2:
                return candidate
        if token.endswith("ves"):
            # e.g. "halves" -> "half"  (not universally correct, but good enough)
            return token[:-3] + "f"
        if token.endswith("ses") or token.endswith("zes"):
            return token[:-2]
        if token.endswith("es"):
            return token[:-2]
        if token.endswith("s") and not token.endswith("ss"):
            return token[:-1]
        return token
