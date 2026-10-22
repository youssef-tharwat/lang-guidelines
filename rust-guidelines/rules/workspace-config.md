# workspace-config

Related crates share one workspace: members inherit metadata, lints and dependency versions from `[workspace.*]`; every crate is a member listed in `[workspace.dependencies]` and siblings depend on it with `.workspace = true`, not `path =`; workspace entries set `default-features = false`.

**Why:** One canonical version and configuration per dependency.

**Sources:** M-CARGO-WORKSPACE, M-CRATES-IN-WORKSPACE

---

## Common settings come from the workspace Cargo.toml (M-CARGO-WORKSPACE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Any repo with two or more crates that somehow belong together should unify these crates with a workspace `Cargo.toml`. Members then inherit shared metadata and dependency versions from the workspace root via `[workspace.dependencies]`, `[workspace.lints]`, ... rather than duplicating these values in each crate.

Where a dependency is crate-specific, it should still be defined in the workspace. Workspace definitions should generally not enable dependency features (except basic ones such as `["std"]`), and should instead use `default-features = false`.


## The workspace lists and versions all crates (M-CRATES-IN-WORKSPACE)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

Every crate produced by the project should be listed as a workspace member, and its version should be declared in `[workspace.dependencies]` so that intra-workspace dependencies resolve to a single canonical version.

```toml
# Bad, crate links its sibling directly
[dependencies]
sibling.path = "../sibling"

# Good, going through workspace
[dependencies]
sibling.workspace = true

[workspace.dependencies]
sibling = { path = "crates/sibling", version = "0.5.2" }
```
