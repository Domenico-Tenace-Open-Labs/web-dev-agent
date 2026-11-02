---
name: nuxt-expert
description: Nuxt 4 / Nuxt 3 conventions — SSR/SSG/hybrid rendering via routeRules, app/ directory structure, useFetch/useAsyncData data fetching, file-based routing, layouts, Nitro server routes, runtimeConfig env. Load when the project uses Nuxt (nuxt.config.ts, app/ or root pages/ directory, server/ handlers); also for SEO meta, hydration, deployment tuning.
---

# Nuxt Expert

Senior Nuxt specialist, Vue.js meta-framework: SSR, SSG, hybrid rendering, Nitro server. *Structure derived from vue-expert skill (MIT).*

> Builds on Vue 3: pair with skill `vue-expert` for Composition API, components, Pinia. Pair with skill `bulma-expert` when project uses Bulma — no duplication.

## Core Workflow

1. **Analyze requirements** - render mode per route (SSR/SSG/SPA/hybrid), data needs, auth, SEO
2. **Design architecture** - app/ structure, pages, layouts, composables, Nitro routes
3. **Implement** - auto-imports, `useFetch`/`useAsyncData`, file-based routing
4. **Validate** - `nuxi typecheck` + `nuxt build`; verify SSR + hydration
5. **Optimize** - routeRules caching/rendering, payload extraction, lazy hydration, bundle analysis
6. **Test** - Vitest + `@nuxt/test-utils`; e2e Playwright

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Structure & auto-imports | `references/structure.md` | app/ vs root dirs, `~/` alias, srcDir, directory conventions |
| Pages, layouts, middleware | `references/routing.md` | File-based routing, dynamic routes, `definePageMeta`, guards |
| Data fetching | `references/data-fetching.md` | `useFetch`, `useAsyncData`, caching, refresh, payload |
| Rendering modes & hydration | `references/rendering.md` | SSR/SSG/SPA/hybrid, routeRules, hydration mismatch, `ClientOnly` |
| Nitro server | `references/server-nitro.md` | `server/api`, event handlers, runtimeConfig, cookies, caching |
| State | `references/state.md` | `useState`, Pinia integration, SSR-safe shared state |
| SEO & metadata | `references/head-seo.md` | `useHead`, `useSeoMeta`, Open Graph, canonical |
| Config, build & deploy | `references/build-config.md` | nuxt.config, TypeScript strict, modules, Vite tuning, nitro preset |

## Quick Example

Minimal Nuxt 4 page with SSR-safe data fetching + typed props:

```vue
<!-- app/pages/users/[id].vue (Nuxt 4) / pages/users/[id].vue (Nuxt 3) -->
<script setup lang="ts">
interface User {
  id: number
  name: string
  email: string
}

const route = useRoute()

// SSR-safe: fetched on server, reused for hydration, deduped by key
const { data: user, pending, error, refresh } = await useFetch<User>(`/api/users/${route.params.id}`)

useSeoMeta({
  title: () => `User: ${user.value?.name ?? 'Loading'}`,
  description: 'User profile page'
})
</script>

<template>
  <div>
    <div v-if="pending">Loading…</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="user">
      <h1>{{ user.name }}</h1>
      <a :href="`mailto:${user.email}`">{{ user.email }}</a>
      <button @click="refresh">Refresh</button>
    </div>
  </div>
</template>
```

## Constraints

### MUST DO

- `useFetch`/`useAsyncData` for data that must exist on server or survive hydration — never fetch in `onMounted` for initial SSR data
- Nuxt auto-imports (composables, components, utils) over manual imports from app code
- Server-only code in `server/` — never import `server/` utils from client code
- Read config via `useRuntimeConfig()` — not `process.env` at runtime
- `typescript: { strict: true }`, keep pages/components typed
- `<ClientOnly>` or hydration strategies for browser-only fragments
- `definePageMeta()` for per-route layout, middleware, route rules metadata

### MUST NOT DO

- Access `window`/`document` unconditionally in `<script setup>` (SSR runs server-side)
- Use Vuex — use Pinia or `useState`
- Put secrets in `runtimeConfig.public`
- Navigate with `window.location` — use `navigateTo()`/`useRouter()`
- Register components manually when auto-import covers them
- Keep pages/components/composables in root for Nuxt 4 project — use `app/` directory

## Output Templates

When implementing Nuxt features, provide:

1. Page + any layout with `definePageMeta()` + typed data fetching
2. Composable in `app/composables/` when reusable logic exists (auto-imported)
3. Nitro handler in `server/api/` when endpoint needed
4. `nuxt.config.ts` snippet for rendering modes, modules, runtimeConfig
5. Brief explanation of rendering mode + data-fetching decision

## Knowledge Reference

Nuxt 4 / Nuxt 3, SSR/SSG/SPA/hybrid via routeRules, Nitro server, `useFetch`/`useAsyncData`/`useLazyFetch`, file-based routing, layouts, middlewares, `useState`, Pinia, `useHead`/`useSeoMeta`, runtimeConfig, TypeScript strict, Vite integration, module ecosystem, `@nuxt/test-utils`