# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial public release as an [OpenCode](https://opencode.ai) global configuration pack.
- Primary agent `web-developer`: Senior Web Developer for Astro, Vue 3 (+Nuxt), Vite, strict TypeScript, Bulma/Tailwind. Owns the generalist skills.
- Specialist subagents, one per domain: `code-reviewer`, `seo-expert`, `ux-ui-expert`, `accessibility-expert`, `documentation-updater`, `security-expert`.
- Skills: `code-review`, `frontend-accessibility`, `performance-optimizer`, `security-audit` (with `references/checklist.md`), `seo-audit`, `systematic-debugging`, `update-documentation`, `web-design`, `website-analyzer` (with stdlib-only `scripts/fetch_site.py` scanner).
- Slash commands: `/doc-compress` (compress memory files, original backed up as `FILE.original.md`) and `/scaffold-frontend-project` (`pnpm` only, 3-page starter site).
- Rules auto-injected into every session via `opencode.jsonc`: `clean-code`, `astro`, `bulma`.
- `opencode.jsonc` configuration: `web-developer` as default agent, `rules/*.md` injected as session instructions, `gh_grep` remote MCP server.
- Approval-gated permission model: every agent proposes edits first and applies them only after explicit user approval (`effect: ask`).
- Workspace sandboxing for all agents: `external_directory: deny` blocks access outside the project.
- Generic, portable paths throughout the instruction set (relative references, no machine-specific paths).
- MIT license.
- Project documentation: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`.

### Security

- `service.json` (plaintext password of the local OpenCode service) added to `.gitignore` to prevent accidental commits to the repository.
