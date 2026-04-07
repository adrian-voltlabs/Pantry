"use client";

import { useState, useCallback } from "react";
import type { SearchStage, ParseResponse, RecipeResult } from "@/lib/types";
import { parse, embed, recommend } from "@/lib/api";

export function useRecipeSearch() {
  const [stage, setStage] = useState<SearchStage>("idle");
  const [parsed, setParsed] = useState<ParseResponse | null>(null);
  const [results, setResults] = useState<RecipeResult[]>([]);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(async (text: string) => {
    try {
      setError(null);
      setResults([]);
      setParsed(null);

      setStage("parsing");
      const parseData = await parse(text);
      setParsed(parseData);

      setStage("embedding");
      const embedData = await embed(
        parseData.ingredients,
        parseData.constraints,
        parseData.mood_tokens
      );

      setStage("recommending");
      const recData = await recommend(embedData.query_vector, parseData.constraints, parseData.ingredients);
      setResults(recData.results);

      setStage("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setStage("error");
    }
  }, []);

  const reset = useCallback(() => {
    setStage("idle");
    setParsed(null);
    setResults([]);
    setError(null);
  }, []);

  return { stage, parsed, results, error, search, reset };
}
