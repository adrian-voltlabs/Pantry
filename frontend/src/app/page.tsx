"use client";

import { Hero } from "@/components/hero";
import { SearchInput } from "@/components/search-input";
import { ParseFeedback } from "@/components/parse-feedback";
import { ResultsGrid } from "@/components/results-grid";
import { useRecipeSearch } from "@/hooks/use-recipe-search";

export default function Home() {
  const { stage, parsed, results, error, search, reset } = useRecipeSearch();

  const isLoading = stage === "parsing" || stage === "embedding" || stage === "recommending";

  return (
    <div className="flex flex-col flex-1 items-center bg-cream min-h-screen">
      <Hero />
      <SearchInput onSearch={search} isLoading={isLoading} />
      <ParseFeedback parsed={parsed} stage={stage} />

      {error && (
        <p className="mt-8 text-red-500 font-body text-sm">{error}</p>
      )}

      <ResultsGrid results={results} stage={stage} />
    </div>
  );
}
