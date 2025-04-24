"""
python-hash : A Python package for password hashing and comparision using bcrypt
"""

from .core import generate_hash_from_text, compare_hash_and_text

__all__ = ["generate_hash_from_text", "compare_hash_and_text"]
__version__ = "1.0.0"