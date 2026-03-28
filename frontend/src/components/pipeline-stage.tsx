"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Check } from "lucide-react";
import type { SearchStage } from "@/lib/types";

interface PipelineStageProps {
  stage: SearchStage;
}

const steps = [
  { key: "parsing", label: "Parsing text" },
  { key: "embedding", label: "Building embeddings" },
  { key: "recommending", label: "Finding recipes" },
] as const;

const stageOrder: Record<string, number> = {
  parsing: 0,
  embedding: 1,
  recommending: 2,
  done: 3,
};

export function PipelineStage({ stage }: PipelineStageProps) {
  const isVisible =
    stage === "parsing" || stage === "embedding" || stage === "recommending";

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          className="w-full max-w-md px-4 mt-8"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3, ease: "easeOut" }}
        >
          <div className="flex items-center justify-between">
            {steps.map((step, i) => {
              const currentIdx = stageOrder[stage] ?? -1;
              const stepIdx = stageOrder[step.key];
              const isCompleted = currentIdx > stepIdx;
              const isActive = stage === step.key;

              return (
                <div key={step.key} className="flex items-center gap-2 flex-1">
                  {i > 0 && (
                    <div
                      className={`h-px flex-1 transition-colors duration-300 ${
                        isCompleted ? "bg-sage-400" : "bg-terracotta-100"
                      }`}
                    />
                  )}
                  <div className="flex flex-col items-center gap-1.5">
                    <div className="relative">
                      {isCompleted ? (
                        <motion.div
                          className="w-6 h-6 rounded-full bg-sage-400 flex items-center justify-center"
                          initial={{ scale: 0.8 }}
                          animate={{ scale: 1 }}
                          transition={{ duration: 0.2 }}
                        >
                          <Check className="w-3.5 h-3.5 text-white" />
                        </motion.div>
                      ) : isActive ? (
                        <motion.div
                          className="w-6 h-6 rounded-full bg-terracotta-400"
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{
                            duration: 1.2,
                            repeat: Infinity,
                            ease: "easeInOut",
                          }}
                        />
                      ) : (
                        <div className="w-6 h-6 rounded-full border-2 border-terracotta-200 bg-white" />
                      )}
                    </div>
                    <span
                      className={`font-body text-xs whitespace-nowrap ${
                        isActive
                          ? "text-terracotta-600 font-medium"
                          : isCompleted
                            ? "text-sage-500"
                            : "text-terracotta-300"
                      }`}
                    >
                      {step.label}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
