"use client";

import { motion } from "framer-motion";
import type { ParseResponse, SearchStage } from "@/lib/types";

interface ParseFeedbackProps {
  parsed: ParseResponse | null;
  stage: SearchStage;
}

export function ParseFeedback({ parsed, stage }: ParseFeedbackProps) {
  if (!parsed || stage === "idle") return null;

  const hasSignals =
    parsed.ingredients.length > 0 ||
    parsed.mood_tokens.length > 0 ||
    parsed.constraints.time !== null ||
    parsed.constraints.effort !== null;

  if (!hasSignals) return null;

  const constraintTags: string[] = [];
  if (parsed.constraints.time) constraintTags.push(`Time: ${parsed.constraints.time}`);
  if (parsed.constraints.effort) constraintTags.push(`Effort: ${parsed.constraints.effort}`);

  return (
    <motion.div
      className="w-full max-w-2xl px-4 mt-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
    >
      <p className="font-body text-sm text-terracotta-400 mb-3">Detected signals:</p>
      <div className="flex flex-wrap gap-2">
        {parsed.ingredients.map((ing, i) => (
          <motion.span
            key={`ing-${ing}`}
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-body bg-sage-100 text-sage-600"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
          >
            {ing}
          </motion.span>
        ))}
        {parsed.mood_tokens.map((mood, i) => (
          <motion.span
            key={`mood-${mood}`}
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-body bg-terracotta-100 text-terracotta-600"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{
              duration: 0.3,
              delay: parsed.ingredients.length * 0.05 + i * 0.05,
            }}
          >
            {mood}
          </motion.span>
        ))}
        {constraintTags.map((tag, i) => (
          <motion.span
            key={`con-${tag}`}
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-body bg-cream text-terracotta-500 border border-terracotta-200"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{
              duration: 0.3,
              delay:
                (parsed.ingredients.length + parsed.mood_tokens.length) * 0.05 +
                i * 0.05,
            }}
          >
            {tag}
          </motion.span>
        ))}
      </div>
    </motion.div>
  );
}
