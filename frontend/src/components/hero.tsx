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
      <h1 className="font-editorial text-7xl md:text-8xl text-terracotta-600 mb-2">
        Pan<span className="italic text-terracotta-400">try</span>
      </h1>
      <div className="flex items-center gap-3 mb-5">
        <span className="block h-px w-12 bg-terracotta-200" />
        <span className="block h-1.5 w-1.5 rounded-full bg-terracotta-300" />
        <span className="block h-px w-12 bg-terracotta-200" />
      </div>
      <p className="font-body text-lg md:text-xl text-terracotta-400 max-w-lg leading-loose tracking-wide">
        Type what you have, how you feel, or how long you&apos;ve got.{" "}
        We&apos;ll find the right recipe.
      </p>
    </motion.div>
  );
}
