# properties

Use `@property` only for cheap, unsurprising computed or access-controlled values; not to wrap a plain attribute (make it public), not for costly work, and not for logic a subclass may need to override.

**Why:** Attribute access must stay cheap and predictable.

**Sources:** G:s2.13-properties

---

## Properties (G:s2.13-properties)

[Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#s2.13-properties), CC BY 3.0.

Properties may be used to control getting or setting attributes that require
trivial computations or logic. Property implementations must match the general
expectations of regular attribute access: that they are cheap, straightforward,
and unsurprising.

### 2.13.1 Definition

A way to wrap method calls for getting and setting an attribute as a standard
attribute access.

### 2.13.2 Pros

*   Allows for an attribute access and assignment API rather than
    getter and setter method calls.
*   Can be used to make an attribute read-only.
*   Allows calculations to be lazy.
*   Provides a way to maintain the public interface of a class when the
    internals evolve independently of class users.

### 2.13.3 Cons

*   Can hide side-effects much like operator overloading.
*   Can be confusing for subclasses.

### 2.13.4 Decision

Properties are allowed, but, like operator overloading, should only be used when
necessary and match the expectations of typical attribute access; follow the
getters and setters rules otherwise.

For example, using a property to simply both get and set an internal attribute
isn't allowed: there is no computation occurring, so the property is unnecessary
(make the attribute public instead). In comparison,
using a property to control attribute access or to calculate a *trivially*
derived value is allowed: the logic is simple and unsurprising.

Properties should be created with the `@property`
decorator. Manually implementing a
property descriptor is considered a power feature.

Inheritance with properties can be non-obvious. Do not use properties to
implement computations a subclass may ever want to override and extend.
