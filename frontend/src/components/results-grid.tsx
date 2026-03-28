"use client";

import type { RecipeResult, SearchStage } from "@/lib/types";
import { RecipeCard } from "@/components/recipe-card";

interface ResultsGridProps {
  results: RecipeResult[];
  stage: SearchStage;
}

export function ResultsGrid({ results, stage }: ResultsGridProps) {
  if (stage !== "done" || results.length === 0) return null;

  return (
    <section className="w-full max-w-6xl px-4 mt-12 pb-16">
      <h2 className="font-editorial text-3xl text-terracotta-600 text-center mb-8">
        Recipes for you
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((recipe, i) => (
          <RecipeCard key={recipe.id} recipe={recipe} index={i} />
        ))}
      </div>
    </section>
  );
}
