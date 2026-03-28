export interface ParseResponse {
  ingredients: string[];
  constraints: {
    time: "short" | "medium" | "long" | null;
    effort: "low" | "medium" | "high" | null;
  };
  mood_tokens: string[];
}

export interface EmbedResponse {
  query_vector: number[] | null;
  weights: Record<string, any>;
}

export interface RecipeResult {
  id: number;
  title: string;
  ingredients: string[];
  instructions: string;
  image_name: string;
  score: number;
  explanation: {
    matched_ingredients: string[];
    mood_match: boolean;
    constraints_met: Record<string, string>;
  };
}

export interface RecommendResponse {
  results: RecipeResult[];
}

export type SearchStage = "idle" | "parsing" | "embedding" | "recommending" | "done" | "error";
