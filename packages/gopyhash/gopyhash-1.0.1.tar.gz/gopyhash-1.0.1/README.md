![pipeline](https://github.com/ihumaunkabir/gopyhash/actions/workflows/publish.yml/badge.svg)

# gopyhash

A package for password hashing and comparision using bcrypt. 

## Installation

```bash
pip install gopyhash
```
#### Golang Installation
Documentation here [go-hash](https://github.com/ihumaunkabir/go-hash/blob/master/README.md)

## Usage

```python
from gopyhash import generate_hash_from_text, compare_hash_and_text

# Generate a hash from a plain text (password)
password = "my_secure_password"
hashed_password = generate_hash_from_text(password)

# Compare and verify a plain text (password) and a generated hash
is_valid = compare_hash_and_text(hashed_password, "my_secure_password/others")
if is_valid:
    print("Password is correct!")
else:
    print("Password is incorrect!")
```

## Features

- Simple API for hashing passwords using bcrypt
- Verify passwords against existing hashes

## License

MIT License
