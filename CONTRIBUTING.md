# Contributing

Thanks for considering contributing to Web Dev Agent.

This project is an [OpenCode](https://opencode.ai) global configuration pack, agents, skills, slash commands, and rules. It is not a traditional codebase: there is no build step, no test suite, and no runtime to run. Contributions are mostly content: instructions, conventions, and configuration.

Before you start, read [`AGENTS.md`](AGENTS.md) and the rules in [`rules/`](rules/), they define the conventions this pack enforces, and contributions should follow them.

## Ground rules

- **English only** for documentation and instruction content.
- **Generic by design**: use relative paths (e.g. `rules/astro.md`). Never add machine- or user-specific paths (`~/.config/opencode`, `/home/...`, absolute paths).
- **Keep `description` frontmatter sharp** in agents and skills: OpenCode selects them based on that text. A vague description means the skill or agent never gets selected.
- **Follow the project conventions** in `rules/clean-code.md`, `rules/astro.md`, and `rules/bulma.md` when editing instruction content.
- **No secrets**: never commit `service.json`, `.env`, credentials, tokens, or private URLs. `service.json` (plaintext password of the local OpenCode service) is gitignored, never add it manually, never echo its contents.
- **Propose, then apply**: the whole pack is built around approval-gated edits. When suggesting changes, describe what and why before expecting them applied.

## What to contribute

- New or improved agents and skills.
- New slash commands.
- Rule improvements and bug fixes to existing instructions.
- Documentation fixes and improvements (README, guides, inline notes).
- Usage examples and tutorials.

## Getting started (GitHub flow)

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/my-change`.
3. Make your changes, following the ground rules above.
4. Commit with a clear, imperative message (e.g. "Add accessibility audit skill").
5. Push the branch and open a pull request describing the change.

## Pull request checklist

- [ ] Only relevant files changed; no formatting churn.
- [ ] `description` frontmatter updated whenever a skill/agent's trigger behavior changed.
- [ ] No machine-specific or absolute paths added, relative paths only.
- [ ] Markdown intact: lists, tables, code fences, and heading hierarchy.
- [ ] User-visible changes documented under `[Unreleased]` in `CHANGELOG.md` (a new feature → `Added`).
- [ ] No secrets, debug leftovers, or commented-out content.
- [ ] Terminology and style consistent with the rest of the pack.

## Review

Maintainers review pull requests constructively; be open to feedback and clarification requests. Smaller, focused pull requests are reviewed faster than large unrelated changes.

## Questions

Open a discussion or issue with a clear question, or ask the maintainers before making a large change.
