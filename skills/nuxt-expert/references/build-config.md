# Config, Build & Deploy

## `nuxt.config.ts` — sane defaults

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // Nuxt version behavior — 3 vs 4 (see structure reference)
  compatibilityVersion: 4,           // Nuxt 4 defaults (or future: {...})

  devtools: { enabled: true },

  // TypeScript — strict, checked at build
  typescript: {
    strict: true,
    typeCheck: true                   // runs vue-tsc on build (slower but safer)
  },

  // Modules (ecosystem — pinia, sitemap, tailwind, content…)
  modules: ['@pinia/nuxt', '@nuxtjs/sitemap'],

  // Global CSS (processed by Vite)
  css: ['~/assets/css/main.css'],

  // Rendering per route (SSR/SSG/SPA/hybrid) — see rendering reference
  routeRules: {
    '/': { prerender: true },
    '/blog/**': { swr: 3600 }
  },

  // Runtime env access (never secrets in public)
  runtimeConfig: {
    apiSecret: process.env.API_SECRET,
    public: { apiBase: '/api' }
  },

  // Vite bundler config
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: { 'vendor': ['vue', 'pinia'] }
        }
      }
    }
  },

  // Nitro server engine
  nitro: {
    preset: 'node-server'            // or vercel, netlify, cloudflare-pages…
  }
})
```

## TypeScript

- `nuxi typecheck` validates types (requires `typescript` package)
- Auto `tsconfig` extends; keep `strict: true`
- Typed pages (experimental): `experimental: { typedPages: true }` — type-safe routes
- Server handler types: `defineEventHandler(async (event) => …)` fully inferred

## Modules ecosystem (principali)

| Module | Purpose |
|--------|---------|
| `@pinia/nuxt` | Pinia store integration |
| `@nuxtjs/tailwindcss` | Tailwind |
| `@nuxtjs/sitemap` | sitemap.xml + robots.txt |
| `@nuxt/content` | Content/markdown-driven sites |
| `@nuxtjs/i18n` | Internationalization (routing + SEO) |
| `@nuxt/image` | Optimized `<NuxtImg>` |
| `nuxt-auth-utils` | Session auth (H3-based) |
| `@nuxt/test-utils` | Vitest + e2e helpers |

Install via pnpm (project convention — never npm/yarn). Configure in `modules` array; check each module's docs for runtime adds.

## Environment variables

- `.env` → loaded automatically (`NUXT_PUBLIC_*` public, `NUXT_*` runtimeConfig)
- Never commit `.env`; never hardcode per-environment config outside env files
- Validate required env at startup (config validated at startup)

```typescript
// app/plugins/validate-env.ts
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  if (!config.public.apiBase) throw new Error('NUXT_PUBLIC_API_BASE is required')
})
```

## Build & verify

```bash
pnpm nuxt typecheck     # type check (vue-tsc)
pnpm nuxt build         # production build (Nitro — .output/)
pnpm nuxt dev           # dev server
pnpm nuxt analyze       # bundle analysis (nuxi analyze)
```

Before wrap-up (project convention): `nuxi typecheck` + `nuxt build` pass, no leftover `console.log`.

## Build optimization

- Route-based code splitting automatic; lazy-load heavy components (`<Lazy*>` / `defineAsyncComponent`)
- Manual chunks only after measuring — defaults usually fine
- `nitro.prerender` static routes; `routeRules.swr` caching dynamic routes at edge
- `nuxi analyze` before optimizing bundles

## Deployment

| Target | `nitro.preset` |
|--------|----------------|
| Node server / VPS | `node-server` |
| Vercel | `vercel` |
| Netlify | `netlify` |
| Cloudflare Pages | `cloudflare-pages` |
| AWS Lambda / ElastiCache | `aws-lambda`, `aws-amplify` |
| Static host (SSG only) | `static` (or `nitro.prerender` + static preset) |

Modern targets (serverless/edge with SWR caching): `vercel`, `netlify`, `cloudflare-pages` support incremental rendering via routeRules. Node server: set `compatibilityDate`/deploy `.output/server` with process manager (systemd, pm2) + proxy (Caddy, nginx).

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `modules: []` | Add ecosystem features |
| `runtimeConfig` + `NUXT_*` | Env access, no hardcoded secrets |
| `typescript: { strict, typeCheck }` | Build-time type safety |
| `routeRules` | Per-route rendering/caching |
| `nitro.preset` | Deployment target |
| `pnpm nuxt build` | Production build |
| `nuxi analyze` | Bundle analysis |