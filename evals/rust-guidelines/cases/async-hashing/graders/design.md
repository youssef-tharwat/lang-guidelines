---
type: llm
focus: {source: file, path: hashing.rs}
weight: 3
---

Judge the code in `hashing.rs`. Pass when ALL of these hold:

1. The CPU-bound hashing does not monopolize the async runtime: it yields cooperatively (for example `tokio::task::yield_now().await` at intervals) or offloads the work (`spawn_blocking`, a thread pool).
2. Each log event records the index and digest as structured `tracing` fields rather than interpolating them into the message string.
3. Fallible operations (such as a `JoinError`) are handled or propagated, not unwrapped without a stated invariant.
4. Digests are returned in input order.
5. The public function has `///` docs.

Fail if any item is missing. List each item as met or not met before the verdict.
