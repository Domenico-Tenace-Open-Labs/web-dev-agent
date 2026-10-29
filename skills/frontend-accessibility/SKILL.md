---
name: frontend-accessibility
description: Analyze a frontend codebase for accessibility issues and implement verified improvements across UI components, pages, styles, forms, navigation, media, and interaction patterns.
---

# Frontend Accessibility

## Purpose

Analyze + improve frontend codebase accessibility. Interfaces usable with:

- Screen readers.
- Keyboard-only navigation.
- Voice control.
- Switch devices.
- Screen magnification.
- Reduced-motion preferences.
- High-contrast or forced-colors settings.
- Different zoom levels and viewport sizes.
- Users with cognitive, visual, auditory, or motor disabilities.

Use when user asks to:

- Audit frontend accessibility.
- Fix accessibility issues.
- Improve WCAG compliance.
- Make component or page accessible.
- Add keyboard navigation.
- Improve screen-reader support.
- Fix color contrast, focus, forms, modals, menus, tables, media, or semantic HTML.
- Review accessibility regressions.
- Add automated accessibility tests.
- Prepare accessibility remediation plan.

Focus: frontend code + user-facing behavior. No legal/certification claims unless user explicitly requests qualified assessment with supporting evidence.

## Accessibility Baseline

Use project's stated accessibility target when exists.

If none specified, use as practical baseline:

- WCAG 2.2 Level AA principles.
- Semantic HTML before ARIA.
- Complete keyboard operability.
- Visible and predictable focus.
- Meaningful accessible names and descriptions.
- Sufficient color contrast.
- Support for zoom and responsive layouts.
- Respect for user preferences (reduced motion).
- Clear form instructions, errors, and status messages.
- Compatibility with common assistive technologies.

No WCAG conformance claim from code review or automated test alone. Accessibility requires testing with real assistive technologies + representative users.

## Core Principles

1. **Inspect before editing.**
   Understand framework, component architecture, design system, routing, styling conventions, test setup.

2. **Prefer native HTML.**
   Use native controls (`button`, `a`, `input`, `select`, `textarea`, `dialog`) + semantic landmarks before adding ARIA.

3. **Use ARIA only when necessary.**
   ARIA must accurately reflect behavior + state. Do not use ARIA to compensate for incorrect semantics when native HTML suffices.

4. **Fix behavior, not only markup.**
   Element not accessible merely because it has role, label, or `tabIndex`. Verify interaction, focus, state changes, announcements.

5. **Preserve existing functionality.**
   Accessibility improvements must not break visual behavior, routing, form submission, responsive layouts, or supported browsers.

6. **Avoid unnecessary changes.**
   Make focused, reviewable changes. Do not refactor unrelated code during accessibility fix.

7. **Treat visible focus as required.**
   Never remove focus indicators without equally visible replacement.

8. **Do not rely on color alone.**
   Convey meaning using text, icons with accessible names, patterns, structure, non-color indicators.

9. **Test both automated and manually observable behavior.**
   Automated tools catch only subset of problems.

10. **Document limitations honestly.**
    Record what was checked, what could not be checked, which issues need manual assistive-technology testing.

## Required Workflow

### 1. Establish Repository Context

Inspect repository before making changes.

Identify:

- Frontend framework and version.
- Rendering model: client-side, server-side, static, or hybrid.
- Component library and design system.
- Styling approach.
- Routing solution.
- Form and validation libraries.
- State-management approach.
- Existing accessibility utilities.
- Test frameworks and scripts.
- End-to-end testing setup.
- Linting and formatting rules.
- Browser support targets.
- Existing accessibility documentation and policies.

Look for:

- `package.json`
- `pnpm-lock.yaml`
- `yarn.lock`
- `package-lock.json`
- `vite.config.*`
- `next.config.*`
- `nuxt.config.*`
- `angular.json`
- `astro.config.*`
- `src/`
- `app/`
- `pages/`
- `components/`
- `tests/`
- `e2e/`
- `playwright.config.*`
- `cypress.config.*`
- `eslint.config.*`
- `.storybook/`
- `storybook/`

Do not assume framework, directory, or testing tool exists. Discover first.

### 2. Understand the Request

Translate request into concrete accessibility tasks.

Determine:

- Which pages, components, flows, or user journeys are in scope.
- Whether request concerns specific WCAG criterion.
- Whether goal is analysis only or implementation.
- Which users or assistive technologies are relevant.
- Whether visual design changes are allowed.
- Whether new dependencies may be added.
- Whether accessibility tests are expected.
- Whether change is bug fix, audit, refactor, or release requirement.

If scope unclear, inspect code and identify smallest useful scope before asking questions.

### 3. Map the User Interface

Identify key user journeys and interactive surfaces:

- Application shell.
- Header and navigation.
- Main content and landmarks.
- Sidebars and menus.
- Search.
- Authentication flows.
- Forms and validation.
- Dialogs and drawers.
- Tabs, accordions, carousels, and disclosures.
- Data tables.
- Lists and virtualized content.
- Tooltips and popovers.
- Toasts and live regions.
- Loading, empty, and error states.
- Drag-and-drop or sortable interfaces.
- Media players.
- Infinite scrolling and pagination.
- Custom controls.
- Mobile-specific interactions.

Prioritize critical flows + shared components. Defect in shared component may affect entire application.

### 4. Perform a Static Accessibility Review

Inspect implementation for following categories.

#### 4.1 Document Structure and Semantics

Check for:

- Meaningful page title.
- Logical heading hierarchy.
- One clear primary page heading where appropriate.
- Semantic landmarks (`header`, `nav`, `main`, `aside`, `footer`).
- Correct list, table, and section semantics.
- Appropriate use of buttons versus links.
- Avoidance of clickable non-interactive elements.
- Decorative elements hidden from assistive technology.
- Appropriate language declarations.
- Skip link or equivalent bypass mechanism where useful.
- Duplicate or ambiguous landmark names.

Do not add landmarks or headings solely to satisfy checklist. Must reflect actual content structure.

#### 4.2 Keyboard Accessibility

Check that:

- All interactive functionality is available by keyboard.
- Interactive elements reachable in logical order.
- No keyboard trap exists.
- Custom controls support expected keys.
- Menus, dialogs, tabs, accordions, carousels implement appropriate keyboard behavior.
- Focus moves predictably when UI state changes.
- Focus restored appropriately when overlays close.
- Disabled or unavailable controls behave consistently.
- No positive `tabIndex` values used without strong, documented reason.
- Hover-only functionality has accessible equivalent.
- Drag-and-drop has keyboard-accessible alternative.

#### 4.3 Focus Management

Check for:

- Visible focus indicator.
- Sufficient focus contrast against adjacent colors.
- Focus styles not clipped or hidden.
- Correct focus placement when opening dialogs or menus.
- Focus trapping only where appropriate (especially modal dialogs).
- Focus restoration after closing overlays.
- Focus behavior after route changes.
- Focus behavior after dynamically inserting content.
- Avoidance of unexpected focus stealing.

Focus management must match interaction model. Must not disorient users.

#### 4.4 Names, Roles, and States

Check that controls have:

- Programmatically determinable role.
- Accessible name.
- State reflecting current UI state.
- Accessible description when additional context necessary.
- Correct relationships between labels, controls, descriptions, errors.

Review relevant attributes:

- `aria-label`
- `aria-labelledby`
- `aria-describedby`
- `aria-controls`
- `aria-expanded`
- `aria-pressed`
- `aria-selected`
- `aria-current`
- `aria-disabled`
- `aria-invalid`
- `aria-live`
- `aria-modal`
- `aria-hidden`

No redundant accessible names that make screen-reader output verbose or confusing.

#### 4.5 Forms

Check that forms provide:

- Explicit labels for all controls.
- Correct label-control associations.
- Instructions before input when needed.
- Clearly identified required fields.
- Correct input types and autocomplete tokens.
- Useful constraints and input modes.
- Inline validation understandable without relying on color.
- Programmatic association between errors and fields.
- Summary for multiple errors when appropriate.
- Error focus or announcement behavior that does not disorient users.
- Preservation of entered values after validation failures.
- Accessible status for asynchronous validation.

No placeholder text as only label or instruction.

#### 4.6 Images and Non-Text Content

Check that:

- Informative images have concise, meaningful alternative text.
- Decorative images use empty alternative text or hidden appropriately.
- Functional images describe action, not only visual.
- Complex images have appropriate long description or nearby explanation.
- SVGs have accessible name when they convey meaning.
- Icons used as controls have accessible names.
- Icon-only controls have visible or programmatic context.
- Images do not contain essential text without accessible equivalent.

No alt text that repeats nearby visible text unnecessarily.

#### 4.7 Color, Contrast, and Visual Presentation

Check for:

- Text contrast.
- Non-text contrast for controls, focus indicators, meaningful graphical objects.
- Error, success, warning, selected states that do not rely only on color.
- Readability at increased text spacing.
- Content usable at high zoom.
- Layouts that do not require two-dimensional scrolling for ordinary content.
- Text not unintentionally truncated.
- Sufficient target size and spacing for controls.
- Compatibility with forced-colors or high-contrast modes where relevant.

Use project's design tokens when available. No arbitrary colors that conflict with design system.

#### 4.8 Responsive and Zoom Behavior

Test or inspect behavior at:

- Small mobile widths.
- Large desktop widths.
- Increased browser zoom.
- Text-only zoom when applicable.
- Different text lengths.
- Large system fonts.
- Portrait and landscape orientations.
- Reduced available height.

Check for:

- Clipped content.
- Hidden controls.
- Overlapping dialogs.
- Unreachable horizontal content.
- Broken focus indicators.
- Menus that cannot be operated on small screens.
- Sticky elements obscuring focused content.

#### 4.9 Motion and Timing

Check for:

- Respect for `prefers-reduced-motion`.
- Avoidance of unnecessary animation.
- User controls for pausing, stopping, or hiding moving content where applicable.
- No flashing that could create risk.
- Sufficient time to read or complete timed interactions.
- Avoidance of auto-advancing content without controls.
- Reduced-motion behavior for route transitions, modals, carousels, loading states.

Reduced-motion implementation must preserve meaning + usability, not simply remove all feedback.

#### 4.10 Dynamic Content and Announcements

Check that:

- Loading states communicated appropriately.
- Async success and error messages announced when necessary.
- Live regions used sparingly.
- Updates do not interrupt users unnecessarily.
- Toasts accessible and persist long enough to be consumed.
- Newly rendered content has logical reading and focus order.
- Infinite scrolling has alternative (pagination or load-more control).
- Route changes provide appropriate page title and focus context.

No large or frequently changing regions in assertive live regions.

#### 4.11 Tables and Data-Dense Interfaces

Check that:

- Tabular data uses table semantics.
- Header cells correctly associated.
- Captions or accessible names provided where needed.
- Sortable columns expose their state.
- Responsive table behavior remains understandable.
- Data not communicated only through visual position or color.
- Virtualized tables preserve appropriate semantics and keyboard access.

#### 4.12 Media

Check that media provides, where relevant:

- Captions.
- Transcripts.
- Audio descriptions.
- Keyboard-accessible controls.
- Visible and programmatic names for controls.
- Pause, stop, and volume controls.
- Non-visual alternative for essential information.

No assumption browser-native media controls meet every project requirement.

### 5. Analyze Shared Components and Abstractions

Pay special attention to shared components:

- Buttons.
- Links.
- Form fields.
- Inputs.
- Selects.
- Dialogs.
- Menus.
- Tabs.
- Accordions.
- Tooltips.
- Alerts.
- Toasts.
- Tables.
- Icons.
- Layout primitives.

Determine whether accessibility behavior is implemented:

- In shared component.
- In individual consumers.
- Through third-party library.
- Through design-system contract.
- Through browser-native behavior.

Fix at lowest appropriate shared layer when safely improves all consumers. Avoid making shared component more restrictive if existing consumers depend on documented behavior.

### 6. Review Existing Tests and Tooling

Inspect existing accessibility coverage:

- Unit tests.
- Component tests.
- Storybook stories.
- Playwright or Cypress tests.
- Axe or equivalent scans.
- ESLint accessibility rules.
- Visual regression tests.
- Manual testing checklists.
- CI accessibility checks.

Use existing tooling + conventions when possible.

Passing automated scan is not proof of full accessibility. Automated tools commonly miss:

- Poor interaction design.
- Incorrect focus movement.
- Inadequate keyboard behavior.
- Unclear wording.
- Poor screen-reader announcements.
- Missing context.
- Inaccessible dynamic workflows.
- Problems caused by real content.

### 7. Implement Fixes

Implement smallest complete solution.

Preferred approaches:

- Replace non-semantic clickable elements with native controls.
- Associate labels, descriptions, errors correctly.
- Add or repair keyboard behavior.
- Add visible focus styles.
- Correct heading and landmark structure.
- Add accessible names to controls.
- Repair dialog focus management.
- Respect reduced-motion preferences.
- Improve status and error announcements.
- Fix responsive and zoom behavior.
- Use native browser validation features where appropriate.
- Add accessible alternatives to pointer-only interactions.
- Remove incorrect or redundant ARIA.

Avoid:

- Adding `role="button"` to non-button when real `button` usable.
- Adding `tabIndex="0"` without implementing complete keyboard behavior.
- Hiding content from screen readers merely to silence test.
- Using `aria-label` to conceal missing visible labels.
- Making all content `aria-live`.
- Removing focus outlines.
- Solving contrast issues by changing colors without checking all states.
- Introducing keyboard shortcuts that conflict with assistive technology.
- Adding inaccessible custom widgets when native control sufficient.

### 8. Add or Update Tests

Add tests when repository has suitable infrastructure.

Tests may cover:

- Accessible names and roles.
- Label and error associations.
- Keyboard activation.
- Focus movement and restoration.
- Dialog behavior.
- Menu and disclosure state.
- Tab selection and navigation.
- Reduced-motion styles or behavior.
- Live-region updates.
- Basic automated accessibility scans.
- Critical user journeys.

Tests verify behavior, not merely presence of ARIA attributes.

No brittle tests dependent on implementation details when user-visible behavior testable instead.

### 9. Validate the Changes

Run most relevant available checks:

- Unit tests.
- Component tests.
- End-to-end tests.
- Accessibility scans.
- Linting.
- Type checking.
- Build commands.
- Storybook tests.
- Visual regression tests.
- Documentation or design-system checks.

Perform manual checks when applicable:

- Navigate changed flow with only keyboard.
- Confirm focus visible.
- Confirm dialogs and menus manage focus correctly.
- Test with browser zoom.
- Test with reduced motion.
- Inspect content with screen reader when available.
- Test at mobile and desktop viewport sizes.
- Verify error and loading states.
- Verify color is not only means of conveying information.

If screen reader or browser unavailable, state not tested.

### 10. Review the Diff

Before finishing:

- Inspect final diff.
- Confirm only relevant files changed.
- Remove accidental formatting churn.
- Verify visual behavior not unintentionally changed.
- Check ARIA attributes match actual behavior.
- Check keyboard interactions do not conflict with browser behavior.
- Check focus styles remain visible.
- Check tests validate meaningful behavior.
- Check no accessibility claim exceeds available evidence.

## Accessibility Issue Severity

Use following severity guidance unless project has own classification.

### Critical

Issues blocking access to essential content or functionality:

- Keyboard trap.
- Essential workflow unavailable without pointer.
- Modal that cannot be closed or exited by keyboard.
- Authentication or checkout inaccessible to assistive technology.
- Content or controls completely hidden from relevant user group.

### High

Issues significantly impairing use:

- Missing labels on important form controls.
- Incorrect focus management in dialogs or navigation.
- Unusable keyboard navigation.
- Severe contrast failures on primary content or controls.
- Errors that cannot be identified or corrected.

### Medium

Issues reducing usability but have workaround:

- Poor heading structure.
- Missing descriptions.
- Incomplete status announcements.
- Inconsistent focus styling.
- Incorrect but non-blocking ARIA state.

### Low

Issues with limited impact:

- Minor terminology inconsistencies.
- Redundant accessible descriptions.
- Non-critical decorative content handling.
- Small improvements to supporting documentation or examples.

Severity reflects user impact, not implementation complexity.

## Reporting Findings

When analyzing without implementing, report findings using table:

| Severity | Location | Issue | User impact | Recommended fix | Verification |
|---|---|---|---|---|---|

For each finding:

- Identify file and component.
- Describe user-facing problem.
- Explain which users may be affected.
- Reference WCAG criterion only when mapping reasonably supported.
- Provide concrete remediation.
- State how fix can be verified.
- Distinguish confirmed issues from items requiring manual testing.

No vague findings like "improve accessibility" without specific location + remediation.

## WCAG Mapping Guidance

Map to WCAG only when relationship clear. Examples:

- Missing form labels: WCAG 1.3.1 and 3.3.2 may be relevant.
- Missing keyboard operation: WCAG 2.1.1 may be relevant.
- Keyboard trap: WCAG 2.1.2 may be relevant.
- Missing visible focus: WCAG 2.4.7 or 2.4.11 may be relevant depending on issue.
- Missing page title: WCAG 2.4.2 may be relevant.
- Unclear link purpose: WCAG 2.4.4 may be relevant.
- Insufficient contrast: WCAG 1.4.3 or 1.4.11 may be relevant.
- Color-only communication: WCAG 1.4.1 may be relevant.
- Missing text alternatives: WCAG 1.1.1 may be relevant.
- Missing captions: WCAG 1.2.2 may be relevant.
- Unexpected context changes: WCAG 3.2.1 or 3.2.2 may be relevant.
- Missing error identification: WCAG 3.3.1 may be relevant.

No success criterion assignment when evidence insufficient. Mention relevant principle or user impact instead.

## Third-Party Components

When using third-party component:

1. Inspect its documented accessibility behavior.
2. Verify how it is configured in repository.
3. Check whether project wraps or overrides it.
4. Avoid duplicating functionality already correctly provided.
5. Document limitations that cannot be fixed at consumer level.
6. Consider upgrading or replacing dependency only when explicitly requested or clearly necessary.
7. Do not patch generated vendor files.

Third-party library accessibility claim is not proof that project's usage is accessible.

## Generated and Design-System Code

If components or styles are generated:

1. Identify source of truth.
2. Update source rather than generated output.
3. Regenerate artifacts only if repository conventions require it.
4. Review generated diff for unexpected changes.
5. Add or update design-system contract when shared accessibility behavior changes.

## Safety and Change Boundaries

Unless explicitly requested, do not:

- Change product behavior unrelated to accessibility.
- Redesign visual interface.
- Remove animations without considering their meaning and feedback.
- Add accessibility overlays or automatic remediation scripts as substitute for fixing UI.
- Claim legal compliance or certification.
- Claim compatibility with specific screen reader without testing it.
- Introduce new dependencies without checking project conventions.
- Modify backend behavior.
- Disable lint rules globally.
- Silence accessibility warnings without understanding and documenting reason.
- Remove content from accessibility tree merely to pass automated tests.
- Make destructive changes to user data or configuration.
- Discard existing user changes.

## Suggested Inspection Commands

Use commands appropriate for repository + environment. Examples:

```bash
pwd
find . -maxdepth 3 -type f | sort
git status --short
rg -n "aria-|role=|tabIndex|onKeyDown|onKeyUp|onClick|outline|focus|prefers-reduced-motion" src app pages components
rg -n "<img|<svg|<button|<a |<input|<select|<textarea|dialog|menu|tablist|tabpanel" src app pages components
rg -n "axe|jest-axe|accessibility|playwright|cypress|storybook" package.json .github src tests e2e
```

No destructive commands or commands that discard user changes.

## Final Response

After completing work, report:

1. Concise summary of analysis or fixes.
2. Files changed.
3. Accessibility areas addressed.
4. Tests and validation commands run.
5. Manual checks performed.
6. Tools or assistive technologies unavailable.
7. Remaining issues, limitations, or assumptions.
8. Findings requiring design, product, or specialist review.

Use format:

```text
## Accessibility work completed

- Fixed keyboard access for the account menu.
- Added an accessible name and description to the search form.
- Corrected dialog focus trapping and focus restoration.
- Added component tests for keyboard navigation and dialog behavior.

## Files changed

- `src/components/AccountMenu.tsx`
- `src/components/SearchForm.tsx`
- `src/components/Modal.tsx`
- `tests/accessibility/account-menu.spec.ts`

## Validation

- Ran: `npm test`
- Ran: `npm run lint`
- Ran: `npm run build`
- Ran: `npx playwright test`
- Manually checked keyboard navigation and browser zoom.

## Limitations

- A screen reader test was not performed because none was available.
- No formal WCAG conformance claim is made.
```

Final response must not claim accessibility check, screen-reader test, or validation performed unless actually performed.