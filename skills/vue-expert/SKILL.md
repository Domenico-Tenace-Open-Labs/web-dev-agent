---
name: vue-expert
description: Vue 3 / Nuxt conventions — Composition API with <script setup>, typed props/emits, composables, Pinia stores, Vite build config. Load when the project uses Vue 3 (.vue SFC, nuxt.config.*, Pinia stores); also Quasar/Capacitor mobile and PWA/service-worker work.
license: MIT
---

# Vue Expert

Senior Vue specialist, deep expertise Vue 3 Composition API, reactivity system, modern Vue ecosystem. *Derived from Jeffallan's vue-expert skill (MIT).*

> Styling-agnostic: pair with skill `bulma-expert` when project uses Bulma — no duplication.

## Core Workflow

1. **Analyze requirements** - component hierarchy, state needs, routing
2. **Design architecture** - plan composables, stores, component structure
3. **Implement** - build components with Composition API + proper reactivity
4. **Validate** - run `vue-tsc --noEmit` type errors; verify reactivity Vue DevTools. Errors → fix each, re-run until clean
5. **Optimize** - minimize re-renders, optimize computed, lazy load
6. **Test** - component tests Vue Test Utils + Vitest. Fail → find root cause (component bug vs wrong assertion), fix, re-run until pass

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Composition API | `references/composition-api.md` | ref, reactive, computed, watch, lifecycle |
| Components | `references/components.md` | Props, emits, slots, provide/inject |
| State Management | `references/state-management.md` | Pinia stores, actions, getters |
| Nuxt 3 | `references/nuxt.md` | SSR, file-based routing, useFetch, Fastify, hydration |
| TypeScript | `references/typescript.md` | Typing props, generic components, type safety |
| Mobile & Hybrid | `references/mobile-hybrid.md` | Quasar, Capacitor, PWA, service worker, mobile |
| Build Tooling | `references/build-tooling.md` | Vite config, sourcemaps, optimization, bundling |

## Quick Example

Minimal component demonstrating preferred patterns:

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{ initialCount?: number }>()

const count = ref(props.initialCount ?? 0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>

<template>
  <button @click="increment">Count: {{ count }} (doubled: {{ doubled }})</button>
</template>
```

## Constraints

### MUST DO

- Use Composition API (NOT Options API)
- Use `<script setup>` syntax
- Type-safe props with TypeScript
- `ref()` primitives, `reactive()` objects
- `computed()` derived state
- Proper lifecycle hooks (onMounted, onUnmounted, etc.)
- Proper cleanup in composables
- Pinia for global state

### MUST NOT DO

- Use Options API (data, methods, computed as object)
- Mix Composition API with Options API
- Mutate props directly
- Create reactive objects unnecessarily
- Use watch when computed suffices
- Forget cleanup of watchers/effects
- Access DOM before onMounted
- Use Vuex (deprecated — Pinia)

## Output Templates

When implementing Vue features, provide:

1. Component file `<script setup>` + TypeScript
2. Composable if reusable logic exists
3. Pinia store if global state needed
4. Brief explanation of reactivity decisions

## Knowledge Reference

Vue 3 Composition API, Pinia, Nuxt 3, Vue Router 4, Vite, VueUse, TypeScript, Vitest, Vue Test Utils, SSR/SSG, reactive programming, performance optimization