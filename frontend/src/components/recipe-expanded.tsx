"use client";

import { motion, AnimatePresence } from "framer-motion";

interface RecipeExpandedProps {
  ingredients: string[];
  instructions: string;
  isOpen: boolean;
}

export function RecipeExpanded({ ingredients, instructions, isOpen }: RecipeExpandedProps) {
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
          <div className="pt-4 border-t border-terracotta-100">
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
            <p className="font-body text-sm text-terracotta-500 whitespace-pre-line leading-relaxed">
              {instructions}
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
