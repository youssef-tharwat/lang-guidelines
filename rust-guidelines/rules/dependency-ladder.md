# dependency-ladder

For a swappable dependency, climb only as far as needed: a concrete type, then an enum with a mock variant, then narrow traits taken as generics, then a named wrapper around `Arc<dyn Trait>` once generics nest. Don't port interface-style `Rc<dyn Trait>` designs.

**Why:** Each step up costs composability and clarity.

**Sources:** M-DI-HIERARCHY, G:generics-versus-dyn-trait

---

## Prefer types over generics, generics over dyn traits (M-DI-HIERARCHY)

[Microsoft Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), MIT.

When asking for async dependencies, prefer concrete types over generics, and generics over `dyn Trait`.

It is easy to accidentally deviate from this pattern when porting code from languages like C# that heavily rely on interfaces.
Consider you are porting a service called `Database` from C# to Rust and, inspired by the original `IDatabase` interface, you naively translate it into:

```rust
trait Database {
    async fn update_config(&self, file: PathBuf);
    async fn store_object(&self, id: Id, obj: Object);
    async fn load_object(&self, id: Id) -> Object;
}

impl Database for MyDatabase { ... }

// Intended to be used like this:
async fn start_service(b: Rc<dyn Database>) { ... }
```

Apart from not feeling idiomatic, this approach precludes other Rust constructs that conflict with object safety,
can cause issues with asynchronous code, and exposes wrappers (compare M-AVOID-WRAPPERS).

Instead, when more than one implementation is needed, this _design escalation ladder_ should be followed:

If the other implementation is only concerned with providing a _sans-io_ implementation for testing, implement your type as an
enum, following M-MOCKABLE-SYSCALLS instead.

If users are expected to provide custom implementations, you should introduce one or more traits, and implement them for your own types
_on top_ of your inherent functions. Each trait should be relatively narrow, e.g., `StoreObject`, `LoadObject`. If eventually a single
trait is needed it should be made a subtrait, e.g., `trait DataAccess: StoreObject + LoadObject {}`.

Code working with these traits should ideally accept them as generic type parameters as long as their use does not contribute to significant nesting
(compare M-ABSTRACTIONS-DONT-NEST).

```rust
// Good, generic does not have infectious impact, uses only most specific trait
async fn read_database(x: impl LoadObject) { ... }

// Acceptable, unless further nesting makes this excessive.
struct MyService<T: DataAccess> {
    db: T,
}
```

Once generics become a nesting problem, `dyn Trait` can be considered. Even in this case, visible wrapping should be avoided, and custom wrappers should be preferred.

```rust
// This allows you to expand or change `DynamicDataAccess` later. You can also
// implement `DataAccess` for `DynamicDataAccess` if needed, and use it with
// regular generic functions.
struct DynamicDataAccess(Arc<dyn DataAccess>);

impl DynamicDataAccess {
    fn new<T: DataAccess + 'static>(db: T) -> Self {
        Self(Arc::new(db))
    }
}

struct MyService {
    db: DynamicDataAccess,
}
```

The generic wrapper can also be combined with the enum approach from [M-MOCKABLE-SYSCALLS]:

```rust
enum DataAccess {
    MyDatabase(MyDatabase),
    Mock(mock::MockCtrl),
    Dynamic(DynamicDataAccess)
}

async fn read_database(x: &DataAccess) { ... }
```


## Generics versus `dyn Trait` (G:generics-versus-dyn-trait)

[Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html#generics-versus-dyn-trait), CC BY 3.0.

In libraries, prefer accepting generics (`T: Trait` or `impl Trait`) in function parameters over `dyn Trait`.

Exceptions:

*   Cases where code size matters.

**Rationale**

*   Efficiency

    *   Additional indirection: Creating a `dyn Trait` requires setting up a fat pointer, and a vtable lookup is required for every call of a function on the trait.

    *   If a function takes a `dyn Trait`, the compiler can’t perform certain optimizations that it could if the function was generic, such as inlining calls to functions of the trait.

*   Some traits are not [`dyn` compatible](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility). For example, a trait is not `dyn` compatible if it has generic functions, associated functions without a `self` parameter, or functions that return `Self`.
