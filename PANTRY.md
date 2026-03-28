# Pantry — Recipe Recommendation System

> A classical NLP-powered recipe discovery app. Type in ingredients, a mood, a time constraint — or any combination — and Pantry finds the right recipe for the moment.

---

## Concept

Users type a free-text prompt describing what they have, how they feel, or how much time they have. Pantry parses the input using a classical NLP pipeline, builds a weighted query vector, and returns ranked recipe recommendations with explainability — showing exactly why each recipe matched.

**Example prompts:**
- *"I've got some tomatoes and I'm trying to cook something quick for a cozy evening"*
- *"salmon and lemon, something elegant for a dinner party"*
- *"comfort food, nothing too hard, rainy day vibes"*
- *"chicken, 30 minutes max"*

---

## Stack

### Frontend
- **Framework:** Next.js + React
- **Deployment:** Vercel
- **Animation:** Framer Motion
- **UI Components:** shadcn/ui

### Backend (NLP)
- **Framework:** FastAPI (Python)
- **Deployment:** Railway or Render
- **NLP:** spaCy, Gensim (Word2Vec) or GloVe pre-trained vectors
- **Vector search:** FAISS

### Data
- **Dataset:** Food.com dataset (Kaggle) — ~230k recipes with ingredients, ratings, cooking time, and steps

---

## NLP Pipeline

### Input: free-text user prompt
### Output: ranked list of recipes with match explanations

### Stage 1 — Three Separate Extractors

Each extractor operates independently. Missing signals contribute zero weight, not errors.

| Extractor | Method | Example input → output |
|---|---|---|
| **Ingredient extractor** | spaCy NER + custom entity list built from Food.com ingredient vocabulary | *"tomatoes, salmon"* → `[tomato, salmon]` |
| **Constraint extractor** | Rule-based: keyword lists + regex | *"quick", "30 minutes", "easy"* → `{time: short, effort: low}` |
| **Mood embedder** | Word2Vec/GloVe vector lookup | *"cozy", "rainy day", "comfort"* → mood vector |

### Stage 2 — Weighted Merging

Detected signals are merged into a unified query vector with dynamic weighting:
- Only detected signals carry weight
- Missing signals = zero weight (graceful degradation)
- Works with any combination of inputs

### Stage 3 — FAISS Retrieval

- All 230k Food.com recipes are pre-embedded (title + ingredients + tags concatenated)
- Embeddings stored in a FAISS index for approximate nearest-neighbor search
- Query vector hits the index → returns top-K recipe matches with cosine similarity scores

### Stage 4 — Explainability

Each result includes which signals drove the match:
- Matched ingredients
- Matched constraints (e.g. cooking time ≤ 30 min)
- Mood alignment score

---

## API — FastAPI Backend

**Three endpoints, each stage inspectable independently:**

| Endpoint | Description |
|---|---|
| `POST /parse` | Runs the three extractors on raw input. Returns detected ingredients, constraints, and mood tokens |
| `POST /embed` | Takes parsed output, returns the merged weighted query vector |
| `POST /recommend` | Takes query vector, returns top-K ranked recipes with match explanations |

---

## Recipe Result Cards

Each result card displays:
- Recipe name
- Thumbnail image
- Ingredients list
- Cooking time + difficulty
- Brief description
- **Why it matched** — explainability tags (e.g. "matched: tomatoes · quick · cozy mood")
- User rating (from Food.com dataset)
- Expandable step-by-step instructions (inline, no page navigation)

---

## Visual Design

**Name:** Pantry

**Aesthetic:** Warm & organic foundation with bold editorial energy.

| Element | Direction |
|---|---|
| **Color palette** | Creamy off-whites, terracotta, sage green |
| **Textures** | Hand-drawn / artisanal textures throughout |
| **Typography** | Strong, bold editorial typefaces — loud and expressive |
| **Layout** | Loud hero section, asymmetric where appropriate, feels alive |
| **Mood** | Cozy but stylistic — artisanal meets avant-garde |
| **Animations** | Framer Motion — smooth, purposeful, premium feel |

---

## User Experience

- **No accounts required** — fully stateless, zero friction
- User types prompt → sees what was extracted (ingredient tags, mood, constraints) → sees ranked recipe cards
- Results appear with explainability visible on each card
- Instructions expand inline — no page navigation

---

## Deployment Architecture

```
User → Next.js (Vercel)
           ↓
       FastAPI (Railway/Render)
           ↓
    [spaCy · GloVe · FAISS]
           ↓
    Food.com recipe index
```

---

## Key Design Decisions

- **Classical NLP only** — no LLMs, no generative AI. spaCy, Word2Vec/GloVe, FAISS, rule-based extractors
- **Partial input robustness** — system works with any combination of signals, never breaks on missing input
- **Explainability first** — every result shows its reasoning, making the NLP pipeline visible and demonstrable
- **Fat API** — each pipeline stage is independently inspectable via its own endpoint
- **Stateless** — no database, no auth, no user data stored
