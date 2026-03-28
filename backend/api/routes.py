"""FastAPI route handlers for the Pantry NLP pipeline."""

from __future__ import annotations

from typing import Optional

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Module-level pipeline reference, set by main.py during startup.
pipeline = None

router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class ParseRequest(BaseModel):
    text: str


class ParseResponse(BaseModel):
    ingredients: list[str]
    constraints: dict
    mood_tokens: list[str]


class EmbedRequest(BaseModel):
    ingredients: list[str]
    constraints: dict
    mood_tokens: list[str]


class EmbedResponse(BaseModel):
    query_vector: Optional[list[float]] = None
    weights: dict


class RecommendRequest(BaseModel):
    query_vector: Optional[list[float]] = None
    constraints: dict = {}


class RecipeResult(BaseModel):
    id: int
    title: str
    ingredients: list[str]
    instructions: str
    image_name: Optional[str] = None
    score: float
    explanation: dict


class RecommendResponse(BaseModel):
    results: list[RecipeResult]


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

@router.post("/parse", response_model=ParseResponse)
def parse(req: ParseRequest):
    """Stage 1: extract ingredients, constraints, and mood tokens from text."""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded")

    parsed = pipeline.parse(req.text)
    return ParseResponse(
        ingredients=parsed["ingredients"],
        constraints=parsed["constraints"],
        mood_tokens=parsed["mood_tokens"],
    )


@router.post("/embed", response_model=EmbedResponse)
def embed(req: EmbedRequest):
    """Stage 2: build a weighted query vector from parsed signals."""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded")

    # Re-run mood embedder on the mood_tokens to reconstruct the vector.
    mood_text = " ".join(req.mood_tokens)
    mood_result = pipeline._mood_embedder.embed(mood_text) if req.mood_tokens else {"vector": None, "mood_tokens": []}

    internal_parsed = {
        "ingredients": req.ingredients,
        "constraints": req.constraints,
        "mood_tokens": req.mood_tokens,
        "_mood_vector": mood_result["vector"],
    }

    embedded = pipeline.embed(internal_parsed)
    return EmbedResponse(
        query_vector=embedded["query_vector"],
        weights=embedded["weights"],
    )


@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    """Stage 3: run FAISS retrieval with a query vector."""
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not loaded")

    if req.query_vector is None:
        return RecommendResponse(results=[])

    query_vector = np.array(req.query_vector, dtype=np.float32)

    # Normalize
    norm = np.linalg.norm(query_vector)
    if norm > 0:
        query_vector = query_vector / norm

    # FAISS search
    query_matrix = query_vector.reshape(1, -1).astype(np.float32)
    top_k = 10
    over_fetch = top_k * 3
    scores, indices = pipeline._retriever._index.search(query_matrix, over_fetch)

    results: list[dict] = []
    n_returned = indices.shape[1]
    for rank in range(min(over_fetch, n_returned)):
        idx = int(indices[0][rank])
        if idx < 0:
            continue
        recipe = pipeline._retriever._recipes[idx]
        results.append(
            {
                "id": recipe["id"],
                "title": recipe["title"],
                "ingredients": recipe["ingredients"],
                "instructions": recipe["instructions"],
                "image_name": recipe.get("image_name"),
                "score": float(scores[0][rank]),
                "explanation": {
                    "matched_ingredients": [],
                    "mood_match": False,
                    "constraints_met": req.constraints,
                },
            }
        )
        if len(results) >= top_k:
            break

    return RecommendResponse(results=results)
