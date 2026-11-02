# State Management

Nuxt provides two SSR-safe state mechanisms: `useState` (built-in, small shared state) + Pinia via `@pinia/nuxt` (structured stores).

## `useState` — SSR-safe shared state

`useState` with same key shares state across components, serialized into payload on server → hydration-safe (no mismatch):

```vue
<script setup lang="ts">
const counter = useState<number>('counter', () => 0)
const user = useState(() => null) // key auto-derived — prefer explicit key

function increment() { counter.value++ }
</script>
<template>
  <button @click="increment">Count: {{ counter }}</button>
</template>
```

Rules:

- `useState` in setup/plugins/middleware (Nuxt context) only
- Prefer **composable** wrapping `useState` so key lives in one place:

```typescript
// app/composables/useCart.ts (auto-imported)
export const useCart = () => {
  const items = useState<CartItem[]>('cart', () => [])
  const total = computed(() => items.value.reduce((s, i) => s + i.price * i.qty, 0))
  function add(item: CartItem) { items.value.push(item) }
  return { items, total, add }
}
```

- No non-serializable values in `useState` (functions, class instances, complex objects)
- Structured/global domain state (auth, cart, settings across many components) → Pinia

## Pinia with Nuxt

```bash
pnpm add pinia @pinia/nuxt
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt']   // auto-installed Pinia instance
})
```

Setup-style store (recommended, Composition API):

```typescript
// app/stores/user.ts (auto-imported via @pinia/nuxt)
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => user.value !== null)

  async function login(email: string, password: string) {
    const { data, error } = await useFetch('/api/auth/login', { method: 'POST', body: { email, password } })
    if (data.value) user.value = data.value.user
    return !!data.value
  }
  function logout() { user.value = null }

  return { user, isLoggedIn, login, logout }
})
```

Use in components (no `storeToRefs` needed for setup stores—destructure refs directly, keep reactivity):

```vue
<script setup lang="ts">
const store = useUserStore()
const { user, isLoggedIn } = storeToRefs(store) // keep reactivity when destructuring
const { login, logout } = store                 // actions are plain functions
</script>
```

## SSR + Pinia pitfalls

- Don't seed `useState`-backed stores from `onMounted` only — initial data must be set during SSR to avoid hydration mismatch
- Guard async store actions against double-run: Nuxt dedupes `useFetch` per key; call store actions inside `await useAsyncData` for server-rendered data:

```typescript
// app/pages/dashboard.vue
const store = useUserStore()
await useAsyncData('dashboard-data', () => store.fetchDashboard()) // SSR-safe, deduped
```

- Pinia devtools work out of the box; enable `devtools` in nuxt.config

## Cookies & client-only state

```typescript
// SSR-safe cookie access
const token = useCookie('token')            // auto-refreshed each request
const theme = useCookie('theme', { maxAge: 60 * 60 * 24 * 365 })
```

Use `useCookie` for per-visitor persistent state (session, theme, locale) instead of `localStorage` (not on server → hydration mismatch).

## Persistence

Nuxt-friendly Pinia persistence: `pinia-plugin-persistedstate` (mount in Nuxt plugin or via `@pinia/nuxt`). Prefer cookies for cross-request values SSR reads.

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `useState(key, init)` | Small SSR-safe shared state |
| `useState` in a composable | One source of truth per key |
| Pinia + `@pinia/nuxt` | Structured global stores |
| Setup stores | Recommended Pinia style |
| `storeToRefs()` | Reactive destructuring |
| `useCookie()` | SSR-safe visitor state |
| Pinia + `useAsyncData` | SSR-seeded store data |