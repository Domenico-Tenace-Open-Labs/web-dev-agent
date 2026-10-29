# clean-code.md

## Overview

Global, language-agnostic clean-code baseline. Applies every file any agent writes/edits, any stack.

Precedence: project conventions (`AGENTS.md`, linter config, existing code style) win **only** when stricter. Doubt → this file wins.

**Prime directive:** write code tired engineer can read at 3am and change in 6 months. Boring beats clever.

---

## 1. Naming

- Intention-revealing, pronounceable, searchable. `getUserById`, not `getData`.
- Booleans read yes/no: `isActive`, `hasPermission`, `canEdit`.
- Functions start verb; no vague `handle`, `process`, `manage`.
- No abbreviations except domain-standard (`id`, `url`, `http`). No single letters except loop indices.
- Magic numbers/strings → named constants.
- Follow language casing: `camelCase` values, `PascalCase` types, `SCREAMING_SNAKE_CASE` constants. Let linter decide.
- Name no longer matches behavior = bug: rename in same change.

## 2. Functions & modules

- One function, one reason to change, one abstraction level.
- Aim <25 lines; needs scrolling → split.
- Guard clauses over nested `if/else`; no `else` after `return`; nesting depth ≤3.
- Max ~3 parameters. More → options object.
- Boolean flag params switching behavior → split into two functions.
- Prefer pure functions; push side effects to edges, name them (`sendEmail`, `saveOrder`).
- Command/query separation: mutate or return data, not both.
- Modules expose smallest public surface; keep internals private.
- Delete dead code. Git remembers it.

## 3. Comments & documentation

- Comment **why**, not **what**. Code already says what.
- Document non-obvious context: business rules, invariants, workarounds, decisions that look wrong but aren't.
- No commented-out code, changelog comments, author tags.
- Public/non-trivial API → short docstring: purpose, params, returns, errors.
- `TODO` only as `// TODO(owner): reason` — never substitute for finishing work.
- Stale comment worse than no comment. Update or delete with code.

## 4. Error handling

- Fail fast, loud, with context.
- Never swallow errors: no empty `catch`, no catch-log-continue.
- Errors answer: what failed, which inputs (never secrets/PII), what caused it.
- No silent `null`/`undefined`: absence explicit in type, handle at call site.
- Validate at system boundaries; reject with actionable message.
- No exceptions for control flow.
- Always release resources (`try/finally`, `defer`, `using`, context managers).
- Internal details → logs; users get safe, useful message.

## 5. Types & input validation

- No `any`/implicit `any` in public APIs. Use `unknown`, narrow.
- Validate every external input (HTTP, CLI, DB, queue, file) with schema library.
- Client validation = UX. Server validation = security. Never trust client.
- Model domain in types: unions/enums over stringly-typed values, branded IDs over raw strings.
- Casts and non-null assertions require proven, commented invariant.
- Design null/empty/zero cases deliberately; don't leak through.

## 6. Data, state, side effects

- `const` default; mutate only intentional, local.
- State local as possible; lift only when shared. No global mutable state.
- One source of truth; derive secondary state, don't duplicate.
- Dependencies explicit (arguments/DI), never hidden singletons or module-level I/O.
- Handle promise rejections and cancellation. No floating promises.
- Retryable writes (payments, webhooks, queues) must be idempotent.

## 7. Architecture & boundaries

- Separate presentation, business logic, data access. UI no business rules; controllers no SQL; domain logic framework-agnostic.
- Organize by feature/domain past trivial size.
- Dependencies point inward. No cycles — two modules needing each other = missing abstraction.
- Cross module boundaries only through contracts; don't reach internals.
- Wrap multi-step writes in transaction.
- Config from env/config files, validated at startup. Never hardcoded per environment.
- No premature abstraction: wait third repetition.

## 8. Security baseline (non-negotiable)

- No secrets in code, VCS, logs. Env vars or secrets manager.
- Parameterized queries only. Never concatenate SQL or shell commands.
- Escape output per context (HTML, attribute, URL, JS).
- Hash passwords with bcrypt/argon2. Never roll own crypto.
- Authorize server-side every request; least privilege everywhere.
- Rate-limit public endpoints; validate upload size/type.
- Logs carry request/correlation id, never tokens, passwords, PII.
- Audit dependencies; commit lockfile.

## 9. Testing

- Test **behavior**, not implementation. Tests survive refactor.
- Pyramid: many fast unit tests, fewer integration, minimal E2E.
- Every bug fix ships regression test.
- Cover edge cases: empty, null, boundary, duplicate, unauthorized, timeout.
- Tests deterministic, independent, fast. No sleeps or real network in unit tests.
- Mock external deps in unit tests; real deps (or containers) in integration.
- Flaky test fixed or deleted — never ignored.
- Test name states behavior + condition. Arrange / act / assert.
- Don't chase 100%; cover logic that can break.

## 10. Performance

- Correct and clear first. Profile before optimizing.
- No N+1: batch or eager-load. Index only queried columns.
- Avoid needless re-renders/recomputation; memoize where measured.
- Lazy-load routes/heavy components; ship responsive, optimized images.
- Paginate or stream large datasets; bound memory.
- Cache with explicit invalidation; never cache secrets.
- Claiming improvement → state measured number.

## 11. Dependencies

- Prefer mainstream, maintained libs. Justify every addition.
- No dependency for few clear lines.
- Check license, maintenance, known vulns, bundle/runtime cost.
- Read breaking changes before major upgrades. Never blind-bump.
- Lockfile committed; installs reproducible.

## 12. Git & delivery

- One logical change per commit/PR. Imperative subject: `Add user validation`.
- Never commit secrets, `.env`, `node_modules`, build artifacts, generated files.
- Don't reformat unrelated files in feature change.
- Explain non-obvious decisions in commit/PR body.
- Run lint, format, typecheck, tests before declaring done.

## 13. Definition of done

- [ ] Matches project structure and conventions
- [ ] Names reveal intent; no magic values
- [ ] Functions small, single-purpose, early-returned
- [ ] External input validated at boundary
- [ ] Errors handled with context; no swallowing
- [ ] No dead code, commented-out code, debug logs
- [ ] Edge cases covered by tests; suite green
- [ ] Lint/format/typecheck clean
- [ ] No secrets, no sensitive data in logs
- [ ] Docs/README updated if behavior or setup changed

## 14. Red flags — reject these

- `utils.ts` / `helpers.ts` dumping grounds
- God objects, 500-line components, deep nesting
- Copy-paste duplication kept "for speed"
- `any`, unvalidated input, unchecked casts
- Empty `catch`, swallowed promise rejections
- Magic numbers, stringly-typed states
- Global mutable state, hidden I/O
- N+1 queries in loops
- Bug fix without test
- Commented-out code, stale comments
