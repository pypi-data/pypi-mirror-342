# src/my_simple_package/__init__.py
"""
My Simple Package
~~~~~~~~~~~~~~~~~

A basic example package showing structure and packaging.
"""

# Import key functions/classes to make them available directly from the package
from .core import greet, farewell, SimpleCounter

# Define the package version (should match pyproject.toml)
__version__ = "0.1.0"

# Define what 'from my_simple_package import *' imports (optional but good practice)
__all__ = [
    'greet',
    'farewell',
    'SimpleCounter',
    '__version__',
]

# You could also initialize package-level things here if needed
# print("my_simple_package initialized") # Usually avoid printing on import
