# edition-and-msrv

Start new crates on the latest stable edition (2024 or later) without a `resolver` field; libraries declare an MSRV kept a few releases behind stable and raise it in minor releases.

**Why:** Old editions add friction and no compatibility.

**Sources:** M-LATEST-EDITION, M-MSRV

---

## New crates target latest edition (M-LATEST-EDITION)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When creating a new crate or workspace, set `edition` to the latest stable edition (at least `2024` at the time of writing); the `resolver` field is generally not needed.

Using an older edition generally has no upsides for new projects, but forces you to write 'old Rust' that is less idiomatic and has worse UX edge cases. Notably, using an older edition does _not_ grant any compatibility benefits with the rest of the ecosystem. An application based on `2015` can use libraries written for `2024` just fine.


## MSRV is conservatively updated (M-MSRV)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

A Minimum Supported Rust Version (MSRV) should be set when libraries are first created. It can be updated as new Rust features are needed, but should be kept a few versions behind the most recent compiler release.

The ecosystem expectation is that projects are compiled with a _reasonably modern_ Rust compiler.

Bumping MSRV therefore does not require a major release, but can be handled through a minor update (e.g., `1.3` to `1.4`). In fact, any project depending on 3rd party crates is already inherently bound to this contract; forcing a major version bump will not confer any benefits, but could possibly bifurcate downstream dependencies.
