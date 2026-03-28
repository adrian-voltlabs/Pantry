"""Tests for the FastAPI backend routes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

from api import routes as routes_module


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _mock_pipeline():
    """Inject a mock pipeline into the routes module for every test."""
    mock = MagicMock()

    # parse returns plausible output
    mock.parse.return_value = {
        "ingredients": ["chicken", "garlic"],
        "constraints": {"time": "quick", "effort": None},
        "mood_tokens": ["cozy"],
        "_mood_vector": np.ones(100, dtype=np.float32),
    }

    # mood embedder re-embed
    mock._mood_embedder.embed.return_value = {
        "vector": np.ones(100, dtype=np.float32),
        "mood_tokens": ["cozy"],
    }

    # embed returns plausible output
    mock.embed.return_value = {
        "query_vector": [0.1] * 100,
        "weights": {
            "ingredients": {"active": True, "weight": 0.7, "tokens": ["chicken", "garlic"]},
            "mood": {"active": True, "weight": 0.3},
        },
        "_query_vector_np": np.ones(100, dtype=np.float32),
        "_constraints": {"time": "quick", "effort": None},
    }

    # retriever for /recommend
    fake_scores = np.array([[0.95, 0.90]], dtype=np.float32)
    fake_indices = np.array([[0, 1]], dtype=np.int64)
    mock._retriever._index.search.return_value = (fake_scores, fake_indices)
    mock._retriever._recipes = [
        {
            "id": 1,
            "title": "Garlic Chicken",
            "ingredients": ["chicken", "garlic", "olive oil"],
            "instructions": "Cook chicken with garlic.",
            "image_name": "garlic_chicken.jpg",
        },
        {
            "id": 2,
            "title": "Pasta Primavera",
            "ingredients": ["pasta", "vegetables"],
            "instructions": "Cook pasta with vegetables.",
            "image_name": None,
        },
    ]

    routes_module.pipeline = mock
    yield
    routes_module.pipeline = None


@pytest.fixture()
def client():
    from api.main import app
    return TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_parse(client):
    resp = client.post("/parse", json={"text": "I want cozy chicken with garlic"})
    assert resp.status_code == 200
    body = resp.json()
    assert "ingredients" in body
    assert "constraints" in body
    assert "mood_tokens" in body
    assert isinstance(body["ingredients"], list)
    assert isinstance(body["mood_tokens"], list)


def test_parse_empty_text(client):
    """Empty text should not crash — pipeline mock still returns valid data."""
    resp = client.post("/parse", json={"text": ""})
    assert resp.status_code == 200


def test_embed(client):
    resp = client.post("/embed", json={
        "ingredients": ["chicken", "garlic"],
        "constraints": {"time": "quick"},
        "mood_tokens": ["cozy"],
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "query_vector" in body
    assert "weights" in body


def test_recommend(client):
    resp = client.post("/recommend", json={
        "query_vector": [0.1] * 100,
        "constraints": {},
    })
    assert resp.status_code == 200
    body = resp.json()
    assert "results" in body
    assert isinstance(body["results"], list)
    assert len(body["results"]) > 0
    result = body["results"][0]
    assert "id" in result
    assert "title" in result
    assert "score" in result
    assert "explanation" in result


def test_recommend_null_vector(client):
    """Null query_vector should return empty results, not crash."""
    resp = client.post("/recommend", json={
        "query_vector": None,
        "constraints": {},
    })
    assert resp.status_code == 200
    assert resp.json()["results"] == []
