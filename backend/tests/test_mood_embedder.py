"""Tests for the mood embedder module."""

import numpy as np

from pantry.mood_embedder import MoodEmbedder


class TestMoodEmbedder:
    def setup_method(self):
        self.embedder = MoodEmbedder()

    def test_known_mood_text_returns_vector_with_correct_shape(self):
        result = self.embedder.embed("cozy evening dinner")
        assert result["vector"] is not None
        assert result["vector"].shape == (100,)

    def test_known_mood_text_returns_mood_tokens(self):
        result = self.embedder.embed("cozy evening dinner")
        assert isinstance(result["mood_tokens"], list)
        assert len(result["mood_tokens"]) > 0
        assert "cozy" in result["mood_tokens"]

    def test_no_mood_text_returns_none_vector_and_empty_tokens(self):
        result = self.embedder.embed("chicken rice 30 minutes")
        assert result["vector"] is None
        assert result["mood_tokens"] == []

    def test_returned_vector_is_normalized(self):
        result = self.embedder.embed("cozy evening dinner")
        assert result["vector"] is not None
        norm = np.linalg.norm(result["vector"])
        assert abs(norm - 1.0) < 1e-5
