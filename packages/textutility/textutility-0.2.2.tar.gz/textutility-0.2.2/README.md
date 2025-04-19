# textutility

A set of useful functions for analyzing and manipulating strings in Python.

---

## ✨ Features

- Check if a string is a number, float, or boolean
- Reverse strings and detect palindromes
- Convert between `snake_case` and `camelCase`
- Print boxed output with `exclusive_print()`
- Detect types using `what_type()`
- And more!

---

## 📦 What's new (v0.2.2)

- ✅ `what_type()` — detects whether a string represents `int`, `float`, `bool`, or plain `string`
- 🧾 `exclusive_print()` — prints any text inside a fancy ASCII box
- 📐 `printBox()` — a context manager version of `exclusive_print()` that works with `with`:
  ```python
  with printBox("Hello box!"):
      pass

## Installation

```bash
pip install textutility
