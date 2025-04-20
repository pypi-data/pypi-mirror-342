> # check if the given module is is-odd

## Install
---
Install with [pip](https://pypi.org/project/pip/):
```sh
pip install is-is-odd
```

## Usage
---
```python
import is_is_odd
import is_odd

print(is_is_odd(is_odd)) #=> True

print(is_is_odd(lambda: None)) #=> False

print(is_is_odd(lambda: print("I'm is_odd"))) #=> False
```

## Why
---
some modules are not is-odd but they might make you think they're is-odd, this package helps you identifies these modules with a simple interface

