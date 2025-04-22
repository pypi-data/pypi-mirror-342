# src/my_simple_package/core.py
"""Core functionality for my_simple_package."""

import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def greet(name: str) -> str:
    """
    Generates a friendly greeting message.

    Args:
        name: The name of the person or thing to greet. Must be a non-empty string.

    Returns:
        A greeting string in the format "Hello, [name]!".

    Raises:
        TypeError: If the input 'name' is not a string.
        ValueError: If the input 'name' is an empty string.
    """
    if not isinstance(name, str):
        logger.error(
            "Type error: Input 'name' must be a string, but got %s.", type(name).__name__)
        raise TypeError("Input 'name' must be a string.")
    if not name:
        logger.error("Value error: Input 'name' cannot be empty.")
        raise ValueError("'name' cannot be empty.")

    greeting = f"Hello, {name}!"
    logger.info("Generated greeting for '%s'.", name)
    return greeting


def farewell(name: str) -> str:
    """
    Generates a farewell message. (Example of adding another function)

    Args:
        name: The name for the farewell. Must be a non-empty string.

    Returns:
        A farewell string.

    Raises:
        TypeError: If 'name' is not a string.
        ValueError: If 'name' is empty.
    """
    # Reuse validation logic or keep it simple for example
    if not isinstance(name, str):
        raise TypeError("Input 'name' must be a string.")
    if not name:
        raise ValueError("'name' cannot be empty.")

    return f"Goodbye, {name}!"

# Example of a class if needed


class SimpleCounter:
    """A basic counter class."""

    def __init__(self):
        self._count = 0

    def increment(self):
        self._count += 1

    def get_count(self) -> int:
        return self._count
