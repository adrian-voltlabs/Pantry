"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Search, Loader2 } from "lucide-react";

interface SearchInputProps {
  onSearch: (text: string) => void;
  isLoading: boolean;
  initialQuery?: string;
}

const exampleQueries = [
  "chicken and rice, cozy",
  "quick pasta under 30 min",
  "elegant dinner party",
];

export function SearchInput({ onSearch, isLoading, initialQuery }: SearchInputProps) {
  const [text, setText] = useState("");

  useEffect(() => {
    if (initialQuery) setText(initialQuery);
  }, [initialQuery]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSearch(text.trim());
    }
  };

  const handleExampleClick = (query: string) => {
    if (!isLoading) {
      setText(query);
      onSearch(query);
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
      <div className="flex items-center gap-3 bg-white rounded-2xl shadow-md border border-terracotta-100 px-6 py-4 focus-within:ring-2 focus-within:ring-terracotta-200 transition-shadow">
        {isLoading ? (
          <Loader2 className="w-5 h-5 text-terracotta-400 shrink-0 animate-spin" />
        ) : (
          <Search className="w-5 h-5 text-terracotta-300 shrink-0" />
        )}
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="tomatoes and basil, something cozy, 30 minutes..."
          className="flex-1 bg-transparent font-body text-terracotta-700 placeholder:text-terracotta-200 outline-none text-lg"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !text.trim()}
          className="bg-terracotta-500 hover:bg-terracotta-600 disabled:bg-terracotta-200 text-white font-body font-medium text-sm px-6 py-2.5 rounded-xl transition-colors"
        >
          {isLoading ? "Searching..." : "Search"}
        </button>
      </div>

      {/* Example queries */}
      <div className="flex flex-wrap items-center justify-center gap-2 mt-3">
        <span className="font-body text-xs text-terracotta-300">Try:</span>
        {exampleQueries.map((query) => (
          <button
            key={query}
            type="button"
            onClick={() => handleExampleClick(query)}
            disabled={isLoading}
            className="font-body text-xs text-terracotta-400 hover:text-terracotta-600 bg-white/60 hover:bg-white border border-terracotta-100 rounded-full px-3 py-1 transition-colors disabled:opacity-50"
          >
            {query}
          </button>
        ))}
      </div>
    </motion.form>
  );
}
