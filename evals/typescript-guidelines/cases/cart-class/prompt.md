---
description: Class design with events and pricing strategies; tests classes, types and JSDoc.
tags: [classes, types, docs]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write]
---

Write a TypeScript module `cart.ts` with a `ShoppingCart` that holds line items (product id, unit price in cents, quantity), computes the total, applies one interchangeable discount policy (none, percentage off, buy-one-get-one on a product), and notifies subscribers whenever its contents change. Include JSDoc. Write it to `cart.ts` in the current directory; don't create other files.
