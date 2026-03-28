"use client";

import { motion } from "framer-motion";
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
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        <h2 className="font-editorial text-3xl text-terracotta-600 text-center mb-2">
          Recipes for you
        </h2>
        <p className="font-body text-sm text-terracotta-400 text-center mb-4">
          {results.length} recipe{results.length !== 1 ? "s" : ""} found
        </p>
        <div className="flex items-center justify-center gap-3 mb-8">
          <span className="block h-px flex-1 max-w-24 bg-terracotta-100" />
          <span className="block h-1 w-1 rounded-full bg-terracotta-200" />
          <span className="block h-px flex-1 max-w-24 bg-terracotta-100" />
        </div>
      </motion.div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {results.map((recipe, i) => (
          <RecipeCard key={recipe.id} recipe={recipe} index={i} />
        ))}
      </div>
    </section>
  );
}
