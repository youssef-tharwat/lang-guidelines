# throughput

Design for throughput: batch APIs, partitioned work, sleep when idle; no hot spinning, per-item work when batching is possible, or per-item work stealing; share state only when it is cheaper than recomputing.

**Why:** Items per CPU cycle is the metric that scales.

**Sources:** M-THROUGHPUT

---

## Optimize for throughput, avoid empty cycles (M-THROUGHPUT)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

You should optimize your library for throughput, and one of your key metrics should be _items per CPU cycle_.

This does not mean to neglect latency&mdash;after all you can scale for throughput, but not for latency. However,
in most cases you should not pay for latency with _empty cycles_ that come with single-item processing, contended locks and frequent task switching.

Ideally, you should

- partition reasonable chunks of work ahead of time,
- let individual threads and tasks deal with their slice of work independently,
- sleep or yield when no work is present,
- design your own APIs for batched operations,
- perform work via batched APIs where available,
- yield within long individual items, or between chunks of batches (see M-YIELD-POINTS),
- exploit CPU caches, temporal and spatial locality.

You should not:

- hot spin to receive individual items faster,
- perform work on individual items if batching is possible,
- do work stealing or similar to balance individual items.

Shared state should only be used if the cost of sharing is less than the cost of re-computation.
