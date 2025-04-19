# 📦 Dict2Obj - Dictionary to Object Converter

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

🚀 Convert Python dictionaries into objects with attribute-style access.  
🔄 Supports nested dictionaries.  
🔍 Easily flatten dictionaries into dot notation.

---

## 🐜 Features

✅ Convert dictionary keys to object attributes  
✅ Return `None` for missing attributes instead of raising errors  
✅ Convert back to dictionary with `to_dict()`  
✅ Flatten to dot notation with `to_dot_dict()`  
✅ Supports non-string keys like integers and tuples  

---

## 🛠 Installation

```sh
pip install dict2objects
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

## 🧠 Access Patterns

Dict2Obj supports access to nested keys using attribute-style access and special handling of non-string keys.

```python
from dict2objects import Dict2Obj

data = {
    "user": {
        "name": "Alice",
        "age": 30,
        (1, 2): "coordinates"
    },
    100: "century",
    "details": {
        "nested": {
            "value": 42
        }
    }
}

obj = Dict2Obj(data)

print(obj.user.name)          # Alice
print(obj.details.nested.value)  # 42
print(obj.to_dict()[(1, 2)])     # coordinates
print(obj.to_dict()[100])        # century
```

### 🔍 Access Table

| Description                          | Access Pattern                          | Output        |
|--------------------------------------|-----------------------------------------|---------------|
| ✅ Top-level key (string)             | `obj.user.name`                         | `"Alice"`     |
| ❓ Nested key                         | `obj.details.nested.value`              | `42`          |
| 🧩 Non-string tuple key (original)   | `obj.to_dict()[(1, 2)]`                 | `"coordinates"`|
| 📦 Non-string integer key (original) | `obj.to_dict()[100]`                    | `"century"`   |
| 📜 Missing key                       | `obj.unknown`                           | `None`        |

---

## 📁 Project Structure

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
   pip install -e .
   ```
3. Run tests:
   ```sh
   python -m unittest discover tests
   ```

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### 🌟 **Like this project? Give it a star ⭐ on GitHub!**

