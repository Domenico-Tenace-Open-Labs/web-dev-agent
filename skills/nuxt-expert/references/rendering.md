# Rendering Modes & Hydration

Nuxt decouples client/server rendering per route via `routeRules`. Choose mode per route instead of one global setting.

## Rendering modes

| Mode | Setup | Use Case |
|------|-------|----------|
| **Universal (SSR)** | default | Dynamic content, personalized pages, SEO-critical with data |
| **SSG (prerendered)** | `routeRules: { '/**': { prerender: true } }` or `nitro.prerender` | Marketing pages, blogs, docs |
| **SPA (client)** | `routeRules: { '/app/**': { ssr: false } }` | Protected dashboards, auth-gated apps |
| **Hybrid** | per-route `routeRules` | Mix of the above in one app |

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },                     // SSG homepage
    '/blog/**': { swr: 3600 },                    // stale-while-revalidate, 1h
    '/app/**': { ssr: false },                    // SPA section
    '/admin/**': { redirect: '/login' },          // redirect
    '/old': { redirect: { to: '/new', statusCode: 301 } },
    '/api/legacy/**': { proxy: 'https://api.legacy.com/**' }, // BFF proxy
    '/privacy': { prerender: true, headers: { 'Cache-Control': 'max-age=31536000, immutable' } }
  }
})
```

`swr`/`prerender` only used with node server or edge provider supporting Nitro caching (Vercel, Netlify, Cloudflare, AWS Lambda).

### Route rule conflict resolution

More specific (larger) patterns win; `ssr: false` and `swr`/`prerender` mutually exclusive per route. Keep rules same specificity; add `app: { pageTransition }` etc. only where intended.

## Server-side rendering (SSR)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  ssr: true, // default; false → pure SPA
})
```

Behavior:

- First request server-renders: HTML + serialized payload (`__NUXT_DATA__`)
- Client hydrates and takes over
- Data via `useFetch`/`useAsyncData` reused — no double fetch when keys match

## SSG / prerendering

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    prerender: { routes: ['/', '/about', '/sitemap.xml'] }
  }
})
```

Prerendered routes ship fully-static HTML — deploy to any static host. Dynamic pages use `getCachedKeys`/callbacks at build time or fall back to SWR at edge.

## Hydration best practices

### Hydration mismatch prevention

```vue
<script setup lang="ts">
// Browser-only value must not render on server
const now = ref<string | null>(null)
onMounted(() => { now.value = new Date().toLocaleString() })
</script>

<template>
  <!-- v-if guards server/HTML vs client-safe value -->
  <span v-if="now">{{ now }}</span>
  <span v-else>—</span>
</template>
```

Root cause of mismatch: output differs between server HTML and first client render. Defer browser-only values to `onMounted` (or `useId`/`v-if`).

### Client-only components

```vue
<script setup lang="ts">
const HeavyChart = defineAsyncComponent(() => import('~/components/HeavyChart.vue'))
</script>

<template>
  <ClientOnly fallback-tag="span" fallback="Loading chart…">
    <HeavyChart />
  </ClientOnly>
</template>
```

`<ClientOnly>` renders nothing (or fallback) server-side, mounts on client.

### Laggy/lazy hydration

```vue
<script setup lang="ts">
definePageMeta({ hydration: 'when-visible' }) // Nuxt 4 experimental hydration strategy
</script>
<template>
  <LazyBelowFoldContent /> <!-- <Lazy*> prefixed import → hydration deferral -->
</template>
```

## Code splitting & loading

- Nuxt auto-split per route (lazy-loaded pages)
- `<LazyComponent>` alone does client-side deferral
- `defineAsyncComponent` for manual `import()` control
- Rarely use `experimental.pages.bypass`-style options; prefer defaults

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `routeRules['/path'].prerender` | SSG for a route |
| `routeRules['/path'].swr: 3600` | Revalidate at most hourly, serve cached |
| `routeRules['/path'].ssr: false` | SPA section |
| `routeRules` `redirect`, `proxy`, `headers` | Edge behaviors in one config |
| `ssr: false` | Whole app as SPA |
| `<ClientOnly>` | Browser-only fragments |
| `onMounted` + guard | Prevent hydration mismatch |
| `<Lazy*>` / `defineAsyncComponent` | Defer non-critical code |