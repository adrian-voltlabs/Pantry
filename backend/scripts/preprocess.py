"""
Preprocess the raw Food Ingredients and Recipe Dataset.

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
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    import pandas as pd

    print(f"Loading CSV from {RAW_CSV} ...")
    df = pd.read_csv(RAW_CSV, index_col=0)
    print(f"  Raw rows: {len(df):,}")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates(subset=["Title", "Cleaned_Ingredients"])
    print(f"  After dropping duplicates: {len(df):,} (removed {before - len(df):,})")

    # Drop rows missing Title or Cleaned_Ingredients
    before = len(df)
    df = df.dropna(subset=["Title", "Cleaned_Ingredients"])
    print(f"  After dropping missing Title/Cleaned_Ingredients: {len(df):,} (removed {before - len(df):,})")

    # Parse ingredients
    df["parsed"] = df["Cleaned_Ingredients"].apply(parse_ingredients)

    # Drop rows where parsing yielded nothing
    before = len(df)
    df = df[df["parsed"].apply(len) > 0]
    print(f"  After dropping empty-ingredient rows: {len(df):,} (removed {before - len(df):,})")

    # Normalize ingredients
    df["normalized"] = df["parsed"].apply(
        lambda lst: [normalize_ingredient(ing) for ing in lst]
    )

    # Build ingredient vocabulary (ingredients in >= 3 recipes)
    ingredient_counter: Counter[str] = Counter()
    for ings in df["normalized"]:
        ingredient_counter.update(set(ings))  # count each ingredient once per recipe

    vocab = {
        ing: count
        for ing, count in ingredient_counter.most_common()
        if count >= 3
    }
    print(f"  Ingredient vocabulary size (>=3 recipes): {len(vocab):,}")

    # Build recipe metadata
    recipes = []
    for idx, (_, row) in enumerate(df.iterrows()):
        recipe = {
            "id": idx,
            "title": row["Title"],
            "ingredients": row["normalized"],
            "ingredients_raw": row["parsed"],
            "instructions": row["Instructions"] if isinstance(row["Instructions"], str) else "",
            "image_name": row["Image_Name"] if isinstance(row["Image_Name"], str) else "",
            "embed_text": row["Title"] + " " + " ".join(row["normalized"]),
        }
        recipes.append(recipe)

    # Save outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    recipes_path = OUT_DIR / "recipes.json"
    vocab_path = OUT_DIR / "ingredient_vocab.json"

    with open(recipes_path, "w") as f:
        json.dump(recipes, f, indent=2)
    print(f"  Saved {len(recipes):,} recipes to {recipes_path}")

    with open(vocab_path, "w") as f:
        json.dump(vocab, f, indent=2)
    print(f"  Saved vocabulary ({len(vocab):,} ingredients) to {vocab_path}")

    print("Done!")


if __name__ == "__main__":
    main()
