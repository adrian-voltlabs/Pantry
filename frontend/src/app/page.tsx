"use client";

import { Hero } from "@/components/hero";
import { SearchInput } from "@/components/search-input";
import { ParseFeedback } from "@/components/parse-feedback";
import { PipelineStage } from "@/components/pipeline-stage";
import { SkeletonGrid } from "@/components/skeleton-grid";
import { ResultsGrid } from "@/components/results-grid";
import { useRecipeSearch } from "@/hooks/use-recipe-search";

export default function Home() {
  const { stage, parsed, results, error, search, reset } = useRecipeSearch();

  const isLoading = stage === "parsing" || stage === "embedding" || stage === "recommending";

  const showIdle = stage === "idle" && results.length === 0;

  return (
    <div className="flex flex-col flex-1 items-center bg-cream min-h-screen">
      <Hero />
      <SearchInput onSearch={search} isLoading={isLoading} />
      <ParseFeedback parsed={parsed} stage={stage} />
      <PipelineStage stage={stage} />

      {error && (
        <div className="mt-8 flex flex-col items-center gap-3">
          <p className="text-red-500 font-body text-sm">{error}</p>
          <button
            onClick={reset}
            className="font-body text-sm font-medium text-white bg-terracotta-500 hover:bg-terracotta-600 px-5 py-2 rounded-xl transition-colors"
          >
            Try again
          </button>
        </div>
      )}

      {stage === "recommending" && <SkeletonGrid />}

      <ResultsGrid results={results} stage={stage} />

      {showIdle && (
        <p className="mt-24 mb-8 font-body text-xs text-terracotta-300 tracking-widest uppercase">
          Powered by classical NLP
        </p>
      )}
    </div>
  );
}
