# Data Fetching

Nuxt data fetching SSR-safe by default: fetched on server during SSR, serialized in payload, reused for hydration — no double fetch.

## `useFetch` — recommended default

```vue
<script setup lang="ts">
interface User { id: number; name: string; email: string }

// Auto keyed by URL + options, cached, SSR + client safe
const { data: users, pending, error, refresh, status } = await useFetch<User[]>('/api/users')

// With options
const { data: page } = await useFetch('/api/items', {
  method: 'GET',
  query: { page: 1, limit: 20 },     // serialized into the key
  headers: {},                        // passed to the request
  transform: (items: Item[]) => items.map(...),  // transform/pick response
  pick: ['id', 'title'],
  watch: [page, limit],               // re-fetch when these change
  server: true,                       // fetch on server (default true)
  lazy: false,                        // non-blocking (default false in await form)
  immediate: true,                    // fetch on mount (default true)
  key: 'custom-key',                  // manual key (deduping/sharing)
  dedupe: 'cancel',                   // 'cancel' (default) or 'defer'
  default: () => [],                  // value while pending
  getCachedData: (key, nuxtApp, payload) => payload.data,
  baseURL: '/',                       // relative base for request
  credentials: 'same-origin'
})
</script>
```

Suspense-friendly: `await useFetch(...)` → navigation waits for fetch. Non-blocking: omit `await`, use `pending`.

## `useAsyncData` — custom handler

```vue
<script setup lang="ts">
const { data: user } = await useAsyncData(
  'user-123',                        // unique key (shared, deduped)
  () => queryDB.getUser(123),        // any async operation
  {
    server: true,
    lazy: false,
    default: () => null,
    transform: (u) => ({ ...u, name: u.name.toUpperCase() })
  }
)
</script>
```

`useAsyncData` takes any async function/callback — for non-fetch work or wrapping libraries. `useFetch` = `useAsyncData` + `$fetch`.

## Lazy variants (non-blocking)

```vue
<script setup lang="ts">
// Does NOT block navigation; data starts null
const { data: posts, pending } = await useLazyFetch('/api/posts')
const { data: comments } = await useLazyAsyncData('comments', () => $fetch('/api/comments'))
</script>
```

Use `lazy: true` or `useLazy*` when page must render before data (UX: skeletons).

## Manual refresh & revalidation

```vue
<script setup lang="ts">
const { data, refresh, status } = await useFetch('/api/items')

async function onFilterChange() {
  await refresh()                       // refresh the single request
}

function reloadAll() {
  refreshNuxtData()                     // all keys
  refreshNuxtData('items')              // one key
}
</script>
```

`clearNuxtData(keys?)` drops cached data (forces re-fetch on next mount).

## `$fetch` — plain HTTP

`$fetch` (ofetch) for client-side-only calls, event handlers, or where SSR reuse not needed:

```typescript
const res = await $fetch('/api/users', { method: 'POST', body: { name: 'Ann' } })
// $fetch throws on 4xx/5xx — catch it:
try {
  await $fetch('/api/users/999')
} catch (err) {
  // err.data (response body), err.statusCode
  showToast('User not found')
}
```

## Error handling

```vue
<script setup lang="ts">
const { data, error } = await useFetch('/api/users')

// useFetch surfaces errors in error.value (does not throw by default)
if (error.value) {
  console.error('failed', error.value.statusCode, error.value.statusMessage)
}
</script>
```

Server-side failures that must 404/500 the page: throw `createError` in server handler or check `error.value` after `await useFetch` and `throw createError({ ... })` when SSR.

## Payload extraction

`useFetch` executes server-side and transfers only payload:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  payloadExtraction: false, // transfer whole data (disabled by default for SPA-less)
})
```

Default: composable data removed from HTML payload unless `payloadExtraction` enabled in production builds. Leave defaults unless measured.

## Caching & deduping

- Requests deduped per key (URL + options default) — concurrent calls share one request
- Manual `key` shares data across components
- `getCachedData` + `routeRules` (see rendering) power incremental static rendering

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `useFetch(url, opts)` | SSR-safe fetching, keyed by URL |
| `useAsyncData(key, fn, opts)` | Any async data with custom key |
| `useLazyFetch` / `useLazyAsyncData` | Non-blocking data (skeleton UX) |
| `refresh()` | Re-run one composable |
| `refreshNuxtData(key?)` | Re-run all / one key |
| `clearNuxtData(key?)` | Drop cached payloads |
| `$fetch` | Plain HTTP, client-side calls, server handlers |
| `error.value` | Non-throwing fetch errors |