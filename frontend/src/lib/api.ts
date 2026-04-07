import type { ParseResponse, EmbedResponse, RecommendResponse } from "./types";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function parse(text: string): Promise<ParseResponse> {
  const res = await fetch(`${BASE_URL}/parse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error(`Parse failed: ${res.statusText}`);
  return res.json();
}

export async function embed(
  ingredients: string[],
  constraints: ParseResponse["constraints"],
  mood_tokens: string[]
): Promise<EmbedResponse> {
  const res = await fetch(`${BASE_URL}/embed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredients, constraints, mood_tokens }),
  });
  if (!res.ok) throw new Error(`Embed failed: ${res.statusText}`);
  return res.json();
}

export async function recommend(
  query_vector: number[] | null,
  constraints: ParseResponse["constraints"],
  ingredients: string[]
): Promise<RecommendResponse> {
  const res = await fetch(`${BASE_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query_vector, constraints, ingredients }),
  });
  if (!res.ok) throw new Error(`Recommend failed: ${res.statusText}`);
  return res.json();
}
