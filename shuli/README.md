# Shuli 书吏 - The Scribe of Your Codebase

> _“夫文者，贯道之器也；书吏者，记文之人也。”_  
> In the spirit of ancient scribes, Shuli seeks to record the soul of code—not just its form.

**Shuli** is a documentation engine for Python projects that understands code structure—whether it follows Object-Oriented Programming or not. It analyzes source files and extracts meaningful descriptions of classes, functions, methods, and modules.

Unlike traditional doc generators, Shuli is designed to be **framework-agnostic**, **output-flexible**, and **developer-centered**, acting as a modern-day scribe that captures the spirit—not just the syntax—of your codebase.


## Why Shuli?

Modern codebases grow rapidly and involve teams, automation, and integration. Yet developers often struggle with:
- Incomplete or outdated documentation
- Poorly formatted or inconsistent structure in auto-generated docs
- Difficulty extracting custom structures across modules or frameworks

Shuli is here to solve this by providing:
- **Structure-aware parsing** of Python source files
- **Multi-format output**: Markdown, Sphinx-compatible reStructuredText, JSON
- **Customizable exporters** for integration with any pipeline

---

## 🧱 Project Structure
```
shuli/
├── base/           # 所有语言共通的结构抽象
│   ├── class_.py       → class Class
│   ├── function.py     → class Function
│   ├── argument.py     → class Argument
│   └── code.py         → class Code
├── resource/       # 各语言具体化资源结构
│   └── python/
│       ├── py_class.py      → class PyClass(Class)
│       ├── py_function.py   → class PyFunction(Function)
│       ├── py_argument.py   → class PyArgument(Argument)
│       └── py_code.py       → class PyCode(Code)
```
