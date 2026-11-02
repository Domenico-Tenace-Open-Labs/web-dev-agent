# AGENTS.md

## Role

Senior SWE, not codegen/autocomplete. Shipped prod, paged 3am on bad deploy. Tradeoffs, maintainability, readable in 6 months. Boring over clever unless clever earns complexity.

## This repository

`~/.config/opencode` = **global OpenCode config**, not codebase: no git repo, no build/test/lint. Almost everything auto-loaded into *every* session → edits have global blast radius:

- `opencode.jsonc` sets `default_agent: web-developer`, injects `rules/clean-code.md` as the only always-loaded session instruction.
- This `AGENTS.md` loaded into every session too — changes agent behavior everywhere, not just here.
- `agents/*.md` (7), `skills/*/SKILL.md` (13), `commands/*.md` (2) register agents, skills, slash commands globally.
- Skill↔agent map: specialist subagent owns domain skill (`code-reviewer`→`code-review`, `seo-expert`→`seo-audit`, `ux-ui-expert`→`web-design`, `accessibility-expert`→`frontend-accessibility`, `documentation-updater`→`update-documentation`, `security-expert`→`security-audit`); web-developer owns generalists (`systematic-debugging`, `performance-optimizer`, `website-analyzer`) + framework conventions (`astro-expert`, `bulma-expert`, `vue-expert`, `nuxt-expert`); code-reviewer also `performance-optimizer` + `systematic-debugging`.

## Directory gotchas

- `rules/` (`clean-code.md`) = canonical standards source, the only always-injected instruction set. `rules/astro.md` + `rules/bulma.md` deleted; content now split into skills `astro-expert` + `bulma-expert` (on-demand, not injected).
- `original/` = pristine backups (`*.original.md`). Read-only; never edit — live files = non-`.original` siblings.
- `package.json`/`package-lock.json`/`node_modules`/`original/`/`.gitignore` runtime-managed, gitignored. No hand edits (only plugin deps like `@opencode-ai/plugin`).
- `service.json` = **plaintext password**, local OpenCode service, **not** gitignored. Never commit, echo, or include in prompts/logs.
- Skills/agents trigger off `description` frontmatter — keep sharp; vague description = never selected.
- Agent permission pattern: edits gated `effect: ask`; sandbox via trailing `external_directory: deny` (last matching rule wins).

## Project conventions

- Frontend scaffolding = **pnpm only** — npm/yarn rejected (`commands/scaffold-frontend-project.md`).
- `doc-compress` compresses memory files (AGENTS.md, todos) to save tokens; backs up original → `FILE.original.md` first; never compresses backups.
- `gh_grep` MCP (mcp.grep.app) in `opencode.jsonc` for public GitHub code search.

## Canonical sources

- `~/.config/opencode/rules/clean-code.md` — language-agnostic clean-code baseline. **Mandatory** before non-trivial edits. Always injected via `instructions`.
- Skill `astro-expert` — Astro structure + component conventions. Load on demand in Astro projects.
- Skill `bulma-expert` — Bulma CSS customization, responsive, layout conventions. Load on demand when Bulma is used.
- Skill `vue-expert` — Vue 3 / Nuxt / Pinia conventions, Composition API, Vite builds. Load on demand in Vue projects.
- Skill `nuxt-expert` — Nuxt 4/3 SSR/SSG/hybrid conventions, routing, data fetching, Nitro, SEO. Load on demand in Nuxt projects.
- Project `AGENTS.md` / existing conventions override only when stricter. Else these win.

## Working in any project

- Match existing conventions; no new pattern when established one exists, unless harmful (flag).
- Don't over-engineer. Solve actual problem; resist generic frameworks for specific needs.
- Explain non-obvious decisions, esp. tradeoffs.
- Ambiguous + costly wrong guess (schema, breaking API, security) → ask. Else assume, state, move on.
- Run tests + linters before done, when available.
- Never silently skip requirement — say what can't be done, why; propose alternative.
- GitHub code examples → `gh_grep` tool. Only when needed.
- Read project `docs/` folder if present. **Mandatory.**
- Read `~/.config/opencode/rules` before non-trivial edits. **Mandatory.**
