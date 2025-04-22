# scsarchive

[![PyPI version](https://img.shields.io/pypi/v/scsarchive.svg?color=green)](https://pypi.org/project/scsarchive/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/scsarchive)](https://pypi.org/project/scsarchive/)

`scsarchive` is a simple Python utility that registers the `.scs` archive format — an uncompressed `.zip` format used by Euro Truck Simulator 2 and American Truck Simulator mods — for use with Python’s `shutil.make_archive()` function.

## 🚀 Features

- Register `.scs` as a custom archive format for use with Python's standard `shutil` module.
- Automatically writes `.scs` files as uncompressed `.zip` archives, fully compatible with SCS Software's games.
- Clean, reusable module for integration into modding tools or automation scripts.

## 📦 Installation

```bash
pip install scsarchive
```

## 🛠️ Usage

```python
import scsarchive
scsarchive.register_scs_format()

import shutil
shutil.make_archive("mymod", "scs", root_dir="mod_files")
```

## 🧼 Optional Cleanup

```python
scsarchive.unregister_scs_format()
```

---

## 🌟 Why I Made This

Coming soon — a personal note from the author.

---

## ⚖️ License

```plaintext
MIT License

Copyright (c) 2025 Allie Nikol Modern

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

Made with 💖 by ~ Allie ~
