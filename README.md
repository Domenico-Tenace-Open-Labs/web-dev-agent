# Web Dev Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ready-to-use set of [OpenCode](https://opencode.ai) agents, skills, slash commands and rules for modern frontend development, with a specialist subagent for every domain (code review, SEO, UI/UX, accessibility, documentation, security), an approval-gated permission model, and clean-code conventions injected into every session.

This repository is an **OpenCode global configuration** (default location: `~/.config/opencode`), not a traditional codebase: there is no build step, no test suite, no application runtime.

## Features

- 🧭 **Primary agent**, [`web-developer`](agents/web-developer.md): Senior Web Developer for Astro, Vue 3 (+Nuxt), Vite and strict TypeScript, with Bulma/Tailwind styling. Owns the generalist skills (debugging, performance, website analysis).
- 🧩 **Six specialist subagents**, each owning one skill: [code review](agents/code-reviewer.md), [SEO](agents/seo-expert.md), [UI/UX](agents/ux-ui-expert.md), [accessibility](agents/accessibility-expert.md), [documentation](agents/documentation-updater.md), [security](agents/security-expert.md).
- 🛡️ **Safe by default**, every write/edit is approval-gated (`effect: ask`); the workspace is sandboxed (`external_directory: deny`). Propose first, apply only after explicit approval.
- 📏 **Enforced conventions**, `clean-code`, `astro` and `bulma` rules are auto-injected into every session via `opencode.jsonc`.
- ⌨️ **Slash commands**, scaffold a new frontend project (`pnpm` only) or compress memory files to save tokens.
- 🌐 **MCP**, ships the `gh_grep` remote server for public GitHub code search.

## Repository structure

```
web-dev-agent/
├── agents/                      # 7 agent definitions (frontmatter: description, mode, permissions)
│   ├── web-developer.md         #   primary agent
│   ├── code-reviewer.md
│   ├── seo-expert.md
│   ├── ux-ui-expert.md
│   ├── accessibility-expert.md
│   ├── documentation-updater.md
│   └── security-expert.md
├── skills/                      # 9 skills (each <name>/SKILL.md) + supporting files
│   ├── code-review/
│   ├── frontend-accessibility/
│   ├── performance-optimizer/
│   ├── security-audit/
│   │   └── references/checklist.md
│   ├── seo-audit/
│   ├── systematic-debugging/
│   ├── update-documentation/
│   ├── web-design/
│   └── website-analyzer/
│       └── scripts/fetch_site.py  # stdlib-only scanner, prints JSON analysis
├── commands/                    # 2 slash commands
│   ├── doc-compress.md
│   └── scaffold-frontend-project.md
├── rules/                       # 3 instruction sets, auto-injected into sessions
│   ├── clean-code.md
│   ├── astro.md
│   └── bulma.md
├── AGENTS.md                    # global agent instructions (loaded into every session)
├── opencode.jsonc               # config: default agent, rules injection, gh_grep MCP
└── LICENSE
```

`package.json` / `package-lock.json` / `node_modules` / `original/` are runtime-managed and gitignored, no manual dependency install.

## Contents

### Agents

| Agent | Mode | Owns skill | Role |
|---|---|---|---|
| [`web-developer`](agents/web-developer.md) | primary | `systematic-debugging`, `performance-optimizer`, `website-analyzer` | Senior Web Developer (Astro, Vue, Vite, TS, Bulma/Tailwind): implementation, responsive, a11y, performance, SEO |
| [`code-reviewer`](agents/code-reviewer.md) | subagent | `code-review` (+ `performance-optimizer`, `systematic-debugging`) | Reviews code changes; reports by severity with `path:line` and concrete fixes |
| [`seo-expert`](agents/seo-expert.md) | subagent | `seo-audit` | Audits on-page/technical/content SEO and **suggests** fixes, never edits |
| [`ux-ui-expert`](agents/ux-ui-expert.md) | subagent | `web-design` | Designs and reviews UI/UX and graphics against the existing design system |
| [`accessibility-expert`](agents/accessibility-expert.md) | subagent | `frontend-accessibility` | Audits and fixes WCAG 2.2 AA issues; no conformance claims without evidence |
| [`documentation-updater`](agents/documentation-updater.md) | subagent | `update-documentation` | Keeps README, changelog, API docs and comments in sync with the code |
| [`security-expert`](agents/security-expert.md) | subagent | `security-audit` | Severity-ranked security audits: source code, secrets, dependencies, IaC |

### Skills

| Skill | Purpose |
|---|---|
| `code-review` | Checklist review: readability, best practices, testing, performance, security, documentation |
| `frontend-accessibility` | Build a11y into components, pages, forms, navigation, media and interaction patterns |
| `performance-optimizer` | Analyze then optimize: duplication, bundle size, images, runtime hotspots, dead code |
| `security-audit` | Output concise, deduplicated, severity-ranked findings (Critical → Info), with rubric |
| `seo-audit` | Suggest-only SEO fixes: meta tags, headings, structured data, sitemap/robots, content |
| `systematic-debugging` | Root-cause analysis before touching code: reproduce → isolate → fix → verify → explain |
| `update-documentation` | Docs as implementation-verified source of truth; focused diffs, no invention |
| `web-design` | UI/UX checklist: design system consistency, responsive behavior, motion, contrast |
| `website-analyzer` | Analyzes a live site from its URL and writes a compact `docs/ANALYSIS.md` report |

### Commands

| Slash command | What it does |
|---|---|
| `/doc-compress <filepath>` | Compresses memory files (AGENTS.md, todos, preferences) into caveman format to save input tokens; backs up the original as `<file>.original.md` |
| `/scaffold-frontend-project <type> <name> [deps]` | Scaffolds a new frontend project from scratch, **pnpm only**, with strict TypeScript and a basic 3-page site (Home, About, Contact) |

### Rules

| Rule | Scope |
|---|---|
| `rules/clean-code.md` | Language-agnostic clean-code baseline: naming, small functions, error handling, security, tests, Definition of Done, red flags |
| `rules/astro.md` | Astro project structure (`public/images/` vs `src/assets/`), component conventions, naming, typed props |
| `rules/bulma.md` | Use Bulma as intended: customization via SCSS variables only, no class overrides, no `!important`, kebab-case custom classes |

## Installation

1. Clone this repository.
2. Copy its contents into your OpenCode global config directory:

   ```bash
   cp -r web-dev-agent/. ~/.config/opencode/
   ```

   (On non-UNIX systems, use OpenCode's config path for your platform.)
3. Restart your OpenCode session.

No manual dependency install: `package.json` / `node_modules` are runtime-managed.

**Requirements**

- [OpenCode](https://opencode.ai), recent version
- Python 3 (standard library only), used by the `website-analyzer` scanner
- `pnpm`, only if you use `/scaffold-frontend-project`

## How it works

- **Skill ↔ agent map**, each specialist subagent owns one domain skill and loads it first; the primary agent owns the generalist skills and delegates the rest. Skills/agents trigger off their `description` frontmatter.
- **Approval gate**, the primary and all subagents use `effect: ask` on edits: nothing is written without explicit user approval.
- **Sandbox**, `external_directory: deny` is declared last so it wins over every earlier `allow`, blocking reads/writes/shell access outside the workspace.
- **Auto-injected instructions**, `opencode.jsonc` sets `default_agent: web-developer` and injects `rules/*.md` (plus `AGENTS.md`) into every session, so conventions apply everywhere.
- **Generic by design**, instructions reference paths relative to the config root (e.g. `rules/astro.md`), so the setup works on any machine without path rewrites.

## Security notes

- `service.json` (local OpenCode service, contains a **plaintext password**) is gitignored, never commit, echo, or paste it into prompts/logs.
- Agents never operate outside the workspace sandbox. If outside access is required they say so and propose an alternative instead of bypassing the boundary.
- The security baseline in `rules/clean-code.md` requires no secrets in code/VCS/logs, parameterized queries, and validated external input.

## Contributing

Keep agent/skill `description` frontmatter sharp, it drives skill/agent selection. Follow the conventions in [`AGENTS.md`](AGENTS.md) and `rules/` when editing. Before a non-trivial change, read `rules/clean-code.md`. Do not commit `node_modules`, `package.json`/`package-lock.json`, `original/`, or `service.json` (all gitignored).

## License

[MIT](LICENSE), Copyright (c) 2026 Domenico
