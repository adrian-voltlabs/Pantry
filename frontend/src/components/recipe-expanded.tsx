"use client";

import { motion, AnimatePresence } from "framer-motion";

interface RecipeExpandedProps {
  ingredients: string[];
  instructions: string;
  isOpen: boolean;
}

function splitIntoSteps(instructions: string): string[] {
  // Split by sentence-ending punctuation followed by space, or by newlines
  const raw = instructions
    .split(/(?<=[.!?])\s+|\n+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
  return raw;
}

export function RecipeExpanded({ ingredients, instructions, isOpen }: RecipeExpandedProps) {
  const steps = splitIntoSteps(instructions);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          transition={{ duration: 0.3, ease: "easeInOut" }}
          className="overflow-hidden"
        >
          <div className="pt-4 mt-4 border-t border-terracotta-100 bg-terracotta-50 -mx-5 px-5 pb-4 rounded-b-2xl">
            <h4 className="font-body font-semibold text-sm text-terracotta-600 mb-2">
              Ingredients
            </h4>
            <ul className="list-disc list-inside space-y-1 mb-4">
              {ingredients.map((ing, i) => (
                <li key={i} className="font-body text-sm text-terracotta-500">
                  {ing}
                </li>
              ))}
            </ul>
            <h4 className="font-body font-semibold text-sm text-terracotta-600 mb-2">
              Instructions
            </h4>
            <ol className="list-none space-y-2">
              {steps.map((step, i) => (
                <li key={i} className="font-body text-sm text-terracotta-500 flex gap-2">
                  <span className="font-semibold text-terracotta-400 shrink-0">
                    {i + 1}.
                  </span>
                  <span className="leading-relaxed">{step}</span>
                </li>
              ))}
            </ol>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
