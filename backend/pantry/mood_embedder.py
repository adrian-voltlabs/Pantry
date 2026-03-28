"""Mood embedder using GloVe vectors and spaCy tokenization."""

import numpy as np
import spacy
import gensim.downloader as gensim_api


MOOD_VOCABULARY = {
    # Cozy/warm
    "cozy", "warm", "comfort", "comforting", "homey", "hearty",
    # Elegant
    "elegant", "fancy", "sophisticated", "refined", "classy",
    # Rustic
    "rustic", "simple", "humble", "traditional", "classic",
    # Fresh
    "fresh", "light", "bright", "vibrant", "zesty",
    # Rich
    "rich", "indulgent", "decadent", "luxurious", "creamy",
    # Spicy
    "spicy", "bold", "fiery", "intense", "hot",
    # Healthy
    "healthy", "clean", "nutritious", "wholesome", "lean",
    # Festive
    "festive", "celebration", "party", "special", "holiday",
    # Romantic
    "romantic", "intimate", "date",
    # Casual
    "lazy", "relaxed", "chill", "casual",
    # Adventurous
    "adventurous", "exotic", "unusual", "creative", "fun",
    # Seasonal
    "rainy", "cold", "winter", "summer", "autumn", "spring",
}


class MoodEmbedder:
    """Embeds text into a mood vector using GloVe word embeddings."""

    SIMILARITY_THRESHOLD = 0.65

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        self._glove = gensim_api.load("glove-wiki-gigaword-100")
        # Pre-filter mood vocab to words that exist in GloVe
        self._mood_words = [w for w in MOOD_VOCABULARY if w in self._glove]

    def embed(self, text: str) -> dict:
        """Embed text into a mood vector.

        Returns a dict with:
          - vector: np.ndarray of shape (100,) or None if no mood detected
          - mood_tokens: list of mood-related tokens found
        """
        doc = self._nlp(text.lower())
        tokens = [
            token.text
            for token in doc
            if not token.is_stop and not token.is_punct and token.text.strip()
        ]

        mood_tokens = []
        for token in tokens:
            if token in MOOD_VOCABULARY:
                mood_tokens.append(token)
            elif token in self._glove:
                # Check similarity to mood vocabulary words
                for mood_word in self._mood_words:
                    sim = self._glove.similarity(token, mood_word)
                    if sim > self.SIMILARITY_THRESHOLD:
                        mood_tokens.append(token)
                        break

        if not mood_tokens:
            return {"vector": None, "mood_tokens": []}

        # Average GloVe vectors of mood tokens
        vectors = []
        for token in mood_tokens:
            if token in self._glove:
                vectors.append(self._glove[token])

        if not vectors:
            return {"vector": None, "mood_tokens": []}

        avg_vector = np.mean(vectors, axis=0)
        # Normalize to unit length
        norm = np.linalg.norm(avg_vector)
        if norm > 0:
            avg_vector = avg_vector / norm

        return {"vector": avg_vector, "mood_tokens": mood_tokens}
