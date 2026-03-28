# Pantry — Realigned Project Design Spec

> **Type:** Academic NLP course project
> **Author:** Adrian (solo)
> **Timeline:** 3 weeks
> **Date:** 2026-03-28

---

## 1. Project Framing

Pantry is an academic project for an NLP course. The goal is to demonstrate mastery of classical NLP techniques — text extraction, word embeddings, vector search, and explainability — through an interactive web app that recommends recipes from natural language input.

**What gets graded:** NLP pipeline design, extraction quality, embedding choices, evaluation methodology, and the ability to demonstrate and explain each stage. A written report is required at end of course.

**What the web app is for:** An impressive, interactive delivery vehicle for the NLP work. Better for grades than a static presentation. Not graded as a software product.

**Core constraint:** Classical NLP only — no LLMs, no generative AI. spaCy, Word2Vec/GloVe, FAISS, rule-based extractors.

---

## 2. NLP Pipeline Design

Four stages, each independently testable and demonstrable. Each stage developed first in a Jupyter notebook (doubles as report material).

### Stage 1 — Ingredient Extractor
- **Method:** spaCy NER + custom entity list built from Epicurious ingredient vocabulary
- **Normalization:** Map raw text to canonical ingredient names (e.g., "tomatoes" → "tomato")
- **Output:** List of matched ingredient tokens
- **Notebook evidence:** Extraction on 10-15 example prompts, edge cases (misspellings, compound ingredients like "olive oil")

### Stage 2 — Constraint Extractor
- **Method:** Rule-based — keyword lists + regex patterns
- **Detects:** Time constraints ("30 minutes", "quick", "under an hour") and effort constraints ("easy", "simple")
- **Output:** `{ time: short | medium | long | null, effort: low | medium | high | null }`
- **Notebook evidence:** Keyword lists, regex patterns, extraction results on example prompts

### Stage 3 — Mood Embedder
- **Method:** Word2Vec or GloVe vector lookup for mood-related tokens ("cozy", "elegant", "comfort")
- **Output:** Mood vector representing emotional intent
- **Notebook evidence:** Nearest-neighbor words to mood tokens, t-SNE plot of mood clusters

### Stage 4 — Weighted Merging + FAISS Retrieval
- **Merging:** Combine extracted signals into a single query vector with dynamic weighting. Only detected signals carry weight — missing signals = zero weight, not errors.
- **Index:** FAISS flat index over all pre-embedded recipes (title + ingredients + tags concatenated)
- **Ranking:** Cosine similarity, return top 10 results
- **Explainability:** Each result includes matched ingredients, matched constraints, and mood alignment score
- **Notebook evidence:** Query vector construction, retrieval results, explainability breakdown

### Key Design Decision
Three separate extractors rather than one model — each signal type (entities, rules, semantics) is best served by a different NLP technique. Demonstrates breadth of NLP knowledge and keeps each stage interpretable.

---

## 3. Dataset

**Source:** [Epicurious — Food Ingredients and Recipes Dataset with Images](https://www.kaggle.com/datasets/pes12017000148/food-ingredients-and-recipe-dataset-with-images) (~13,500 recipes with images)

**Why this over Food.com (230k):** Real images make the web app significantly more polished. 13.5k recipes is plenty for demonstrating the NLP pipeline. Evaluators care about pipeline quality, not dataset size.

### Preprocessing Pipeline (Jupyter notebook)
1. Load raw data, drop duplicates and recipes missing critical fields
2. Normalize ingredient names — lowercase, singularize, strip quantities
3. Build custom ingredient vocabulary list (for spaCy extractor)
4. Concatenate title + ingredients + tags (if available) into single text field per recipe
5. Generate embeddings using Word2Vec/GloVe model
6. Build FAISS flat index, persist to disk
7. Save cleaned recipe metadata (name, ingredients, time, steps, rating, description, image) as JSON/pickle

### What Loads at Startup
- FAISS index file
- Recipe metadata (for result cards)
- spaCy model + custom ingredient entity list
- Word2Vec/GloVe model

---

## 4. Evaluation Framework

### Test Set
40-50 hand-labeled prompts covering:
- Ingredient-only ("chicken and rice")
- Mood-only ("cozy comfort food")
- Constraint-only ("under 20 minutes")
- Mixed signals ("salmon, something elegant, 30 minutes")
- Edge cases (vague input, typos, no recognizable signals)

Each prompt labeled with expected extracted ingredients, constraints, and mood tokens.

### Metrics

| What | Metric | Method |
|---|---|---|
| Ingredient extraction | Precision & Recall | Compare against labeled ground truth |
| Constraint extraction | Accuracy | Correct time/effort category? |
| Mood embedding | Qualitative | Nearest-neighbor sanity checks |
| End-to-end retrieval | Relevance@5 | Are ≥3 of top 5 results reasonable? Human judgment |
| Partial input handling | Pass/fail | Returns results (no errors) for every single-signal input |

### For the Report
Metrics table with scores, cherry-picked examples of pipeline working well, 1-2 failure cases with analysis of why they failed.

---

## 5. API Design

FastAPI backend. Three endpoints, each pipeline stage independently callable.

| Endpoint | Input | Output |
|---|---|---|
| `POST /parse` | `{ "text": "..." }` | `{ "ingredients": [...], "constraints": { "time": ..., "effort": ... }, "mood_tokens": [...] }` |
| `POST /embed` | Parsed output | `{ "query_vector": [...], "weights": { "ingredients": ..., "mood": ..., "constraints": ... } }` |
| `POST /recommend` | Query vector + weights | `{ "results": [{ "name": ..., "score": ..., "explanation": { ... }, ... }] }` |

**No production concerns:** No auth, no rate limiting, no error recovery middleware, no OpenAPI polish. Frontend chains all three calls in sequence.

---

## 6. Frontend & UI Design

Next.js + React, shadcn/ui, Framer Motion. Use the **ui-ux-pro-max** and **vercel-react-best-practices** skills when building.

### Visual Design System
| Element | Direction |
|---|---|
| Color palette | Creamy off-whites, terracotta, sage green |
| Textures | Hand-drawn / artisanal textures |
| Typography | Bold, editorial typefaces — loud and expressive |
| Layout | Loud hero section, asymmetric where appropriate |
| Mood | Cozy but stylistic — artisanal meets avant-garde |

### Page Structure (Single Page)
1. **Hero** — Bold name, tagline, single text input front and center
2. **Parse Feedback Strip** — Animated tags/chips showing extracted ingredients, mood tokens, constraint badges (NLP showcase)
3. **Results Grid** — Recipe cards with real images, name, cooking time, rating, match explanation tags. Staggered entrance animation.
4. **Expanded Card** — Inline expand for ingredients list and step-by-step instructions

### Animations (Framer Motion)
- Hero entrance
- Parse tag appearance
- Results card stagger
- Card expand/collapse

### Responsive
- Desktop: multi-column grid
- Mobile: single-column stack

---

## 7. Scope

### In Scope
- Full NLP pipeline (4 stages) with Jupyter notebooks
- FastAPI backend (3 endpoints)
- Next.js frontend with warm editorial design and real recipe images
- Evaluation framework (40-50 labeled prompts, metrics)
- Written report

### Out of Scope
- User accounts, saved recipes, any persistent state
- Dietary restriction filtering
- Deployment optimization (uptime, latency targets, cold start)
- WCAG accessibility compliance
- Configurable top-K (hardcode 10)
- Convenience chaining endpoint
- Meal planning, shopping lists, social features
- Multilingual support

---

## 8. Timeline

### Week 1 — NLP Pipeline (Python only)
- Day 1-2: Dataset exploration, preprocessing notebook, ingredient vocabulary
- Day 3-4: Three extractors as standalone functions, tested in notebooks
- Day 5-6: Recipe embeddings, FAISS index, weighted merging, retrieval
- Day 7: Explainability logic, labeled test set, evaluation, metrics recorded
- **Deliverable:** Working pipeline in Jupyter notebooks, evaluation results

### Week 2 — API + Frontend
- Day 8-9: FastAPI wrapping the pipeline, tested with curl/Postman
- Day 10-13: Next.js frontend (hero, input, parse feedback, results grid, card expand, animations, connect to API)
- **Deliverable:** Working web app connected to API

### Week 3 — Polish + Report
- Day 14-15: UI polish, edge case handling
- Day 16-18: Write report (pipeline design, decisions, evaluation, screenshots)
- Day 19-21: Buffer

**Safety net:** If frontend runs long, week 1's notebooks already contain everything needed for the report and a command-line demo.

---

## 9. Report Outline

1. **Introduction** — Problem statement, why natural language recipe search, why classical NLP over LLMs
2. **Data** — Dataset description, preprocessing decisions, ingredient vocabulary construction
3. **Pipeline Design** — Each stage with rationale (why spaCy NER, why rule-based constraints, why Word2Vec/GloVe, how FAISS works)
4. **Evaluation** — Test set, metrics table, failure case analysis
5. **Demo** — Screenshots of web app showing pipeline in action
6. **Discussion** — Limitations, potential improvements, extensions
7. **Conclusion**

Notebooks from week 1 feed sections 2-4. Web app screenshots feed section 5.
