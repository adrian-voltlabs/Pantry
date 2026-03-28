"""GloVe embedder for recipe text using spaCy tokenization."""

import numpy as np
import spacy
import gensim.downloader as gensim_api


class GloVeEmbedder:
    """Embeds text into 100-d vectors by averaging GloVe word embeddings."""

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        self._glove = gensim_api.load("glove-wiki-gigaword-100")
        self._dim = 100

    def embed_text(self, text: str) -> np.ndarray | None:
        """Embed text by averaging GloVe vectors of non-stop, non-punct tokens.

        Returns a unit-length vector of shape (100,), or None if no tokens
        have GloVe vectors.
        """
        doc = self._nlp(text.lower())
        vectors = [
            self._glove[token.text]
            for token in doc
            if not token.is_stop
            and not token.is_punct
            and token.text.strip()
            and token.text in self._glove
        ]

        if not vectors:
            return None

        avg = np.mean(vectors, axis=0)
        norm = np.linalg.norm(avg)
        if norm > 0:
            avg = avg / norm
        return avg

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Embed a list of texts, returning an (N, 100) array.

        Texts that cannot be embedded get a zero vector.
        """
        results = np.zeros((len(texts), self._dim), dtype=np.float32)
        for i, text in enumerate(texts):
            vec = self.embed_text(text)
            if vec is not None:
                results[i] = vec
        return results
