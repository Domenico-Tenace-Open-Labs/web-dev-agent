---
name: update-documentation
description: Analyze a codebase and update its documentation, including README files, changelogs, API documentation, inline comments, docstrings, configuration references, and usage examples.
---

# Update Documentation

## Purpose

Keep codebase docs accurate, consistent, discoverable, aligned with current implementation.

Use when user asks to:

- Update or improve docs.
- Sync docs with recent code changes.
- Review README.
- Update changelog.
- Add or improve code comments and docstrings.
- Document new features, APIs, config options, commands, or workflows.
- Identify and fix outdated, incomplete, or misleading docs.
- Prepare doc changes for release.

Prioritize factual accuracy over verbosity. Never document behavior not verifiable from repo.

## Documentation Scope

Inspect and update docs in these areas when relevant:

- `README.md` and localized README files.
- `CHANGELOG.md`, release notes, and migration guides.
- Markdown files in `docs/`, `documentation/`, or similar dirs.
- API documentation.
- Code comments and docstrings.
- CLI help text and command docs.
- Config reference documentation.
- Env var documentation.
- Install and setup instructions.
- Usage examples and tutorials.
- Architecture and design docs.
- Contributing guidelines.
- Examples and sample config files.
- Docs generated from source annotations.
- Links, references, badges, and version info.

Only modify files affected by requested change or containing demonstrably stale info.

## Core Principles

1. **Inspect before editing.**
   Understand repo structure, dev conventions, and existing doc style before changes.

2. **Use implementation as source of truth.**
   Verify documented behavior against actual code, tests, config, scripts, and command definitions.

3. **Make focused changes.**
   No unrelated rewrites, formatting churn, or broad restructuring unless requested.

4. **Preserve existing voice and structure.**
   Follow language, tone, heading hierarchy, terminology, and formatting conventions already used.

5. **Document user-visible behavior.**
   Prefer behavior, inputs, outputs, side effects, errors, config, and examples over impl details.

6. **Keep examples executable or realistic.**
   Examples must use valid commands, current APIs, correct paths, realistic values.

7. **Avoid duplication.**
   Link to canonical source instead of copying.

8. **Do not hide uncertainty.**
   State uncertainty and ask user instead of inventing details.

9. **Preserve intentional comments.**
   Keep comments explaining non-obvious constraints, compat decisions, security considerations, known trade-offs.

10. **Keep docs maintainable.**
    Prefer concise, structured docs easy to update as code evolves.

## Required Workflow

### 1. Establish Repository Context

Before editing, inspect:

- Repo root.
- Project type and primary languages.
- Package or build manifests.
- Existing doc files.
- Contribution and style guidelines.
- Git status and recent history, when available.
- Test and validation commands.
- CI configuration.
- Release and versioning conventions.

Useful files to inspect may include:

- `README.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `package.json`
- `pyproject.toml`
- `Cargo.toml`
- `go.mod`
- `pom.xml`
- `build.gradle`
- `Makefile`
- `Dockerfile`
- `.github/`
- `docs/`
- `src/`
- `lib/`
- `app/`
- `tests/`

Discover repo structure first. Don't assume files exist.

### 2. Understand the Requested Change

Map user request to concrete doc tasks.

Determine:

- Which behavior, feature, API, command, or workflow changed.
- Which users affected.
- Which doc files likely affected.
- Whether change needs changelog entry.
- Whether migration or upgrade instructions needed.
- Whether inline comments or docstrings need updating.
- Whether examples, screenshots, diagrams, or config references now stale.

If request ambiguous, inspect code and recent changes before asking.

### 3. Inspect the Relevant Implementation

Trace documented behavior to its implementation.

Inspect:

- Public functions, classes, modules, and endpoints.
- CLI commands and argument parsing.
- Config loading and defaults.
- Env vars.
- Error handling and exit codes.
- Auth and authorization behavior.
- Serialization and response formats.
- Feature flags.
- Database migrations.
- Build and deployment scripts.
- Tests and fixtures.
- Recent commits or diffs related to requested change.

Use tests as evidence of intended behavior. Don't assume tests cover every use case.

### 4. Search for Documentation Drift

Search for:

- References to renamed symbols.
- Removed commands or options.
- Outdated version numbers.
- Incorrect default values.
- Stale file paths.
- Broken or obsolete links.
- Examples that no longer match API.
- Config options no longer supported.
- Missing docs for new public behavior.
- Comments contradicting implementation.
- Duplicate or conflicting instructions.

Search globally for relevant identifiers, commands, option names, env vars, URLs, and version strings.

### 5. Create a Documentation Plan

Before editing, identify:

- Files to modify.
- Files to add, if needed.
- Files that should stay unchanged.
- Reason for each modification.
- Validation commands to run.

Keep plan proportional to request. Small code change may only need short changelog entry + one README update.

### 6. Edit Documentation

Apply smallest complete set of changes.

#### README and Guides

When updating README or guide:

- Keep intro concise and accurate.
- Verify install commands.
- Verify prerequisites and supported versions.
- Verify setup steps and config names.
- Verify command examples.
- Explain expected output where useful.
- Document common errors if relevant.
- Keep sections in logical order.
- Use consistent heading levels.
- Prefer relative links for repo-local files.
- Avoid embedding secrets or machine-specific paths.

#### Changelogs

Follow repo's existing changelog format.

When no format exists, use clear categories:

- Added
- Changed
- Fixed
- Deprecated
- Removed
- Security

Changelog entries should:

- Describe user-visible impact.
- Use project's existing tense and style.
- Avoid impl details unless relevant to users.
- Mention breaking changes explicitly.
- Include migration guidance when needed.
- Avoid claiming release version unless known.

Don't rewrite historical entries to improve style unless requested.

#### Comments and Docstrings

Add or update comments only when they improve understanding.

Good comments explain:

- Why non-obvious decision exists.
- Important invariants.
- Compatibility behavior.
- Security constraints.
- Performance trade-offs.
- Workarounds for external limitations.
- Preconditions and side effects.
- Public API behavior not obvious from signature.

Avoid comments that restate code.

For public APIs, document when relevant:

- Parameters.
- Return values.
- Exceptions or errors.
- Side effects.
- Threading or async behavior.
- Config requirements.
- Compatibility constraints.
- Examples.

Keep comments close to code they describe.

#### API Documentation

For public APIs, verify and document:

- Endpoint or function purpose.
- Method and path, when applicable.
- Auth requirements.
- Parameters and types.
- Required and optional fields.
- Default values.
- Return format.
- Error responses.
- Pagination, filtering, or sorting behavior.
- Rate limits or retries.
- Compatibility and deprecation status.
- Minimal valid examples.

Don't document internal impl details as public API guarantees unless project explicitly treats them as stable.

### 7. Validate the Changes

Run doc-specific validation when available:

- Markdown linting.
- Link checking.
- Doc builds.
- API doc generation.
- Example tests.
- CLI help verification.
- Repo-provided validation scripts.

Manual checks:

- Read every changed section from user perspective.
- Check heading hierarchy.
- Check links and anchors.
- Check code fences and syntax highlighting.
- Check command names and flags.
- Check env vars and defaults.
- Check version references.
- Check terminology consistency.
- Check examples match current interfaces.
- Check no secrets or private info added.

If validation can't run, explain why.

### 8. Review the Diff

Before finishing:

- Inspect final diff.
- Confirm only relevant files changed.
- Remove accidental formatting churn.
- Ensure no source code modified unless requested.
- Ensure docs don't contradict tests or implementation.
- Confirm changelog wording appropriate.
- Confirm comments explain intent, not restate code.
- Check for duplicated or conflicting instructions.

## Safety and Change Boundaries

Unless explicitly requested, do not:

- Change app behavior.
- Change public APIs.
- Rename code symbols.
- Modify tests to make docs pass.
- Rewrite entire README.
- Rewrite historical changelog entries.
- Add unsupported features to docs.
- Invent config options, defaults, or compat guarantees.
- Add deps solely for docs.
- Remove comments without understanding purpose.
- Include credentials, tokens, private URLs, or sensitive internal info.
- Update generated files manually when produced by documented generator.

If generated docs involved:

1. Identify source files.
2. Determine project's generation command.
3. Update source.
4. Regenerate output only if repo conventions require committed generated files.
5. Verify generated changes are limited and expected.

## Changelog Policy

Add changelog entry when change affects users, operators, devs consuming public API, or maintainers upgrading.

Usually add entry for:

- New features.
- Breaking changes.
- New or changed config.
- Changed CLI commands.
- Changed API behavior.
- Bug fixes with user-visible impact.
- Security fixes, following repo policy.
- Deprecations or removals.
- New supported platforms or runtimes.

Usually skip entry for:

- Purely internal refactoring.
- Comment-only changes.
- Formatting-only changes.
- Test-only changes.
- Doc typo fixes, unless project tracks them explicitly.

If user asks for doc updates but no release version, add unreleased entry only when consistent with project's changelog convention.

## Handling Ambiguity

Ask clarifying question when:

- Multiple incompatible interpretations plausible.
- Required behavior not verifiable from codebase.
- Release version required but unknown.
- Requested docs would expose sensitive info.
- Repo has conflicting doc conventions.
- Change would alter app behavior.
- User requests guarantee implementation doesn't support.

Otherwise, make smallest reasonable assumption, document only verifiable facts, mention assumption in final report.

## Suggested Inspection Commands

Use commands appropriate for repo and environment. Examples:

```bash
pwd
find . -maxdepth 2 -type f | sort
git status --short
git diff -- README.md CHANGELOG.md
git log -n 10 --oneline
rg -n "TODO|FIXME|deprecated|DEPRECATED" .
rg -n "COMMAND|OPTION|ENVIRONMENT_VARIABLE|PUBLIC_SYMBOL" .
```

Don't run destructive commands. Don't discard user changes.

## Final Response

After completing work, report:

1. Concise summary of doc updates.
2. Files changed.
3. Assumptions or unresolved questions.
4. Validation commands run.
5. Validation not run and reason.
6. Follow-up docs still useful.

Use concise format:

```text
## Documentation updated

- Updated `README.md` with the new configuration workflow.
- Added an unreleased entry to `CHANGELOG.md`.
- Updated the public API docstring in `src/example.py`.

## Validation

- Ran: `make docs`
- Ran: `markdownlint README.md`
- Manually verified command examples and internal links.

## Notes

- No application behavior was changed.
- The release version was not specified, so the changelog entry was added under `Unreleased`.
```

Final response must not claim docs validated if command not actually run.