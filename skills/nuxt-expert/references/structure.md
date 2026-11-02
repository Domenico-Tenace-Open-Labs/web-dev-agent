# Nuxt Structure & Auto-imports

## Nuxt 4 Project Structure (default)

```
my-nuxt-app/
├── app/                   # App source (Nuxt 4) — Nuxt 3 keeps these at root
│   ├── app.vue            # Root component
│   ├── components/        # Auto-imported components
│   │   ├── AppHeader.vue  # → <AppHeader>
│   │   └── base/
│   │       └── Button.vue # → <BaseButton>
│   ├── composables/       # Auto-imported composables
│   ├── layouts/           # Layout components
│   ├── middleware/        # Route middleware
│   ├── pages/             # File-based routing
│   ├── plugins/           # App plugins
│   └── utils/             # Auto-imported utilities
├── server/                # Nitro server (always at root)
│   ├── api/               # /api/* endpoints
│   ├── routes/            # Non-/api routes
│   ├── middleware/        # Server middleware
│   ├── utils/             # Server-only utilities
│   └── plugins/           # Nitro plugins
├── assets/                # Uncompiled assets (CSS, images)
├── public/                # Static files (served at /)
├── content/               # Nuxt Content (if used)
├── data/                  # Data files for defineAppConfig (optional)
├── nuxt.config.ts
├── tsconfig.json
└── package.json
```

Nuxt 3 structure identical but `app/` contents at project root (`pages/`, `components/`, etc. under root). Detect layout via `nuxt.config.ts`:

```typescript
// Nuxt 4 (default: compatibilityVersion 4 or app/ dir exists)
export default defineNuxtConfig({
  future: { compatibilityVersion: 4 }
})

// Nuxt 3 structure (old srcDir behavior)
export default defineNuxtConfig({
  srcDir: '.',
  dir: { app: 'app' }
})
```

## `~/` alias

- Nuxt 4: `~` + `@` → `app/` by default → `~/components/Button.vue`
- Nuxt 3: `~` + `@` → project root → same import path when files at root
- `~~` and `@@` → project root always

Use `~`/`@`, never relative paths, for app-to-app imports.

## Auto-imports

Nuxt auto-imports (no manual import needed):

| Directory | Auto-imports | Notes |
|-----------|--------------|-------|
| `app/composables/` | functions exported | namespaced by folder for multi-file dirs |
| `app/utils/` | functions exported | same rules |
| `app/components/` | Vue components | nested dirs → prefix; `~components/` for explicit |
| `app/pages/`, `app/layouts/`, `app/middleware/` | Nuxt conventions | handled by framework |
| Nuxt composables | `useState`, `useFetch`, `useRoute`, … | framework-provided |
| Vue APIs | `ref`, `computed`, `watch`, … (Nuxt ≥3) | default on; disable via `imports.vue: false` |

### Component auto-import rules

```text
app/components/
├── AppHeader.vue      → <AppHeader>
└── base/
    └── Button.vue     → <BaseButton>   (folder name becomes prefix)
```

Explicit import via `#components` (e.g. in a plugin):

```typescript
import { AppHeader } from '#components'
```

### Composables naming

Auto-imported composables must be called in Nuxt context (setup, plugins, middleware). Name `useXxx`, export function:

```typescript
// app/composables/useAuth.ts (auto-imported)
export const useAuth = () => {
  const user = useState<User | null>('user', () => null)
  return { user, isLoggedIn: computed(() => user.value !== null) }
}
```

## Directory conventions

- **`app/app.vue`** — root component; `<NuxtLayout>` + `<NuxtPage>` via `<NuxtPage />`
- **`app/pages/`** — file-based routes (see routing)
- **`app/layouts/`** — `default.vue` applies automatically; others via `definePageMeta({ layout })`
- **`app/middleware/`** — named middleware; run via `definePageMeta({ middleware })`, `router.options.ts`, or inline `defineNuxtRouteMiddleware` per-file (Nuxt 4 per-file = `definePageMeta({ middleware: 'name' })`)
- **`server/`** — Nitro handlers, only place for server-only code
- **`public/`** — static assets served as-is at `/`
- **`assets/`** — processed by bundler (CSS, images imported in components)

## Config basics

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  compatibilityVersion: 4,          // Nuxt 4 behavior
  devtools: { enabled: true },
  typescript: { strict: true, typeCheck: true },
  css: ['~/assets/css/main.css'],   // ~/ = app/ in Nuxt 4
  modules: ['@pinia/nuxt', '@nuxtjs/tailwindcss']
})
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `app/` (Nuxt 4) or root (Nuxt 3) | Where pages/components/composables live |
| `server/` | Nitro endpoints + server-only code |
| `~/` vs `~~/` | app dir vs project root |
| Auto-imported composables/components/utils | No manual imports needed |
| `#components` | Explicit component import outside templates |
| `nuxi init <name>` | Create new Nuxt project |