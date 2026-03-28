# Pantry — Product Requirements Document

> **Version:** 1.0
> **Last Updated:** 2026-03-28
> **Status:** Draft

---

## 1. Overview

**Product Name:** Pantry

**Vision:** A recipe discovery app powered by classical NLP that understands natural language — ingredients, moods, time constraints, or any combination — and returns ranked recipe recommendations with full explainability.

**One-liner:** Type what you have, how you feel, or how long you've got — Pantry finds the right recipe for the moment.

---

## 2. Problem Statement

### The Problem
Finding the right recipe is a surprisingly frustrating experience. Users know what ingredients they have, how much time they have, or what kind of meal they're in the mood for — but existing recipe platforms force them into rigid search interfaces: dropdown filters, category browsing, or keyword-exact matching. These tools don't understand intent, can't combine multiple signals, and never explain why a result was chosen.

### Why Existing Solutions Fall Short
- **Traditional recipe sites** (AllRecipes, Food Network) rely on keyword search and category filters — they can't interpret "cozy dinner with salmon, nothing too hard"
- **AI chatbot approaches** (ChatGPT, etc.) generate recipes on the fly but lack a curated dataset, can hallucinate ingredients, and don't provide consistent, rankable results
- **No solution today** combines free-text understanding, multi-signal parsing, ranked retrieval over a real dataset, and match explainability in a single, frictionless experience

### What Pantry Does Differently
Pantry uses a classical NLP pipeline (no LLMs) to parse free-text input into structured signals — ingredients, constraints, and mood — then retrieves from a real dataset of 230k recipes using vector similarity search. Every result explains exactly why it matched.

---

## 3. Target Users

### Primary Persona: The Everyday Home Cook
- **Who:** Adults who cook at home regularly (3-7 times/week)
- **Frustration:** Knows what they have in the fridge and how they feel, but struggles to find the right recipe quickly
- **Behavior:** Would rather type "chicken, something quick and cozy" than browse categories and apply filters
- **Tech comfort:** Comfortable using web apps; doesn't need onboarding or tutorials

### Secondary Persona: The Curious Explorer
- **Who:** Food enthusiasts who enjoy discovering new recipes based on mood or occasion
- **Frustration:** Recipe fatigue — keeps making the same things because discovery tools are poor
- **Behavior:** Types mood-driven prompts like "elegant dinner party" or "rainy day comfort food"

### Secondary Persona: The Practical Planner
- **Who:** Budget-conscious or time-constrained cooks
- **Frustration:** Has specific ingredients to use up and a time limit, needs recipes that match both
- **Behavior:** Types "tomatoes, rice, 20 minutes" and expects results that respect all constraints

---

## 4. User Stories

### Input & Search
- **US-1:** As a user, I can type a free-text prompt describing ingredients, mood, time constraints, or any combination, so that I don't have to use rigid search filters.
- **US-2:** As a user, I can submit a prompt with only ingredients (e.g., "tomatoes and basil") and receive relevant results, so that the system works even without mood or time input.
- **US-3:** As a user, I can submit a prompt with only a mood (e.g., "cozy comfort food") and receive relevant results.
- **US-4:** As a user, I can submit a prompt with only constraints (e.g., "30 minutes, easy") and receive relevant results.
- **US-5:** As a user, I can submit a prompt combining all signal types (e.g., "salmon and lemon, something elegant, under an hour") and receive results that account for all of them.

### Parsing Transparency
- **US-6:** As a user, I can see what the system extracted from my prompt (detected ingredients, mood tokens, constraints) before viewing results, so I understand how my input was interpreted.
- **US-7:** As a user, I can verify that the system correctly parsed my intent, giving me confidence in the results.

### Results & Explainability
- **US-8:** As a user, I see a ranked list of recipe cards after submitting my prompt, so I can quickly scan my options.
- **US-9:** As a user, each recipe card shows me *why it matched* my query (e.g., "matched: tomatoes · quick · cozy mood"), so I understand the recommendation logic.
- **US-10:** As a user, I can see the recipe name, thumbnail, cooking time, difficulty, rating, and a brief description on each card without clicking into it.
- **US-11:** As a user, I can expand a recipe card inline to see step-by-step instructions without navigating to a new page.

### General Experience
- **US-12:** As a user, I can use Pantry without creating an account or logging in, so there's zero friction.
- **US-13:** As a user, the interface feels warm, polished, and inviting — not clinical or utilitarian.

---

## 5. Functional Requirements

### 5.1 Free-Text Input
| ID | Requirement | Priority |
|---|---|---|
| FR-1 | The system shall accept a single free-text input field as the primary (and only) search mechanism | P0 |
| FR-2 | The input field shall accept prompts of any length, with no minimum or maximum character limit enforced in the UI | P0 |
| FR-3 | The system shall handle prompts containing any combination of: ingredients, mood descriptors, time/effort constraints — including prompts with only one signal type | P0 |
| FR-4 | The system shall gracefully handle empty or nonsensical input (no crashes, meaningful feedback to user) | P1 |

### 5.2 NLP Pipeline — Extraction
| ID | Requirement | Priority |
|---|---|---|
| FR-5 | **Ingredient Extractor:** The system shall identify food ingredients from free text using spaCy NER combined with a custom entity list built from the Food.com ingredient vocabulary | P0 |
| FR-6 | The ingredient extractor shall normalize ingredient names to match the Food.com dataset vocabulary (e.g., "tomatoes" → "tomato") | P0 |
| FR-7 | **Constraint Extractor:** The system shall detect time constraints (e.g., "30 minutes", "quick", "under an hour") and effort constraints (e.g., "easy", "simple", "nothing too hard") using keyword lists and regex rules | P0 |
| FR-8 | The constraint extractor shall map detected constraints to structured values: `{time: short/medium/long, effort: low/medium/high}` | P0 |
| FR-9 | **Mood Embedder:** The system shall map mood-related tokens (e.g., "cozy", "elegant", "comfort") to vector representations using Word2Vec or GloVe pre-trained embeddings | P0 |
| FR-10 | Missing signals from any extractor shall contribute zero weight to the query — not errors or defaults | P0 |

### 5.3 NLP Pipeline — Merging & Retrieval
| ID | Requirement | Priority |
|---|---|---|
| FR-11 | The system shall merge extracted signals (ingredients, constraints, mood vector) into a single weighted query vector | P0 |
| FR-12 | Signal weights shall be dynamic: only detected signals carry weight, proportional to their presence in the prompt | P0 |
| FR-13 | All 230k Food.com recipes shall be pre-embedded (title + ingredients + tags concatenated) and stored in a FAISS index | P0 |
| FR-14 | The system shall perform approximate nearest-neighbor search against the FAISS index using the query vector | P0 |
| FR-15 | The system shall return the top-K recipe matches ranked by cosine similarity score | P0 |
| FR-16 | K (number of results) shall be configurable, with a default of 10 | P1 |

### 5.4 Explainability
| ID | Requirement | Priority |
|---|---|---|
| FR-17 | Each result shall include an explanation of which signals drove the match | P0 |
| FR-18 | Explanations shall include: matched ingredients, matched constraints (with values), and mood alignment score | P0 |
| FR-19 | Explanations shall be displayed as human-readable tags on each recipe card (e.g., "matched: tomatoes · quick · cozy mood") | P0 |

### 5.5 Recipe Display
| ID | Requirement | Priority |
|---|---|---|
| FR-20 | Each recipe result card shall display: recipe name, thumbnail image, ingredients list, cooking time, difficulty, brief description, user rating (from Food.com), and match explanation tags | P0 |
| FR-21 | Each recipe card shall be expandable inline to reveal step-by-step cooking instructions | P0 |
| FR-22 | Expanding instructions shall not trigger page navigation — all content renders within the current view | P0 |

### 5.6 API Endpoints
| ID | Requirement | Priority |
|---|---|---|
| FR-23 | `POST /parse` — Accepts raw text input, returns detected ingredients, constraints, and mood tokens | P0 |
| FR-24 | `POST /embed` — Accepts parsed output, returns the merged weighted query vector | P0 |
| FR-25 | `POST /recommend` — Accepts query vector, returns top-K ranked recipes with match explanations | P0 |
| FR-26 | Each endpoint shall be independently callable (fat API design) for inspectability and debugging | P0 |
| FR-27 | A convenience endpoint or client-side flow shall chain all three stages for the standard user experience | P1 |

---

## 6. Non-Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| NFR-1 | **Response Time:** End-to-end query (input → results) shall complete in under 2 seconds for 95th percentile requests | P0 |
| NFR-2 | **FAISS Query Time:** Vector search against the 230k recipe index shall complete in under 100ms | P0 |
| NFR-3 | **Availability:** The application shall target 99% uptime (acceptable for a portfolio/demo project) | P2 |
| NFR-4 | **Statelessness:** The system shall store no user data — no accounts, no sessions, no cookies beyond what's required for the app to function | P0 |
| NFR-5 | **Browser Support:** The frontend shall support the latest versions of Chrome, Firefox, Safari, and Edge | P1 |
| NFR-6 | **Responsive Design:** The frontend shall be usable on desktop (1024px+) and mobile (375px+) viewports | P1 |
| NFR-7 | **Accessibility:** The frontend shall meet WCAG 2.1 AA standards for color contrast, keyboard navigation, and screen reader compatibility | P1 |
| NFR-8 | **Cold Start:** The backend shall load the FAISS index and NLP models at startup, not per-request | P0 |

---

## 7. Technical Architecture

### Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js + React, deployed on Vercel |
| **UI Components** | shadcn/ui |
| **Animation** | Framer Motion |
| **Backend** | FastAPI (Python), deployed on Railway or Render |
| **NLP** | spaCy, Gensim (Word2Vec) or GloVe pre-trained vectors |
| **Vector Search** | FAISS |
| **Dataset** | Food.com (Kaggle) — ~230k recipes |

### Deployment Architecture

```
User → Next.js (Vercel)
           ↓
       FastAPI (Railway/Render)
           ↓
    [spaCy · GloVe · FAISS]
           ↓
    Food.com recipe index
```

### Key Architectural Decisions
- **Classical NLP only** — no LLMs, no generative AI. This is intentional: demonstrates NLP fundamentals (tokenization, embeddings, vector search) and keeps the system deterministic and explainable.
- **Fat API** — each pipeline stage has its own endpoint, making the NLP pipeline inspectable and debuggable independently.
- **Stateless** — no database, no auth, no user data. Simplifies deployment and eliminates privacy concerns.
- **Pre-computed embeddings** — all recipe embeddings are generated offline and loaded at startup via FAISS index, keeping query-time fast.

---

## 8. Data Requirements

### Dataset: Food.com (Kaggle)
- **Size:** ~230,000 recipes
- **Fields used:** Recipe name, ingredients list, cooking time, tags, steps/instructions, user ratings, description
- **Source:** https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions

### Preprocessing Pipeline
| Step | Description |
|---|---|
| **Data Cleaning** | Remove duplicates, handle missing fields (especially cooking time, ingredients) |
| **Ingredient Normalization** | Standardize ingredient names to build the custom entity vocabulary for the ingredient extractor |
| **Text Concatenation** | Concatenate recipe title + ingredients + tags into a single text field per recipe |
| **Embedding Generation** | Generate vector embeddings for each recipe's concatenated text using Word2Vec/GloVe |
| **FAISS Index Build** | Build and persist a FAISS index from all recipe embeddings |
| **Thumbnail Resolution** | Determine image strategy — Food.com dataset may not include images (see Open Questions) |

---

## 9. UI/UX Requirements

### Visual Design System
| Element | Specification |
|---|---|
| **Color Palette** | Creamy off-whites, terracotta, sage green — warm and organic |
| **Textures** | Hand-drawn / artisanal textures throughout the UI |
| **Typography** | Bold, editorial typefaces — loud and expressive headings, clean body text |
| **Layout** | Loud hero section, asymmetric where appropriate, feels alive and editorial |
| **Mood** | Cozy but stylistic — artisanal meets avant-garde |

### Animations (Framer Motion)
| Element | Animation |
|---|---|
| **Page load** | Hero section entrance animation |
| **Search submission** | Smooth transition from input state to results state |
| **Parsing display** | Extracted tags animate in as they're detected |
| **Recipe cards** | Staggered entrance animation for results list |
| **Card expansion** | Smooth inline expand/collapse for instructions |

### Layout Structure
1. **Hero Section** — Bold, editorial landing with the search input prominently centered
2. **Parsing Feedback** — Displays extracted ingredients, mood, and constraints as visual tags/chips
3. **Results Grid** — Recipe cards in a responsive grid/list layout
4. **Recipe Card** — Compact view with all key info + expandable instructions

### Responsive Behavior
- Desktop: multi-column recipe grid
- Tablet: 2-column grid
- Mobile: single-column stack, full-width cards

---

## 10. Scope & Constraints

### In Scope (v1)
- Single-page application with free-text search
- Full NLP pipeline: ingredient extraction, constraint extraction, mood embedding
- FAISS-based recipe retrieval over Food.com dataset
- Explainable results with match tags
- Recipe cards with inline expandable instructions
- Three inspectable API endpoints (`/parse`, `/embed`, `/recommend`)
- Responsive design (desktop + mobile)
- Deployed and publicly accessible

### Out of Scope (v1)
- User accounts, saved recipes, or any persistent user state
- Recipe submission or user-generated content
- Dietary restriction filtering (vegan, gluten-free, etc.) — could be a v2 feature
- Meal planning or weekly schedule features
- Shopping list generation
- Social features (sharing, comments, ratings)
- Multilingual support
- Offline/PWA support
- Recipe images beyond what's available in the dataset

---

## 11. Success Metrics

| Metric | Target | How to Measure |
|---|---|---|
| **Parse Accuracy** | ≥ 85% of test prompts have all signals correctly extracted | Manual evaluation against a labeled test set of 50+ prompts |
| **Result Relevance** | ≥ 70% of top-5 results rated "relevant" by human evaluators | Manual evaluation: does the recipe match the intent of the prompt? |
| **Response Time** | < 2s end-to-end (p95) | Backend timing logs |
| **Explainability Clarity** | Users can identify why each result matched from the tags alone | Qualitative review — are the match tags accurate and understandable? |
| **Partial Input Handling** | System returns reasonable results for any single-signal input | Test with ingredient-only, mood-only, and constraint-only prompts |
| **Deployment** | App is live, publicly accessible, and functional | Verify both frontend (Vercel) and backend (Railway/Render) are up |

---

## 12. Open Questions

| # | Question | Impact |
|---|---|---|
| 1 | **Recipe Images:** Does the Food.com dataset include image URLs, or do we need a fallback strategy (placeholder images, generated thumbnails, or an external image API)? | Affects FR-20 (recipe card display) |
| 2 | **Mood Vocabulary:** How large should the mood token vocabulary be? Should we curate a fixed list or use embedding similarity to catch any adjective? | Affects FR-9 (mood embedder design) |
| 3 | **Top-K Default:** What's the right default number of results — 10, 15, 20? | Affects FR-16 and UI layout |
| 4 | **Embedding Model:** Word2Vec (Gensim) vs. GloVe pre-trained — which performs better for food/mood domain? Needs experimentation. | Affects FR-9, FR-13 |
| 5 | **Constraint Thresholds:** What are the exact cutoffs for time categories (short/medium/long) and effort categories (low/medium/high)? | Affects FR-8 |
| 6 | **FAISS Index Size:** What's the expected index size for 230k recipe embeddings, and does it fit in memory on Railway/Render free/starter tiers? | Affects deployment feasibility |
| 7 | **Font Selection:** Which specific editorial typefaces to use? Need to select fonts that are web-safe or available via Google Fonts. | Affects UI implementation |
| 8 | **Error States:** What should the UI show for zero-result queries or completely unparseable input? | Affects FR-4 and UX |
