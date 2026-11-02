# SEO & Metadata

Nuxt provides framework-level head management via Unhead — composables for title, meta, Open Graph, JSON-LD, canonical URLs, all SSR-rendered.

## Static site metadata (nuxt.config)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'My App',
      meta: [
        { name: 'description', content: 'Short site description' },
        { name: 'theme-color', content: '#06b6d4' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'canonical', href: 'https://example.com/' }
      ]
    }
  }
})
```

Global defaults here; per-page values via composables (below) override.

## Per-page head (in pages)

```vue
<script setup lang="ts">
// useHead — full control
useHead({
  title: 'About — My App',
  meta: [
    { name: 'description', content: 'About this site' }
  ]
})

// useSeoMeta — focused SEO helper (kebab-case props)
useSeoMeta({
  title: 'About Us',
  description: 'Company page',
  ogTitle: 'About Us',
  ogDescription: 'Company page',
  ogType: 'website',
  ogImage: '/images/og-about.png',   // absolute URLs preferred
  twitterCard: 'summary_large_image',
  canonical: 'https://example.com/about'
})
</script>
```

Reactivity: pass getters (functions returning values) for reactive titles:

```vue
<script setup lang="ts">
const page = ref(1)
useSeoMeta({
  title: () => `Products — page ${page.value}`
})
</script>
```

## Dynamic route pages (title from data)

```vue
<script setup lang="ts">
const route = useRoute()
const { data: post } = await useFetch(`/api/posts/${route.params.slug}`)

useHead(() => ({
  title: `${post.value?.title ?? 'Post'} — Blog`,
  meta: [
    { name: 'description', content: post.value?.excerpt?.slice(0, 155) }
  ]
}))
</script>
```

## Structured data (JSON-LD)

```vue
<script setup lang="ts">
useHead({
  script: [
    {
      type: 'application/ld+json',
      children: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: 'My post',
        datePublished: '2026-01-01',
        author: { '@type': 'Person', name: 'Ann' }
      })
    }
  ]
})
</script>
```

## Open Graph images & social preview

- Use absolute URLs (`https://domain/path/og.png`) — crawlers ignore relative paths
- Dynamic previews: `nuxt-og-image` for per-page OG images
- Add `<meta name="robots">` only to block indexing (`noindex`); otherwise omit (crawlers default to index)

## Sitemap & robots

```bash
pnpm add @nuxtjs/sitemap
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxtjs/sitemap'],
  site: { url: 'https://example.com' },   // sitemap + og base
  sitemap: {
    exclude: ['/admin/**'],
    defaults: { changefreq: 'weekly', priority: 0.8 }
  }
})
// /robots.txt generated automatically when sitemap module + site.url set
```

## Canonical management

- Default canonical in `app.head`, override per-page with `canonical`
- Strip query params unless they change content; self-referencing canonical on paginated pages
- Moved routes: `navigateTo(..., { redirectCode: 301 })` (see routing)

## SSR vs client-only SEO

- All `useHead`/`useSeoMeta` output renders in HTML (SSR) — crawlers get full metadata
- SPA-only routes (`ssr: false`): keep meta + content server-rendered where SEO matters (`routeRules` prerender/ssr, see rendering)

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `app.head` in nuxt.config | Global defaults |
| `useHead({...})` | Full head control |
| `useSeoMeta({...})` | Focused SEO helper |
| getters in composables | Reactive title/meta |
| JSON-LD via `useHead` script | Structured data |
| `@nuxtjs/sitemap` | sitemap.xml + robots.txt |
| Route-level SEO via routeRules | Prerender/SSR where SEO matters |