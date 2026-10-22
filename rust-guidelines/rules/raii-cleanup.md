# raii-cleanup

Put cleanup in `Drop`, using RAII guards that borrow the resource, rather than repeating it at every return path.

**Why:** Runs on every exit, including `?` and unwinding.

**Sources:** P:idioms/dtor-finally, P:patterns/behavioural/RAII

---

## Finalisation in destructors (P:idioms/dtor-finally)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/idioms/dtor-finally.html), MPL-2.0.

### Description

Rust does not provide the equivalent to `finally` blocks - code that will be
executed no matter how a function is exited. Instead, an object's destructor can
be used to run code that must be run before exit.

### Example

```rust
fn baz() -> Result<(), ()> {
    // some code
}

fn bar() -> Result<(), ()> {
    // These don't need to be defined inside the function.
    struct Foo;

    // Implement a destructor for Foo.
    impl Drop for Foo {
        fn drop(&mut self) {
            println!("exit");
        }
    }

    // The destructor of _exit will run however the function `bar` is exited.
    let _exit = Foo;
    // Implicit return with `?` operator.
    baz()?;
    // Normal return.
    Ok(())
}
```

### Motivation

If a function has multiple return points, then executing code on exit becomes
difficult and repetitive (and thus bug-prone). This is especially the case where
return is implicit due to a macro. A common case is the `?` operator which
returns if the result is an `Err`, but continues if it is `Ok`. `?` is used as
an exception handling mechanism, but unlike Java (which has `finally`), there is
no way to schedule code to run in both the normal and exceptional cases.
Panicking will also exit a function early.

### Advantages

Code in destructors will (nearly) always be run - copes with panics, early
returns, etc.

### Disadvantages

It is not guaranteed that destructors will run. For example, if there is an
infinite loop in a function or if running a function crashes before exit.
Destructors are also not run in the case of a panic in an already panicking
thread. Therefore, destructors cannot be relied on as finalizers where it is
absolutely essential that finalisation happens.

This pattern introduces some hard to notice, implicit code. Reading a function
gives no clear indication of destructors to be run on exit. This can make
debugging tricky.

Requiring an object and `Drop` impl just for finalisation is heavy on
boilerplate.

### Discussion

There is some subtlety about how exactly to store the object used as a
finalizer. It must be kept alive until the end of the function and must then be
destroyed. The object must always be a value or uniquely owned pointer (e.g.,
`Box<Foo>`). If a shared pointer (such as `Rc`) is used, then the finalizer can
be kept alive beyond the lifetime of the function. For similar reasons, the
finalizer should not be moved or returned.

The finalizer must be assigned into a variable, otherwise it will be destroyed
immediately, rather than when it goes out of scope. The variable name must start
with `_` if the variable is only used as a finalizer, otherwise the compiler
will warn that the finalizer is never used. However, do not call the variable
`_` with no suffix - in that case it will be destroyed immediately.

In Rust, destructors are run when an object goes out of scope. This happens
whether we reach the end of block, there is an early return, or the program
panics. When panicking, Rust unwinds the stack running destructors for each
object in each stack frame. So, destructors get called even if the panic happens
in a function being called.

If a destructor panics while unwinding, there is no good action to take, so Rust
aborts the thread immediately, without running further destructors. This means
that destructors are not absolutely guaranteed to run. It also means that you
must take extra care in your destructors not to panic, since it could leave
resources in an unexpected state.

### See also

RAII guards.


## RAII with guards (P:patterns/behavioural/RAII)

[Rust Design Patterns (rust-unofficial)](https://rust-unofficial.github.io/patterns/patterns/behavioural/RAII.html), MPL-2.0.

### Description

RAII stands for "Resource Acquisition is Initialisation" which is a
terrible name. The essence of the pattern is that resource initialisation is
done in the constructor of an object and finalisation in the destructor. This
pattern is extended in Rust by using a RAII object as a guard of some resource
and relying on the type system to ensure that access is always mediated by the
guard object.

### Example

Mutex guards are the classic example of this pattern from the std library (this
is a simplified version of the real implementation):

```rust
use std::ops::Deref;

struct Foo {}

struct Mutex<T> {
    // We keep a reference to our data: T here.
    //..
}

struct MutexGuard<'a, T: 'a> {
    data: &'a T,
    //..
}

// Locking the mutex is explicit.
impl<T> Mutex<T> {
    fn lock(&self) -> MutexGuard<T> {
        // Lock the underlying OS mutex.
        //..

        // MutexGuard keeps a reference to self
        MutexGuard {
            data: self,
            //..
        }
    }
}

// Destructor for unlocking the mutex.
impl<'a, T> Drop for MutexGuard<'a, T> {
    fn drop(&mut self) {
        // Unlock the underlying OS mutex.
        //..
    }
}

// Implementing Deref means we can treat MutexGuard like a pointer to T.
impl<'a, T> Deref for MutexGuard<'a, T> {
    type Target = T;

    fn deref(&self) -> &T {
        self.data
    }
}

fn baz(x: Mutex<Foo>) {
    let xx = x.lock();
    xx.foo(); // foo is a method on Foo.
              // The borrow checker ensures we can't store a reference to the underlying
              // Foo which will outlive the guard xx.

    // x is unlocked when we exit this function and xx's destructor is executed.
}
```

### Motivation

Where a resource must be finalised after use, RAII can be used to do this
finalisation. If it is an error to access that resource after finalisation, then
this pattern can be used to prevent such errors.

### Advantages

Prevents errors where a resource is not finalised and where a resource is used
after finalisation.

### Discussion

RAII is a useful pattern for ensuring resources are properly deallocated or
finalised. We can make use of the borrow checker in Rust to statically prevent
errors stemming from using resources after finalisation takes place.

The core aim of the borrow checker is to ensure that references to data do not
outlive that data. The RAII guard pattern works because the guard object
contains a reference to the underlying resource and only exposes such
references. Rust ensures that the guard cannot outlive the underlying resource
and that references to the resource mediated by the guard cannot outlive the
guard. To see how this works it is helpful to examine the signature of `deref`
without lifetime elision:

```rust
fn deref<'a>(&'a self) -> &'a T {
    //..
}
```

The returned reference to the resource has the same lifetime as `self` (`'a`).
The borrow checker therefore ensures that the lifetime of the reference to `T`
is shorter than the lifetime of `self`.

Note that implementing `Deref` is not a core part of this pattern, it only makes
using the guard object more ergonomic. Implementing a `get` method on the guard
works just as well.

### See also

Finalisation in destructors idiom

RAII is a common pattern in C++:
[cppreference.com](http://en.cppreference.com/w/cpp/language/raii),
wikipedia.

[Style guide entry](https://doc.rust-lang.org/1.0.0/style/ownership/raii.html)
(currently just a placeholder).
