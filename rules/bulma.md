# bulma.md

## Overview

Global rules + conventions Bulma CSS. Template-agnostic: any markup (Astro, plain HTML, React, Vue, etc.). Pair with framework rules file (e.g. `astro.md`), no duplication.

## Core Principle

Use Bulma as intended: utility classes on markup, no rewriting/overriding base components unless strictly necessary. Before custom CSS, check Bulma covers it.

## Customization

Bulma customization **only via CSS/SASS variables**, never direct class overrides.

Overrides in one dedicated file, path per project structure (e.g. `styles/bulma-overrides.scss`):

```scss
// styles/bulma-overrides.scss
@use "bulma/sass" with (
  $primary: #your-color,
  $family-sans-serif: '"Your Font", sans-serif'
);
```

No `!important` for conflicts — fix specificity upstream.

## Custom Classes

Bulma genuinely insufficient:

- Naming **kebab-case**: `.card-featured`, `.hero-compact`
- Project prefix avoid collisions: `.ag-card-featured` (`ag` = Antigravity)
- Custom classes separate files from Bulma, never mixed same block

## Responsive

Bulma breakpoints + helpers default: use `.is-hidden-mobile`, `.is-flex-desktop`, etc. No custom media queries when Bulma covers case. Custom breakpoint truly required → document next to component/stylesheet using it.

## Columns

Bulma column system (`columns` + `column`) layout backbone. Use it. Avoid raw flexbox/grid when Bulma can do job — unless design explicitly requires.

---

## PR Checklist

- [ ] No Bulma overrides via direct class rewrites
- [ ] Customization via CSS/SASS variables
- [ ] No `!important` for conflicts
- [ ] Custom classes kebab-case, project-prefixed
- [ ] Bulma helpers instead custom media queries where possible
- [ ] Custom CSS dedicated files, not mixed Bulma blocks
