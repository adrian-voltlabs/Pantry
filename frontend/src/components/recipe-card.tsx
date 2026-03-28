"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import type { RecipeResult } from "@/lib/types";
import { RecipeExpanded } from "@/components/recipe-expanded";

interface RecipeCardProps {
  recipe: RecipeResult;
  index: number;
}

export function RecipeCard({ recipe, index }: RecipeCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [imgError, setImgError] = useState(false);

  const visibleIngredients = recipe.ingredients.slice(0, 5);
  const remaining = recipe.ingredients.length - 5;

  const scorePercent = Math.round(recipe.score * 100);

  // Filter out empty/null/undefined constraint values
  const validConstraints = Object.entries(recipe.explanation.constraints_met).filter(
    ([, val]) => val !== null && val !== undefined && val !== ""
  );

  return (
    <motion.div
      className="bg-white rounded-2xl shadow-sm border border-terracotta-50 overflow-hidden flex flex-col hover:shadow-lg transition-shadow duration-300"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1, ease: "easeOut" }}
    >
      {!imgError && (
        <div className="relative h-48 overflow-hidden bg-terracotta-50">
          <img
            src={`/images/${recipe.image_name}.jpg`}
            alt={recipe.title}
            className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
            onError={() => setImgError(true)}
          />
          {/* Dark gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent pointer-events-none" />
          {/* Score badge */}
          <div className="absolute top-3 right-3 w-10 h-10 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-sm">
            <span className="font-body text-xs font-semibold text-terracotta-600">
              {scorePercent}%
            </span>
          </div>
        </div>
      )}

      <div className="p-5 flex flex-col flex-1">
        <h3 className="font-editorial text-xl text-terracotta-700 mb-3">
          {recipe.title}
        </h3>

        {/* Explanation tags */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {recipe.explanation.matched_ingredients.map((ing) => (
            <span
              key={ing}
              className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-body bg-sage-100 text-sage-600"
            >
              {ing}
            </span>
          ))}
          {recipe.explanation.mood_match && (
            <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-body bg-terracotta-100 text-terracotta-600">
              mood match
            </span>
          )}
          {validConstraints.map(([key, val]) => (
            <span
              key={key}
              className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-body bg-cream text-terracotta-500 border border-terracotta-200"
            >
              {key}: {val}
            </span>
          ))}
        </div>

        {/* Truncated ingredients */}
        <p className="font-body text-sm text-terracotta-400 mb-4">
          {visibleIngredients.join(", ")}
          {remaining > 0 && ` +${remaining} more`}
        </p>

        <div className="mt-auto">
          <button
            onClick={() => setExpanded(!expanded)}
            className="cursor-pointer font-body text-sm font-medium text-terracotta-500 hover:text-terracotta-600 transition-colors"
          >
            {expanded ? "Hide steps" : "Show steps"}
          </button>
        </div>

        <RecipeExpanded
          ingredients={recipe.ingredients}
          instructions={recipe.instructions}
          isOpen={expanded}
        />
      </div>
    </motion.div>
  );
}
