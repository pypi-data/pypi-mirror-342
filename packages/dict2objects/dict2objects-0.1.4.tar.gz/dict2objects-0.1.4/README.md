# 📦 Dict2Obj - Dictionary to Object Converter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/dict2objects.svg)](https://pypi.org/project/dict2objects/)

🚀 Convert Python dictionaries into objects with attribute-style access.  
🔄 Supports nested dictionaries.  
🔍 Easily flatten dictionaries into dot notation.

---

## 🐜 Features

✅ Convert dictionary keys to object attributes  
✅ Return `None` for missing attributes instead of raising errors  
✅ Convert back to dictionary with `to_dict()`  
✅ Flatten to dot notation with `to_dot_dict()`  

---

## 🛠 Installation

```sh
pip install dict2objects
```

Or using Poetry:

```sh
poetry add dict2objects
```

---

## 🚀 Usage

### **Basic Example**
```python
from dict2objects import Dict2Obj

data = {"name": "Alice", "age": 30, "address": {"city": "New York", "zip": "10001"}}
obj = Dict2Obj(data)

print(obj.name)  # Alice
print(obj.address.city)  # New York
print(obj.to_dict())  
# {'name': 'Alice', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}
```

---

### **Flatten Dictionary**
```python
print(obj.to_dot_dict())  
# {'name': 'Alice', 'age': 30, 'address.city': 'New York', 'address.zip': '10001'}
```

---

### **Handling Missing Keys**
```python
print(obj.salary)  # None (key does not exist)
print(obj.address.country)  # None (nested non-existent key)
```

---

## 📌 Access Patterns

| Access Type          | Example                            | Output        |
|----------------------|------------------------------------|---------------|
| Attribute-style      | `obj.name`                         | `'Alice'`     |
| Nested attribute     | `obj.address.city`                 | `'New York'`  |
| Missing attribute    | `obj.not_exist`                    | `None`        |
| Flatten dot notation| `obj.to_dot_dict()`                | `{...}`       |

```python
obj = Dict2Obj({"user": {"details": {"name": "Janardhan"}}})
print(obj.user.details.name)  # "Janardhan"
print(obj.user.age)  # None
print(obj.to_dot_dict())
# {'user.details.name': 'Janardhan'}
```

---

## 💂️ Project Structure

```
dict2obj/
├── dict2obj/
│   ├── __init__.py
│   ├── converter.py
├── tests/
│   ├── test_converter.py
├── setup.py
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
```

---

## 🛠 Development & Contribution

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/dict2obj.git
   cd dict2obj
   ```
2. Install dependencies:
   ```sh
   poetry install
   ```
3. Run tests:
   ```sh
   poetry run pytest
   ```

---

## 🐜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### 🌟 **Like this project? Give it a star ⭐ on GitHub!**
