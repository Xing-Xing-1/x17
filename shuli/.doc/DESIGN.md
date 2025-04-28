
# 📐 Shuli Design Philosophy: Language-Agnostic Structure Model

Shuli adopts a **language-agnostic code structure model**, built on a two-layered architecture:

```
shuli/
├── base/           # Language-agnostic semantic definitions
├── resource/       # Language-specific structural implementations
```

- `base/` contains core abstract types such as `Class`, `Function`, `Argument`, and `Code`.
- `resource/<language>/` contains language-specific versions like `PyClass`, `PyFunction`, etc., which inherit from the base definitions.

---

## ✅ Advantages

| Category         | Benefit                                             |
|------------------|-----------------------------------------------------|
| **Modularity**   | Clear separation of concerns between abstraction and implementation |
| **Extensibility**| Easy to add support for new languages like Java, JS, etc. |
| **Unified Interface** | Exporters operate on `base` models, decoupled from language-specific details |
| **Maintainability** | Updates to one language do not affect the rest of the system |
| **Philosophical Clarity** | Encourages structure-first thinking and long-term system growth |

---

## ❗ Challenges & How We Address Them

| Challenge                | Description                                      | Mitigation Strategy                                          |
|--------------------------|--------------------------------------------------|--------------------------------------------------------------|
| **Initial Complexity**   | More files and modules compared to flat designs | Accept as upfront investment for long-term scalability       |
| **Subclass Redundancy**  | Some `PyClass(Class)` may seem thin wrappers    | Designed for future customization (e.g., AST-specific fields)|
| **Deeper Import Paths**  | Can result in verbose imports                   | Use `__init__.py` files to re-export top-level interfaces    |
| **Synchronization Overhead** | Changes in `base` may require refactoring in `resource/*` | Keep base models stable; use interface contracts carefully   |

---

## 📌 Why This Matters

This architecture allows Shuli to **scale from a Python-only tool to a multi-language documentation system**, while keeping its core logic clean, testable, and adaptable.

