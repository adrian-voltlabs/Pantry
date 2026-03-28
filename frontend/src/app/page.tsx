"use client";

import { Suspense, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Hero } from "@/components/hero";
import { SearchInput } from "@/components/search-input";
import { ParseFeedback } from "@/components/parse-feedback";
import { PipelineStage } from "@/components/pipeline-stage";
import { SkeletonGrid } from "@/components/skeleton-grid";
import { ResultsGrid } from "@/components/results-grid";
import { useRecipeSearch } from "@/hooks/use-recipe-search";
import Link from "next/link";

function HomeContent() {
  const { stage, parsed, results, error, search, reset } = useRecipeSearch();
  const searchParams = useSearchParams();

  useEffect(() => {
    const q = searchParams.get("q");
    if (q && stage === "idle") {
      search(q);
    }
  }, [searchParams]);

  const isLoading = stage === "parsing" || stage === "embedding" || stage === "recommending";

  const showIdle = stage === "idle" && results.length === 0;

  return (
    <div className="flex flex-col flex-1 items-center bg-cream min-h-screen relative">
      <Link
        href="/about"
        className="absolute top-5 right-6 font-body text-xs text-terracotta-300 hover:text-terracotta-500 transition-colors tracking-wide"
      >
        How it works
      </Link>
      <Hero />
      <SearchInput onSearch={search} isLoading={isLoading} initialQuery={searchParams.get("q") ?? undefined} />
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

      {stage === "done" && results.length === 0 && (
        <div className="mt-12 flex flex-col items-center gap-2">
          <p className="font-editorial text-2xl text-terracotta-400">No recipes found</p>
          <p className="font-body text-sm text-terracotta-300">
            Try different ingredients, a mood, or a time constraint
          </p>
        </div>
      )}

      {showIdle && (
        <Link
          href="/about"
          className="mt-24 mb-8 font-body text-xs text-terracotta-300 hover:text-terracotta-500 tracking-widest uppercase transition-colors"
        >
          How it works &rarr;
        </Link>
      )}
    </div>
  );
}

export default function Home() {
  return (
    <Suspense>
      <HomeContent />
    </Suspense>
  );
}
