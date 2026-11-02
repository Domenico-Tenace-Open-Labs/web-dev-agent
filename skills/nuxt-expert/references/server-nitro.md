# Nitro Server

Nitro powers `server/` — API endpoints, middleware, scheduled tasks, deployment presets. Code here server-only, never ships to client.

## Project structure

```text
server/
├── api/           # /api/* endpoints (auth.api.ts → /api/auth)
│   ├── users.get.ts
│   ├── users/[id].get.ts
│   └── users.post.ts
├── routes/        # non-/api endpoints (/health)
├── middleware/    # server middleware (runs before handlers)
├── utils/         # auto-imported server helpers (import from '~server/utils/...')
├── plugins/       # Nitro lifecycle hooks
└── tasks/         # scheduled/queued tasks
```

Handlers auto-registered by filename (`[name].[method].ts`, `[name].get.ts`, …). Same path, multiple methods → `users.get.ts` + `users.post.ts`.

## Event handlers

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event)                 // { page?: string, limit?: string }
  const users = await db.users.findMany({ ... })
  return users                                  // auto-serialized JSON
})

// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')        // route param
  const user = await db.users.findUnique({ where: { id: Number(id) } })
  if (!user) {
    throw createError({ statusCode: 404, statusMessage: 'User not found' })
  }
  return user
})

// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)            // parsed body
  const created = await db.users.create({ data: body })
  setResponseStatus(event, 201)
  return created
})
```

## Request helpers

```typescript
const query = getQuery(event)                                   // GET query
const params = getRouterParam(event, 'name')                    // route params
const body = await readBody(event)                              // POST body
const cookie = getCookie(event, 'session')                      // cookies
const headers = getHeaders(event)                               // request headers
const host = getRequestHost(event)                              // host
const url = getRequestURL(event)                                // full URL
```

## Responses

```typescript
return createError({ statusCode: 400, statusMessage: 'Bad request', data: { field: 'email' } })
sendRedirect(event, '/new', 302)
event.node.res.statusCode // low-level escape hatch (avoid unless needed)
```

Never disclose internal details in errors; keep user-facing messages safe.

## Runtime config (env access)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    // Server-side only — never sent to client
    apiSecret: process.env.API_SECRET,
    // Public — exposed to client via NUXT_PUBLIC_*
    public: { apiBase: '/api' }
  }
})
```

```typescript
// In handlers & composables
const config = useRuntimeConfig()
config.apiSecret        // server-only (undefined on client)
config.public.apiBase   // everywhere
```

Env overrides: `NUXT_API_SECRET=...`, `NUXT_PUBLIC_API_BASE=...` — prefer env vars over committing secrets.

## Server middleware

```typescript
// server/middleware/log.ts — runs before every request
export default defineEventHandler((event) => {
  console.log(`[${event.method}] ${event.path}`)
})
```

## Server plugins (lifecycle)

```typescript
// server/plugins/db.ts
export default defineNitroPlugin((nitroApp) => {
  nitroApp.hooks.hook('request', (event) => { /* per request */ })
  nitroApp.hooks.hook('error', (error, event) => { logError(error) })
})
```

## Caching & performance

```typescript
// server/api/slow.get.ts
export default defineCachedEventHandler(
  async (event) => { return await expensiveCompute() },
  { maxAge: 60 * 5, swr: true, name: 'slow-result' }
)

// setCacheHeaders() for edge caching via routeRules instead
```

## WebSockets & events

```typescript
// server/api/ws.ts (Nuxt 4 / Nitro supports fresh/WebSockets)
export default defineWebSocketHandler({
  open(peer) { peer.send('connected') },
  message(peer, message) { peer.send(message.text()) }
})
```

## Error handling

```typescript
// Global error hook in server/plugins
export default defineNitroPlugin((nitroApp) => {
  nitroApp.hooks.hook('error', (error, event) => {
    // correlate via event.path, event.headers.…; never log secrets/PII
    captureError(error)
  })
})
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `server/api/**` | REST endpoints |
| `server/routes/**` | Non-/api paths |
| `defineEventHandler` | Handler signature |
| `getQuery` / `readBody` / `getRouterParam` | Input access |
| `createError` / `sendRedirect` | Responses & errors |
| `useRuntimeConfig()` | Env/secret access |
| `server/middleware/*` | Pre-handler logic |
| `defineCachedEventHandler` | Response caching |
| `defineWebSocketHandler` | WS endpoints |