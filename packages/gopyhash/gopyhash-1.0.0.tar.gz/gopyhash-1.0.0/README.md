![pipeline](https://github.com/ihumaunkabir/python-hash/actions/workflows/publish.yml/badge.svg)

# gopyhash

A package for password hashing and comparision using bcrypt. 

## Installation

```bash
pip install gopyhash
```

## Usage

```python
from gopyhash import generate_hash_from_text, compare_hash_and_text

# Generate a hash from a password
password = "my_secure_password"
hashed_password = generate_hash_from_text(password)

# Store hashed_password in your database
# ...

# Later, to verify a password
is_valid = compare_hash_and_text(hashed_password, "attempted_password")
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
