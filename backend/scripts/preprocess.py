"""
Preprocess the raw recipe datasets.

Sources:
  - Food Ingredients and Recipe Dataset with Image Name Mapping.csv
  - recipes_w_search_terms.csv

Outputs:
  - backend/data/processed/recipes.json
  - backend/data/processed/ingredient_vocab.json
"""

import ast
import json
import re
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent          # backend/
RAW_CSV = ROOT / "data" / "raw" / "Food Ingredients and Recipe Dataset with Image Name Mapping.csv"
RAW_CSV_2 = ROOT / "data" / "raw" / "recipes_w_search_terms.csv"
OUT_DIR = ROOT / "data" / "processed"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Common units to strip from ingredient names
_UNITS = (
    r"cups?|c\.|tbsps?|tablespoons?|tsps?|teaspoons?|ozs?|ounces?|lbs?|pounds?|"
    r"grams?|g\b|kgs?|kilograms?|mls?|milliliters?|liters?|l\b|"
    r"pinch(es)?|dash(es)?|cloves?|slices?|pieces?|cans?|packages?|"
    r"stalks?|sprigs?|bunche?s?|heads?|inches?|in\."
)

# Regex: leading quantities like "1", "1/2", "1.5", "½", ranges "1-2", etc.
_QTY_RE = re.compile(
    r"^[\d¼½¾⅓⅔⅛⅜⅝⅞/.\-–—\s]+",
)

# Regex: parenthetical notes like "(about 3 lb.)" or "(optional)"
_PAREN_RE = re.compile(r"\([^)]*\)")

# Regex: unit words right after quantity removal
_UNIT_RE = re.compile(rf"^({_UNITS})\b\.?\s*", re.IGNORECASE)

# Very basic singularization: trailing "es" / "s"
_PLURAL_SPECIAL = {
    "tomatoes": "tomato",
    "potatoes": "potato",
    "anchovies": "anchovy",
    "cherries": "cherry",
    "berries": "berry",
    "strawberries": "strawberry",
    "blueberries": "blueberry",
    "raspberries": "raspberry",
    "cranberries": "cranberry",
    "leaves": "leaf",
}


def _singularize(word: str) -> str:
    if word in _PLURAL_SPECIAL:
        return _PLURAL_SPECIAL[word]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("ses") or word.endswith("shes") or word.endswith("ches"):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def normalize_ingredient(raw: str) -> str:
    """Normalize a single ingredient string."""
    s = raw.lower().strip()
    # Remove parenthetical notes
    s = _PAREN_RE.sub("", s)
    # Remove leading quantities
    s = _QTY_RE.sub("", s).strip()
    # Remove unit words
    s = _UNIT_RE.sub("", s).strip()
    # Remove leftover punctuation at edges
    s = s.strip(",.;:- ")
    # Basic singularization of the last word
    words = s.split()
    if words:
        words[-1] = _singularize(words[-1])
    return " ".join(words)


def parse_ingredients(raw: str) -> list[str]:
    """Parse a stringified Python list of ingredients."""
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        return []


# ---------------------------------------------------------------------------
# Per-dataset loaders
# ---------------------------------------------------------------------------

def _load_image_dataset(pd) -> list[dict]:
    """Load and normalise the Image Name Mapping CSV."""
    print(f"Loading CSV from {RAW_CSV} ...")
    df = pd.read_csv(RAW_CSV, index_col=0)
    print(f"  Raw rows: {len(df):,}")

    before = len(df)
    df = df.drop_duplicates(subset=["Title", "Cleaned_Ingredients"])
    print(f"  After dropping duplicates: {len(df):,} (removed {before - len(df):,})")

    before = len(df)
    df = df.dropna(subset=["Title", "Cleaned_Ingredients"])
    print(f"  After dropping missing Title/Cleaned_Ingredients: {len(df):,} (removed {before - len(df):,})")

    df["parsed"] = df["Cleaned_Ingredients"].apply(parse_ingredients)

    before = len(df)
    df = df[df["parsed"].apply(len) > 0]
    print(f"  After dropping empty-ingredient rows: {len(df):,} (removed {before - len(df):,})")

    df["normalized"] = df["parsed"].apply(
        lambda lst: [normalize_ingredient(ing) for ing in lst]
    )

    records = []
    for _, row in df.iterrows():
        records.append({
            "title": row["Title"],
            "ingredients": row["normalized"],
            "ingredients_raw": row["parsed"],
            "instructions": row["Instructions"] if isinstance(row["Instructions"], str) else "",
            "image_name": row["Image_Name"] if isinstance(row["Image_Name"], str) else "",
            "tags": [],
            "search_terms": [],
        })
    print(f"  Produced {len(records):,} records from dataset 1.\n")
    return records


def _load_search_terms_dataset(pd) -> list[dict]:
    """Load and normalise the recipes_w_search_terms CSV."""
    print(f"Loading CSV from {RAW_CSV_2} ...")
    df = pd.read_csv(RAW_CSV_2)
    print(f"  Raw rows: {len(df):,}")

    before = len(df)
    df = df.drop_duplicates(subset=["name", "ingredients"])
    print(f"  After dropping duplicates: {len(df):,} (removed {before - len(df):,})")

    before = len(df)
    df = df.dropna(subset=["name", "ingredients"])
    print(f"  After dropping missing name/ingredients: {len(df):,} (removed {before - len(df):,})")

    df["parsed"] = df["ingredients"].apply(parse_ingredients)

    before = len(df)
    df = df[df["parsed"].apply(len) > 0]
    print(f"  After dropping empty-ingredient rows: {len(df):,} (removed {before - len(df):,})")

    df["normalized"] = df["parsed"].apply(
        lambda lst: [normalize_ingredient(ing) for ing in lst]
    )

    # Parse steps list into a single instructions string
    def _steps_to_str(raw) -> str:
        if not isinstance(raw, str):
            return ""
        try:
            steps = ast.literal_eval(raw)
            if isinstance(steps, list):
                return " ".join(str(s) for s in steps)
        except (ValueError, SyntaxError):
            pass
        return str(raw)

    # Parse raw ingredient strings list
    def _parse_raw_str(raw) -> list[str]:
        if not isinstance(raw, str):
            return []
        try:
            items = ast.literal_eval(raw)
            if isinstance(items, list):
                return [str(i) for i in items]
        except (ValueError, SyntaxError):
            pass
        return []

    # Parse tags / search_terms sets/lists stored as strings
    def _parse_set_str(raw) -> list[str]:
        if not isinstance(raw, str):
            return []
        try:
            obj = ast.literal_eval(raw)
            if isinstance(obj, (set, list)):
                return sorted(str(v) for v in obj)
        except (ValueError, SyntaxError):
            pass
        return []

    records = []
    for _, row in df.iterrows():
        records.append({
            "title": row["name"],
            "ingredients": row["normalized"],
            "ingredients_raw": _parse_raw_str(row.get("ingredients_raw_str", "")),
            "instructions": _steps_to_str(row.get("steps", "")),
            "image_name": "",
            "tags": _parse_set_str(row.get("tags", "")),
            "search_terms": _parse_set_str(row.get("search_terms", "")),
        })
    print(f"  Produced {len(records):,} records from dataset 2.\n")
    return records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    import pandas as pd

    records1 = _load_image_dataset(pd)
    records2 = _load_search_terms_dataset(pd)

    # Merge and de-duplicate across both datasets by case-insensitive title
    seen_titles: set[str] = set()
    all_records: list[dict] = []
    for record in records1 + records2:
        key = record["title"].lower().strip()
        if key not in seen_titles:
            seen_titles.add(key)
            all_records.append(record)

    print(f"Combined unique recipes: {len(all_records):,} "
          f"({len(records1):,} from dataset 1, {len(records2):,} from dataset 2, "
          f"{len(records1) + len(records2) - len(all_records):,} cross-dataset duplicates removed)")

    # Assign sequential IDs and build embed_text
    recipes = []
    for idx, record in enumerate(all_records):
        recipes.append({
            "id": idx,
            **record,
            "embed_text": record["title"] + " " + " ".join(record["ingredients"]),
        })

    # Build ingredient vocabulary (ingredients appearing in >= 3 recipes)
    ingredient_counter: Counter[str] = Counter()
    for r in recipes:
        ingredient_counter.update(set(r["ingredients"]))

    vocab = {
        ing: count
        for ing, count in ingredient_counter.most_common()
        if count >= 3
    }
    print(f"Ingredient vocabulary size (>=3 recipes): {len(vocab):,}")

    # Save outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    recipes_path = OUT_DIR / "recipes.json"
    vocab_path = OUT_DIR / "ingredient_vocab.json"

    with open(recipes_path, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(recipes):,} recipes to {recipes_path}")

    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=2, ensure_ascii=False)
    print(f"Saved vocabulary ({len(vocab):,} ingredients) to {vocab_path}")

    print("Done!")


if __name__ == "__main__":
    main()
