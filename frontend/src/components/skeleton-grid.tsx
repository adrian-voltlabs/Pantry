"use client";

import { motion } from "framer-motion";

function SkeletonCard({ index }: { index: number }) {
  return (
    <motion.div
      className="bg-white rounded-2xl border border-terracotta-50 overflow-hidden flex flex-col"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.08, ease: "easeOut" }}
    >
      {/* Image placeholder */}
      <div className="h-48 bg-terracotta-50 animate-pulse" />

      <div className="p-5 flex flex-col gap-3">
        {/* Title */}
        <div className="h-5 w-3/4 bg-terracotta-50 rounded-md animate-pulse" />

        {/* Tags */}
        <div className="flex gap-2">
          <div className="h-5 w-16 bg-sage-50 rounded-full animate-pulse" />
          <div className="h-5 w-20 bg-sage-50 rounded-full animate-pulse" />
          <div className="h-5 w-14 bg-terracotta-50 rounded-full animate-pulse" />
        </div>

        {/* Ingredients lines */}
        <div className="space-y-2 mt-1">
          <div className="h-3 w-full bg-terracotta-50 rounded animate-pulse" />
          <div className="h-3 w-2/3 bg-terracotta-50 rounded animate-pulse" />
        </div>
      </div>
    </motion.div>
  );
}

export function SkeletonGrid() {
  return (
    <section className="w-full max-w-6xl px-4 mt-12 pb-16">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array.from({ length: 6 }).map((_, i) => (
          <SkeletonCard key={i} index={i} />
        ))}
      </div>
    </section>
  );
}
