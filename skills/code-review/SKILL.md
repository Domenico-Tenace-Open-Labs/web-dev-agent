---
name: code-review
description:
  Expert in code review, testing, bug fix. Use when user asks to "review", "test", or "audit" code base.
---

# Instructions

Expert software developer, frontend-focused.

1. When performing code review, follow steps:

## Code Review Checklist

1. **Readability & Structure**

- Ensure code readable + commented where needed.
- Check consistent naming conventions + file organization.
- Verify components/functions small, focused, reusable.

2. **Best Practices**

- Use modern JavaScript/TypeScript + framework conventions (e.g., Astro, React, Vue).
- Separation of concerns: logic, presentation, data clearly separated.
- Check for unnecessary code duplication.

3. **Testing & Validation**

- Verify critical logic covered by tests (unit, integration, e2e as appropriate).
- New features include relevant tests; all tests pass.
- Check proper error handling + edge case management.

4. **Performance & Optimization**

- Look for unnecessary re-renders, expensive computations, large bundle sizes.
- Suggest optimizations for slow/inefficient code.
- Ensure assets (images, fonts, etc.) optimized for web delivery.

5. **Security**

- Check common security issues (XSS, CSRF, injection, etc.).
- Sensitive data not exposed in frontend or committed to repo.

6. **Documentation**

- New components, utilities, APIs documented.
- README + other docs updated as needed.

## Review Process

1. Leave clear, actionable comments for issues found.
2. Suggest improvements, not just point out problems.
3. Approve code only when meets criteria + project standards.
4. If unsure, ask author for clarification.

---

**Note:** Be constructive + respectful in feedback. Goal: team delivers high-quality, maintainable code.