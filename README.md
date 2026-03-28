# Pantry

A classical NLP recipe recommendation system. Enter ingredients you have on hand and Pantry suggests recipes using spaCy NER, GloVe embeddings, and FAISS similarity search.

## Prerequisites

- Python 3.10+
- Node.js 18+
- The raw dataset CSV: **Food Ingredients and Recipe Dataset with Image Name Mapping.csv** (place it in `backend/data/raw/`)

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Preprocess Data

The raw CSV and generated index files are gitignored due to size. After placing the dataset CSV in `backend/data/raw/`, run:

```bash
python scripts/preprocess.py
python scripts/build_index.py
```

This generates `recipes.json`, `ingredient_vocab.json`, `recipes.index`, and `recipe_embeddings.npy` in `backend/data/processed/`.

### Run the API

```bash
uvicorn api.main:app --reload
```

The API runs at `http://localhost:8000`. Check `http://localhost:8000/health` to verify.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:3000`. The frontend calls the backend at `http://localhost:8000` by default. To override, set:

```
NEXT_PUBLIC_API_URL=http://your-backend-host:port
```

### Food Images

Recipe images are gitignored. To display them locally, symlink the dataset's image folder:

```bash
ln -s ../backend/data/raw/Food\ Images frontend/public/images
```

## Project Structure

```
backend/
  api/          # FastAPI app and route handlers
  pantry/       # NLP pipeline (embedder, NER, FAISS search)
  scripts/      # Data preprocessing and index building
  data/         # Raw dataset and processed artifacts
  tests/        # pytest tests
  notebooks/    # Jupyter notebooks for exploration
  evaluation/   # Pipeline evaluation scripts

frontend/
  src/          # Next.js app (React 19, Tailwind CSS)
```
