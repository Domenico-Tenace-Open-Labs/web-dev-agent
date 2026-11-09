# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial public release as an [OpenCode](https://opencode.ai) global configuration pack.
- Primary agent `web-developer`: Senior Web Developer for Astro, Vue 3 (+Nuxt), Vite, strict TypeScript, Bulma/Tailwind. Owns the generalist skills.
- Specialist subagents, one per domain: `code-reviewer`, `seo-expert`, `ux-ui-expert`, `accessibility-expert`, `documentation-updater`, `security-expert`.
- Skills: `code-review`, `frontend-accessibility`, `performance-optimizer`, `security-audit` (with `references/checklist.md`), `seo-audit`, `systematic-debugging`, `update-documentation`, `web-design`, `website-analyzer` (with stdlib-only `scripts/fetch_site.py` scanner), plus on-demand framework skills `astro-expert`, `bulma-expert`, `vue-expert`, `nuxt-expert`.
- Slash commands: `/doc-compress` (compress memory files, original backed up as `FILE.original.md`) and `/scaffold-frontend-project` (`pnpm` only, 3-page starter site).
- `opencode.jsonc` configuration: `web-developer` as default agent, `rules/clean-code.md` injected as session instruction, `gh_grep` remote MCP server.
- Approval-gated permission model: every agent proposes edits first and applies them only after explicit user approval (`effect: ask`).
- Workspace sandboxing for all agents: `external_directory: deny` blocks access outside the project.
- Generic, portable paths throughout the instruction set (relative references, no machine-specific paths).
- MIT license.
- Project documentation: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`.

### Changed

- Framework conventions no longer auto-injected as rules: `rules/astro.md` and `rules/bulma.md` removed; content moved into on-demand skills `astro-expert` and `bulma-expert`, plus new `vue-expert` and `nuxt-expert` skills loaded per-project.

### Removed

- `rules/astro.md` and `rules/bulma.md` (replaced by on-demand skills).

### Security

- Shell commands are now approval-gated in every agent (`shell: ask` by default). Previously no `shell` rule existed, so under OpenCode V2's permissive defaults terminal commands ran without confirmation and could modify or delete files, bypassing the `edit: ask` gate. Exact read-only commands stay allowed; `rm -rf`, `git push` and `git reset --hard` are denied.
- `service.json` (plaintext password of the local OpenCode service) added to `.gitignore` to prevent accidental commits to the repository.
