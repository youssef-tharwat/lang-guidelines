---
description: Typed REST client module; tests exports, unknown data, errors and type design.
tags: [modules, types, errors]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Write a TypeScript module `userClient.ts` that fetches users from `GET {baseUrl}/users` (a JSON array of objects with `id`, `name`, optional `email`) and `GET {baseUrl}/users/{id}`, using the global `fetch`. Responses come from a server you don't control. Export what callers need, including an error type for failed requests and malformed responses, with JSDoc. Write it to `userClient.ts` in the current directory; don't create other files.
