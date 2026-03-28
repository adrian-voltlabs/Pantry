"use client";

import { motion } from "framer-motion";
import { FileText, Layers, Search, ArrowRight, ChevronRight } from "lucide-react";
import Link from "next/link";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0 },
};

const stagger = {
  visible: {
    transition: { staggerChildren: 0.12 },
  },
};

const pipelineStages = [
  {
    icon: FileText,
    title: "Text Parsing",
    description:
      "spaCy NER + custom vocabulary matching extracts ingredients. Rule-based keyword and regex patterns detect time/effort constraints. GloVe similarity identifies mood tokens.",
  },
  {
    icon: Layers,
    title: "Vector Embedding",
    description:
      "Extracted signals are converted to 100-dimensional GloVe vectors. Ingredient and mood vectors are combined with learned weights (0.7 / 0.3) into a single query vector.",
  },
  {
    icon: Search,
    title: "Recipe Retrieval",
    description:
      "FAISS IndexFlatIP performs cosine similarity search over 13,482 pre-embedded recipes. Over-fetches 30 candidates, applies constraint filters, returns top 10 with explainability scores.",
  },
];

const categoryBreakdown = [
  { category: "ingredient-only", prompts: 10, ingredients: "100%", constraints: "100%", mood: "90%" },
  { category: "mood-only", prompts: 8, ingredients: "100%", constraints: "100%", mood: "100%" },
  { category: "constraint-only", prompts: 8, ingredients: "100%", constraints: "100%", mood: "62%" },
  { category: "mixed", prompts: 12, ingredients: "100%", constraints: "100%", mood: "100%" },
  { category: "edge-case", prompts: 9, ingredients: "100%", constraints: "100%", mood: "78%" },
];

const exampleQueries = [
  {
    prompt: "tomatoes and basil, something cozy, 30 minutes",
    ingredients: ["tomato", "basil"],
    mood: ["cozy"],
    constraints: [{ label: "time: short", type: "time" }],
  },
  {
    prompt: "elegant dinner party",
    ingredients: [],
    mood: ["elegant", "party"],
    constraints: [],
  },
  {
    prompt: "quick spicy chicken tacos",
    ingredients: ["chicken"],
    mood: ["spicy"],
    constraints: [{ label: "time: short", type: "time" }],
  },
  {
    prompt: "garlic butter pasta, romantic dinner, under an hour",
    ingredients: ["butter", "garlic", "pasta"],
    mood: ["romantic"],
    constraints: [{ label: "time: medium", type: "time" }],
  },
  {
    prompt: "warm hearty bacon and potato, beginner friendly",
    ingredients: ["bacon", "potato"],
    mood: ["warm", "hearty"],
    constraints: [{ label: "effort: low", type: "effort" }],
  },
];

const techStack = [
  { name: "spaCy", description: "Named entity recognition & tokenization" },
  { name: "GloVe 100d", description: "Word embeddings (via gensim)" },
  { name: "FAISS", description: "Vector similarity search" },
  { name: "FastAPI", description: "Python API server" },
  { name: "Next.js", description: "React frontend framework" },
  { name: "Framer Motion", description: "Animations" },
];

const datasetStats = [
  { value: "13,482", label: "Recipes from Epicurious" },
  { value: "4,675", label: "Unique ingredients in vocabulary" },
  { value: "100d", label: "GloVe vectors (wiki-gigaword-100)" },
];

export default function AboutPage() {
  return (
    <div className="flex flex-col items-center bg-cream min-h-screen">
      {/* Top nav link */}
      <div className="w-full flex justify-between items-center px-6 md:px-10 pt-6">
        <Link
          href="/"
          className="font-editorial text-xl text-terracotta-600 hover:text-terracotta-500 transition-colors"
        >
          Pan<span className="italic text-terracotta-400">try</span>
        </Link>
        <Link
          href="/"
          className="font-body text-sm text-terracotta-300 hover:text-terracotta-500 transition-colors"
        >
          Back to search
        </Link>
      </div>

      <div className="w-full max-w-5xl px-6 md:px-10 pb-24">
        {/* Header */}
        <motion.header
          className="pt-16 pb-16 text-center"
          initial="hidden"
          animate="visible"
          variants={stagger}
        >
          <motion.h1
            variants={fadeUp}
            transition={{ duration: 0.6 }}
            className="font-editorial text-6xl md:text-7xl text-terracotta-600 mb-4"
          >
            How it works
          </motion.h1>
          <motion.div
            variants={fadeUp}
            transition={{ duration: 0.6 }}
            className="flex items-center justify-center gap-3 mb-6"
          >
            <span className="block h-px w-12 bg-terracotta-200" />
            <span className="block h-1.5 w-1.5 rounded-full bg-terracotta-300" />
            <span className="block h-px w-12 bg-terracotta-200" />
          </motion.div>
          <motion.p
            variants={fadeUp}
            transition={{ duration: 0.6 }}
            className="font-body text-lg md:text-xl text-terracotta-400 max-w-2xl mx-auto leading-relaxed tracking-wide"
          >
            A classical NLP pipeline for recipe discovery
          </motion.p>
        </motion.header>

        {/* Section 1: Pipeline Architecture */}
        <motion.section
          className="mb-20"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-editorial text-3xl md:text-4xl text-terracotta-600 text-center mb-12"
          >
            Pipeline Architecture
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-0 items-stretch">
            {pipelineStages.map((stage, i) => (
              <motion.div
                key={stage.title}
                variants={fadeUp}
                transition={{ duration: 0.5 }}
                className="flex items-stretch"
              >
                <div className="flex-1 bg-white border border-terracotta-50 rounded-2xl p-6 md:p-8 flex flex-col items-center text-center">
                  <div className="w-14 h-14 rounded-xl bg-terracotta-50 flex items-center justify-center mb-5">
                    <stage.icon className="w-7 h-7 text-terracotta-500" strokeWidth={1.5} />
                  </div>
                  <h3 className="font-editorial text-xl text-terracotta-600 mb-3">
                    {stage.title}
                  </h3>
                  <p className="font-body text-sm text-terracotta-400 leading-relaxed">
                    {stage.description}
                  </p>
                </div>
                {i < pipelineStages.length - 1 && (
                  <div className="hidden md:flex items-center px-2">
                    <ChevronRight className="w-6 h-6 text-terracotta-200" />
                  </div>
                )}
                {i < pipelineStages.length - 1 && (
                  <div className="flex md:hidden justify-center py-2">
                    <ChevronRight className="w-5 h-5 text-terracotta-200 rotate-90" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Section 2: Evaluation Results */}
        <motion.section
          className="mb-20"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-editorial text-3xl md:text-4xl text-terracotta-600 text-center mb-4"
          >
            Evaluation Results
          </motion.h2>
          <motion.p
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-body text-sm text-terracotta-300 text-center mb-10"
          >
            47 hand-labeled prompts across 5 categories
          </motion.p>

          {/* Overall Metrics */}
          <motion.div
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10"
          >
            <div className="bg-white border border-terracotta-50 rounded-2xl p-6 text-center">
              <p className="font-editorial text-4xl text-sage-500 mb-2">100%</p>
              <p className="font-body text-sm text-terracotta-400">Ingredient Extraction F1</p>
            </div>
            <div className="bg-white border border-terracotta-50 rounded-2xl p-6 text-center">
              <p className="font-editorial text-4xl text-sage-500 mb-2">100%</p>
              <p className="font-body text-sm text-terracotta-400">Constraint Detection Accuracy</p>
            </div>
            <div className="bg-white border border-terracotta-50 rounded-2xl p-6 text-center">
              <p className="font-editorial text-4xl text-terracotta-400 mb-2">80%</p>
              <p className="font-body text-sm text-terracotta-400">Mood Detection F1</p>
              <p className="font-body text-xs text-terracotta-300 mt-1">
                66.7% precision &middot; 100% recall
              </p>
            </div>
          </motion.div>

          {/* Category Breakdown */}
          <motion.div
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="bg-white border border-terracotta-50 rounded-2xl overflow-hidden"
          >
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-terracotta-50">
                    <th className="font-body text-xs font-semibold text-terracotta-400 uppercase tracking-wider px-5 py-4">
                      Category
                    </th>
                    <th className="font-body text-xs font-semibold text-terracotta-400 uppercase tracking-wider px-5 py-4 text-center">
                      Prompts
                    </th>
                    <th className="font-body text-xs font-semibold text-terracotta-400 uppercase tracking-wider px-5 py-4 text-center">
                      Ingredients
                    </th>
                    <th className="font-body text-xs font-semibold text-terracotta-400 uppercase tracking-wider px-5 py-4 text-center">
                      Constraints
                    </th>
                    <th className="font-body text-xs font-semibold text-terracotta-400 uppercase tracking-wider px-5 py-4 text-center">
                      Mood
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {categoryBreakdown.map((row, i) => (
                    <tr
                      key={row.category}
                      className={i < categoryBreakdown.length - 1 ? "border-b border-terracotta-50/60" : ""}
                    >
                      <td className="font-body text-sm text-terracotta-600 px-5 py-3.5 font-medium">
                        {row.category}
                      </td>
                      <td className="font-body text-sm text-terracotta-400 px-5 py-3.5 text-center">
                        {row.prompts}
                      </td>
                      <td className="font-body text-sm text-sage-500 px-5 py-3.5 text-center font-medium">
                        {row.ingredients}
                      </td>
                      <td className="font-body text-sm text-sage-500 px-5 py-3.5 text-center font-medium">
                        {row.constraints}
                      </td>
                      <td
                        className={`font-body text-sm px-5 py-3.5 text-center font-medium ${
                          row.mood === "100%" ? "text-sage-500" : "text-terracotta-400"
                        }`}
                      >
                        {row.mood}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.div>
        </motion.section>

        {/* Section 3: Example Queries */}
        <motion.section
          className="mb-20"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-editorial text-3xl md:text-4xl text-terracotta-600 text-center mb-12"
          >
            Example Queries
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {exampleQueries.map((example) => (
              <motion.div
                key={example.prompt}
                variants={fadeUp}
                transition={{ duration: 0.5 }}
                className="bg-white border border-terracotta-50 rounded-2xl p-6"
              >
                <p className="font-body text-sm text-terracotta-600 font-medium mb-4 italic">
                  &ldquo;{example.prompt}&rdquo;
                </p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {example.ingredients.map((ing) => (
                    <span
                      key={ing}
                      className="font-body text-xs px-2.5 py-1 rounded-full bg-sage-50 text-sage-600 border border-sage-100"
                    >
                      {ing}
                    </span>
                  ))}
                  {example.mood.map((m) => (
                    <span
                      key={m}
                      className="font-body text-xs px-2.5 py-1 rounded-full bg-terracotta-50 text-terracotta-500 border border-terracotta-100"
                    >
                      {m}
                    </span>
                  ))}
                  {example.constraints.map((c) => (
                    <span
                      key={c.label}
                      className="font-body text-xs px-2.5 py-1 rounded-full bg-cream text-terracotta-400 border border-terracotta-100"
                    >
                      {c.label}
                    </span>
                  ))}
                </div>
                <Link
                  href={`/?q=${encodeURIComponent(example.prompt)}`}
                  className="inline-flex items-center gap-1.5 font-body text-xs font-medium text-terracotta-500 hover:text-terracotta-600 transition-colors"
                >
                  Try this search
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Section 4: Tech Stack */}
        <motion.section
          className="mb-20"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-editorial text-3xl md:text-4xl text-terracotta-600 text-center mb-12"
          >
            Tech Stack
          </motion.h2>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {techStack.map((tech) => (
              <motion.div
                key={tech.name}
                variants={fadeUp}
                transition={{ duration: 0.5 }}
                className="bg-white border border-terracotta-50 rounded-2xl p-5 text-center"
              >
                <p className="font-editorial text-lg text-terracotta-600 mb-1">{tech.name}</p>
                <p className="font-body text-xs text-terracotta-300 leading-relaxed">
                  {tech.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Section 5: Dataset */}
        <motion.section
          className="mb-20"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          <motion.h2
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-editorial text-3xl md:text-4xl text-terracotta-600 text-center mb-12"
          >
            Dataset
          </motion.h2>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {datasetStats.map((stat) => (
              <motion.div
                key={stat.label}
                variants={fadeUp}
                transition={{ duration: 0.5 }}
                className="bg-white border border-terracotta-50 rounded-2xl p-6 text-center"
              >
                <p className="font-editorial text-3xl md:text-4xl text-terracotta-500 mb-2">
                  {stat.value}
                </p>
                <p className="font-body text-sm text-terracotta-400">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Footer */}
        <motion.footer
          className="text-center pt-8 pb-4 border-t border-terracotta-50"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={stagger}
        >
          <motion.div variants={fadeUp} transition={{ duration: 0.5 }}>
            <Link
              href="/"
              className="inline-flex items-center gap-2 font-editorial text-2xl text-terracotta-500 hover:text-terracotta-600 transition-colors"
            >
              Try Pantry
              <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>
          <motion.p
            variants={fadeUp}
            transition={{ duration: 0.5 }}
            className="font-body text-xs text-terracotta-300 mt-4 tracking-wide"
          >
            Built with classical NLP techniques — no large language models
          </motion.p>
        </motion.footer>
      </div>
    </div>
  );
}
