# SetDB

> The simplest zero-setup Python database layer — just import and store.

[![PyPI version](https://img.shields.io/pypi/v/setdb.svg)](https://pypi.org/project/SetDB/)
[![License](https://img.shields.io/pypi/l/setdb.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/setdb.svg)](https://python.org)

---

### ⚡ What is SetDB?

**SetDB** is a minimalist, plug-and-play database layer for Python apps.  
No configuration. No boilerplate. Just import and start saving data.

Works out of the box with SQLite — extendable for other backends.

---

### 🔧 Installation

```bash
pip install setdb
```

---

### 🚀 Quickstart

```python
import setdb

# SetDB connects automatically to a default local SQLite database.
setdb.insert("users", {"name": "alice", "age": 30})

user = setdb.get("users", name="alice")
print(user)  # {'name': 'alice', 'age': 30}
```

---

### 🌐 Features

- 🔌 Zero-config database setup
- ⚡ Single-file persistence with SQLite
- 📦 Simple key-value and table-based storage
- ✅ Auto-create tables if they don't exist
- 🔒 Optional encryption-ready

---

### 📁 Coming Soon

- `.env` + CLI config support
- More backends (PostgreSQL, TinyDB, etc.)
- Model/decorator-based syntax (`@setdb.model`)
- Integration with [SetAPI](https://pypi.org/project/SetAPI/)

---

### 📄 License

MIT — do whatever you want.  
Want to contribute? PRs welcome soon.