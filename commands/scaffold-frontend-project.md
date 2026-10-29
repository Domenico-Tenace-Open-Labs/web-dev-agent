--- 
description: Scaffold new frontend project from scratch — usage `/scaffold-frontend-project <projectType> <projectName> [dependencies]`. pnpm only; initial 3-page site.
---

Scaffold new frontend project from scratch. Usage: `/scaffold-frontend-project <projectType> <projectName> [dependencies]` — $1 projectType, $2 projectName, $3 dependencies (optional).

1. Create project `$2`, type `$1`, from scratch. `$1`/`$2` missing → ask user.
2. Latest versions of all dependencies. “pnpm”, not "npm" or “yarn.” MANDATORY.
3. Install `$3` + all deps needed for task; set up per project conventions.
4. Strict TypeScript by default where stack supports (no `any`); plain JS only for pure HTML/CSS/JS scaffolds.
5. Apply global structure rules where applicable (Astro → `rules/astro.md`: `public/images/` vs `src/assets/`, layouts, components, kebab-case pages, typed props).
6. On completion generate a simple basic website, three pages: Home, About Us, Contact. Use front-end CSS library if among installed dependencies; else pure CSS.
7. Before wrap-up: typecheck + build pass, no leftover `console.log`/dead code.
