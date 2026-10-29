---
name: performance-optimizer
description: Analyze codebase for performance issues and code quality problems, then apply optimizations directly to code. Use when user asks to analyze performance, audit code quality, find bottlenecks, reduce bundle size, optimize images/assets, remove duplicated code, or "make the code faster/cleaner/lighter" — even if not named explicitly. Trigger on "check the performance of this project", "optimize my codebase", "find and fix inefficiencies", "reduce bundle size", "clean up duplicated code".
---

# Codebase Performance Optimizer

Two phases: **Analyze** then **Optimize**. Always show findings before touching code, unless user says "just fix it".

## Phase 1 — Analyze

1. Map project: language(s), framework, build tool, package manager. Use `view` on root dir, then relevant configs (package.json, webpack/vite config, tsconfig, etc).
2. Scan for these issue categories (use `bash_tool` with grep/find, or language-specific tools when available):
   - **Duplication**: repeated logic/blocks across files (near-identical functions, copy-pasted components).
   - **Bundle size**: heavy/unused deps, missing tree-shaking, no code-splitting, large barrel imports.
   - **Images/assets**: uncompressed images, wrong format (e.g. PNG where WebP/AVIF fits), oversized dimensions, missing lazy-loading.
   - **Runtime perf**: N+1 queries, unnecessary re-renders (React: missing memo/useMemo/useCallback, inline object/function props), blocking sync I/O, unindexed DB queries, O(n²) loops on large data.
   - **Dead code**: unused exports, unreachable branches, commented-out blocks.
   - **Build config**: missing minification, no compression (gzip/brotli), dev-only code shipped to prod.
3. Produce findings report (in chat, concise): per issue — file:line, what's wrong, estimated impact (high/medium/low), proposed fix.
4. Ask user which categories to act on if list long (use `ask_user_input_v0`), unless already said "fix everything".

## Phase 2 — Optimize

Apply fixes incrementally, one category at a time, so changes stay reviewable:

- **Dedup**: extract shared logic into function/module/component; update call sites.
- **Bundle**: replace heavy deps with lighter alternatives (only if drop-in compatible), add/adjust code-splitting or dynamic imports, fix barrel-import issues.
- **Images**: recompress/convert via `bash_tool` (e.g. `cwebp`, `sharp`, `imagemin` if available — check what's installed first), resize to actual display dimensions, add lazy-loading attributes.
- **Runtime**: apply memoization, batch queries, replace O(n²) with efficient structures/algorithms.
- **Dead code**: remove after confirming no external references (grep whole repo first).

After each category: run existing tests/build if project has them (`npm test`, `npm run build`, etc.) to confirm nothing broke. Report what changed and why, file by file, in short summary — not just "done".

## Rules

- Never guess at "optimized" behavior that changes program output — perf fixes must be behavior-preserving.
- Don't install new deps for a fix if native/existing solution works.
- No test suite → flag it and proceed more conservatively (smaller diffs, manual reasoning about correctness).
- Very large repos → sample representative files/modules first, not blind full scan; ask user for subfolder if scope unclear.