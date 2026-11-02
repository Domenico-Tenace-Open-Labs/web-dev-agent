# Pages, Layouts & Middleware

## File-based Routing

`app/pages/` (Nuxt 4) or `pages/` (Nuxt 3) maps files to routes:

```text
app/pages/
├── index.vue            # /
├── about.vue            # /about
├── users/
│   ├── index.vue        # /users
│   └── [id].vue         # /users/:id
├── blog/
│   └── [...slug].vue    # /blog/... (catch-all)
├── dashboard.vue
└── admin/
    └── index.vue        # /admin
```

Dynamic params via `useRoute()`:

```vue
<!-- app/pages/users/[id].vue -->
<script setup lang="ts">
const route = useRoute()
const userId = computed(() => route.params.id)
</script>
```

Catch-all:

```vue
<!-- app/pages/blog/[...slug].vue -->
<script setup lang="ts">
const route = useRoute()
const slug = route.params.slug // string[] | string
</script>
```

## Page Metadata

```vue
<script setup lang="ts">
definePageMeta({
  title: 'Dashboard',
  layout: 'dashboard',           // select a layout
  middleware: 'auth',            // named middleware (string or array)
  // prefer global `routeRules` in nuxt.config for caching/prerender
})
</script>
```

`definePageMeta` only in `app/pages/`. Statically analyzed — no dynamic values beyond supported options.

## Navigation

```typescript
const router = useRouter()
const route = useRoute()

await navigateTo('/users/1')           // server + client safe
await navigateTo({ path: '/users', query: { page: 2 } })
await navigateTo('/login', { redirectCode: 301 })

router.push('/about')
router.replace('/about')

return navigateTo('/login')            // from route middleware — stop execution
```

Prefer `navigateTo()` (server + client); `router.push` client-only.

## Layouts

```vue
<!-- app/layouts/default.vue -->
<template>
  <div class="app-shell">
    <header><AppHeader /></header>
    <main><slot /></main>
    <footer><AppFooter /></footer>
  </div>
</template>

<!-- app/layouts/dashboard.vue -->
<template>
  <div class="dashboard">
    <aside><Navigation /><slot /></aside>
  </div>
</template>
```

Select via `definePageMeta`:

```vue
<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })
</script>
```

`app.vue` renders active layout + page:

```vue
<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
```

## Route Middleware

Named middleware run before page render:

```typescript
// app/middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn } = useAuth()
  if (!isLoggedIn.value) {
    return navigateTo('/login')
  }
})

// Inline (Nuxt 4) — colocated in app/middleware, named by file
```

Reference by name:

```vue
<script setup lang="ts">
definePageMeta({ middleware: 'auth' })
</script>
```

Return values: `navigateTo()` (redirect), `abortNavigation()` (cancel), or nothing (allow).

## Error Pages

```vue
<!-- app/error.vue -->
<script setup lang="ts">
const props = defineProps<{ error: Error & { statusCode: number } }>()
</script>

<template>
  <div>
    <h1>{{ props.error.statusCode }}</h1>
    <p>{{ props.error.message }}</p>
  </div>
</template>
```

## Type-safe routes (Nuxt 4, experimental)

Typed routes for autocomplete-aware `navigateTo`/`<NuxtLink>`:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  experimental: { typedPages: true }
})
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `app/pages/**/*.vue` | File-based routes |
| `[id].vue` / `[...slug].vue` | Dynamic / catch-all routes |
| `definePageMeta()` | Layout, middleware, title |
| `navigateTo()` | Server+client safe navigation |
| `app/layouts/default.vue` | Automatic default layout |
| `definePageMeta({ layout })` | Choose a named layout |
| `app/middleware/*.ts` | Route guards |
| `app/error.vue` | Custom error page |
| `experimental.typedPages` | Type-safe routing |