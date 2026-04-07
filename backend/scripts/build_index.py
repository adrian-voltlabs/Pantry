"""Build FAISS index from recipe embeddings."""

import json
import sys
from pathlib import Path

import faiss
import numpy as np

# Add backend dir to path so pantry package is importable
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from pantry.embedder import GloVeEmbedder

DATA_DIR = backend_dir / "data" / "processed"
RECIPES_PATH = DATA_DIR / "recipes.json"
INDEX_PATH = DATA_DIR / "recipes.index"
EMBEDDINGS_PATH = DATA_DIR / "recipe_embeddings.npy"


def main():
    # Load recipes
    print(f"Loading recipes from {RECIPES_PATH} ...")
    with open(RECIPES_PATH, encoding="utf-8") as f:
        recipes = json.load(f)
    print(f"Loaded {len(recipes)} recipes.")

    # Init embedder (loads GloVe + spaCy)
    print("Initializing GloVeEmbedder (loading GloVe + spaCy) ...")
    embedder = GloVeEmbedder()

    # Embed all recipes
    texts = [r["embed_text"] for r in recipes]
    print(f"Embedding {len(texts)} recipes ...")
    embeddings = np.zeros((len(texts), 100), dtype=np.float32)
    for i, text in enumerate(texts):
        vec = embedder.embed_text(text)
        if vec is not None:
            embeddings[i] = vec
        if (i + 1) % 1000 == 0 or (i + 1) == len(texts):
            print(f"  Embedded {i + 1}/{len(texts)} recipes")

    # Normalize for cosine similarity via inner product
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    print("Building FAISS IndexFlatIP(100) ...")
    index = faiss.IndexFlatIP(100)
    index.add(embeddings)
    print(f"Index contains {index.ntotal} vectors.")

    # Save outputs
    faiss.write_index(index, str(INDEX_PATH))
    print(f"Saved index to {INDEX_PATH}")

    np.save(str(EMBEDDINGS_PATH), embeddings)
    print(f"Saved embeddings to {EMBEDDINGS_PATH}")

    print("Done!")


if __name__ == "__main__":
    main()
