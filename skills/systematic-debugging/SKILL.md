---
name: systematic-debugging
description:
  Root-cause analysis + bug fixing. Use when user reports bug, error, crash, unexpected behavior, failing test, or asks "debug", "fix this", "why is this happening", "investigate this issue".
---

# Instructions

## When to use it

Fixing bugs, errors, unexpected behavior, failing tests. Not for new code.

## Why it matters

Without guidance, agents default to: read stack trace, spot suspicious line, change, hope. Sometimes works. Often fixes symptom not cause, or adds new bug. This skill slows that reflex, follows experienced developer path.

## The process

### 1. Reproduce the problem before touching anything

Can't reproduce reliably = guessing, not debugging. Find minimal triggering case. Intermittent: find what differs between passing/failing runs (input, timing, prior state).

Vague report ("it breaks sometimes"): turn into reproducible case first, don't poke code randomly.

### 2. Isolate the cause before proposing a fix

Reproduced? Narrow it down:

- **Bisection**: suspect recent change? Check git history, find which commit introduced bug.
- **Targeted logging**: logs/breakpoints at key flow points, not everywhere. Find where state diverges from expected.
- **Shrink the problem**: bug in complex flow? Isolate in simpler scenario (standalone script, minimal unit test).

No fix without clear theory of why. "I changed this line and error went away" = luck, not explanation.

### 3. Tell the symptom apart from the cause

Before fixing, ask: fix cause or hide symptom? Classic: `null` crashes downstream. Adding `if (x !== null)` removes crash, but if `x` should never be `null` there, real bug is upstream where `x` is produced.

Real cause too risky to fix now? Temporary mitigation OK, but flag clearly (code comment or PR note), don't pass off as final solution.

### 4. Verify the fix, not just the case you reproduced

After fix:
- Confirm original case works.
- Check nearby cases not broken (similar edge cases, alternate paths).
- Run test suite if exists. No test covering this bug? Add one — best prevention against regression.

### 5. Explain what happened

When presenting fix, include:
- Expected vs observed behavior.
- Actual root cause (not just "I changed X").
- Why fix addresses cause, not symptom.
- Remaining risks or uncovered cases.

Not bureaucracy — lets reviewer trust change without redoing investigation.

## Things to avoid

- Don't trial-and-error code changes hoping error disappears.
- Don't ignore warnings/side errors during investigation — sometimes clue to real cause.
- Don't mark resolved if main test passes but side effects unchecked.
- Don't refactor while hunting bug. Isolate + fix first, refactor separately if needed.