"""FastAPI application for the Pantry NLP recipe recommendation pipeline."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import routes as routes_module
from api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the pipeline on startup."""
    from pantry.pipeline import PantryPipeline

    routes_module.pipeline = PantryPipeline()
    yield
    routes_module.pipeline = None


app = FastAPI(title="Pantry API", lifespan=lifespan)

# CORS — allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
