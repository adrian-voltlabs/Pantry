"use client";

import { motion } from "framer-motion";
import { Leaf, Sparkles, Clock, Flame } from "lucide-react";
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

  const constraintTags: { label: string; type: "time" | "effort" }[] = [];
  if (parsed.constraints.time)
    constraintTags.push({ label: `Time: ${parsed.constraints.time}`, type: "time" });
  if (parsed.constraints.effort)
    constraintTags.push({ label: `Effort: ${parsed.constraints.effort}`, type: "effort" });

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
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-sm font-body bg-sage-100 text-sage-600"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
          >
            <Leaf className="w-3.5 h-3.5" />
            {ing}
          </motion.span>
        ))}
        {parsed.mood_tokens.map((mood, i) => (
          <motion.span
            key={`mood-${mood}`}
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-sm font-body bg-terracotta-100 text-terracotta-600"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{
              duration: 0.3,
              delay: parsed.ingredients.length * 0.05 + i * 0.05,
            }}
          >
            <Sparkles className="w-3.5 h-3.5" />
            {mood}
          </motion.span>
        ))}
        {constraintTags.map((tag, i) => (
          <motion.span
            key={`con-${tag.label}`}
            className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-sm font-body bg-cream text-terracotta-500 border border-terracotta-200"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{
              duration: 0.3,
              delay:
                (parsed.ingredients.length + parsed.mood_tokens.length) * 0.05 +
                i * 0.05,
            }}
          >
            {tag.type === "time" ? (
              <Clock className="w-3.5 h-3.5" />
            ) : (
              <Flame className="w-3.5 h-3.5" />
            )}
            {tag.label}
          </motion.span>
        ))}
      </div>
    </motion.div>
  );
}
