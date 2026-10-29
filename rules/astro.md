# astro.md

## Overview

Global rules + conventions Astro projects. Styling-agnostic: pair with rules file of CSS solution in use (e.g. `bulma.md`), no duplication.

## Project Structure

```
project-root/
├── public/
│   └── images/          /* Statically served images */
├── src/
│   ├── assets/          /* Fonts, SVGs, images imported via bundle */
│   ├── components/      /* Reusable Astro components */
│   ├── data/            /* JSON/TS files with static data or mocks */
│   ├── layouts/         /* Base layouts and page templates */
│   └── pages/           /* Site pages and routes */
├── package.json
├── astro.config.mjs
└── README.md
```

### Structure Rules

**`public/images/`** — Only assets not going through bundler: images referenced directly by URL in markup/meta tags (`og:image`, favicon, etc.). Images used inside Astro components go in `src/assets/`.

**`src/assets/`** — Everything Vite must process: images imported inside components, inline SVGs, local fonts. Astro optimizes images imported here.

**`src/components/`** — Reusable `.astro` components. Page-specific components next to page or dedicated subfolder. As project grows, organize by domain (e.g. `components/nav/`, `components/cards/`).

**`src/data/`** — Static data, content config, mocks: `.json`/`.ts` files export arrays/objects for pages. No logic, just data.

**`src/layouts/`** — Layouts wrap pages. At minimum `BaseLayout.astro` with `<head>`, metadata, base HTML. One layout per site section when needed (e.g. `BlogLayout.astro`, `LandingLayout.astro`).

**`src/pages/`** — Site pages; folder structure maps to routes. No complex presentation logic: pages assemble layouts + components, don't define them.

---

## Conventions

### Naming

- Component files **PascalCase**: `HeroSection.astro`, `NavBar.astro`, `CardGrid.astro`
- Page files **kebab-case**: `about-us.astro`, `contact.astro`
- Layouts **PascalCase** with `Layout` suffix: `BaseLayout.astro`, `ArticleLayout.astro`
- Files in `src/data/` **kebab-case**: `team-members.json`, `services.ts`

### Components

Each component one job. `.astro` over 150 lines = split.

Props always typed TypeScript in frontmatter:

```astro
---
interface Props {
  title: string;
  description?: string;
  variant?: 'primary' | 'secondary';
}

const { title, description, variant = 'primary' } = Astro.props;
---
```

No `any`. Type unclear → `unknown` almost always right.

### Frontmatter

Imports first, then props, then logic. No large logic blocks — complex logic → `.ts` file in `src/data/` or utility module.

### Slots

`<slot />` for main content, named slots for specific areas (header, footer, etc.). Document non-obvious slots with comment inside component.

---

## PR Checklist

- [ ] Project structure matches this file
- [ ] No leftover `console.log`
- [ ] Component props typed, no `any`
- [ ] Components under 150 lines, or split
- [ ] Images in components `src/assets/`; static `public/images/`
- [ ] README updated when features/structure change
