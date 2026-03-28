"use client";

import { Hero } from "@/components/hero";
import { SearchInput } from "@/components/search-input";
import { useRecipeSearch } from "@/hooks/use-recipe-search";

export default function Home() {
  const { stage, parsed, results, error, search, reset } = useRecipeSearch();

  const isLoading = stage === "parsing" || stage === "embedding" || stage === "recommending";

  return (
    <div className="flex flex-col flex-1 items-center bg-cream min-h-screen">
      <Hero />
      <SearchInput onSearch={search} isLoading={isLoading} />

      {error && (
        <p className="mt-8 text-red-500 font-body text-sm">{error}</p>
      )}

      {stage === "done" && results.length > 0 && (
        <div className="mt-12 px-4 w-full max-w-4xl">
          <p className="font-body text-terracotta-400 text-center">
            Found {results.length} recipe{results.length !== 1 ? "s" : ""}
          </p>
        </div>
      )}
    </div>
  );
}
