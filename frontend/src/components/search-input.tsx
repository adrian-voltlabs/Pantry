"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Search } from "lucide-react";

interface SearchInputProps {
  onSearch: (text: string) => void;
  isLoading: boolean;
}

export function SearchInput({ onSearch, isLoading }: SearchInputProps) {
  const [text, setText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSearch(text.trim());
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className="w-full max-w-2xl px-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3, ease: "easeOut" }}
    >
      <div className="flex items-center gap-3 bg-white rounded-2xl shadow-sm border border-terracotta-100 px-5 py-3 focus-within:ring-2 focus-within:ring-terracotta-200 transition-shadow">
        <Search className="w-5 h-5 text-terracotta-300 shrink-0" />
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="tomatoes and basil, something cozy, 30 minutes..."
          className="flex-1 bg-transparent font-body text-terracotta-700 placeholder:text-terracotta-200 outline-none text-base"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !text.trim()}
          className="bg-terracotta-500 hover:bg-terracotta-600 disabled:bg-terracotta-200 text-white font-body font-medium text-sm px-5 py-2 rounded-xl transition-colors"
        >
          {isLoading ? "Searching..." : "Search"}
        </button>
      </div>
    </motion.form>
  );
}
