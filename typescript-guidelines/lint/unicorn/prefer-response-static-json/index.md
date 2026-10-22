
### What it does

Enforces the use of `Response.json()` over `new Response(JSON.stringify())`.

### Why is this bad?

`Response.json()` is a more concise and semantically clear way to create JSON responses.
It automatically sets the correct `Content-Type` header (`application/json`) and handles
serialization, making the code more maintainable and less error-prone.

### Examples

Examples of **incorrect** code for this rule:

```javascript
const response = new Response(JSON.stringify(data));
const response = new Response(JSON.stringify(data), { status: 200 });
```

Examples of **correct** code for this rule:

```javascript
const response = Response.json(data);
const response = Response.json(data, { status: 200 });
```

## How to use

## References
