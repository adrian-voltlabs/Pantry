"use client";

import { motion } from "framer-motion";

export function Hero() {
  return (
    <motion.div
      className="flex flex-col items-center text-center pt-24 pb-8 px-4"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, ease: "easeOut" }}
    >
      <h1 className="font-editorial text-6xl md:text-7xl text-terracotta-600 mb-4">
        Pantry
      </h1>
      <p className="font-body text-lg md:text-xl text-terracotta-400 max-w-lg leading-relaxed">
        Type what you have, how you feel, or how long you&apos;ve got. We&apos;ll find the right recipe.
      </p>
    </motion.div>
  );
}
