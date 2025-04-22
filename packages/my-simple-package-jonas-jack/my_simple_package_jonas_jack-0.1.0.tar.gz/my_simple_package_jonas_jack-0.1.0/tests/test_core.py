# tests/test_core.py
import unittest
import sys
import os

# A common pattern to make the 'src' directory importable in tests
# This assumes the tests are run from the project root directory
# Or that the test runner handles the path correctly (like pytest often does)
# Alternatively, install the package in editable mode (`pip install -e .`) before running tests
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Now import from the package
from my_simple_package import greet, farewell, SimpleCounter  # Use package import


class TestGreetFunction(unittest.TestCase):
    """Tests for the greet function."""

    def test_greet_standard_name(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

    def test_greet_name_with_spaces(self):
        self.assertEqual(greet("Bob Smith"), "Hello, Bob Smith!")

    def test_greet_raises_type_error_for_non_string(self):
        with self.assertRaisesRegex(TypeError, "Input 'name' must be a string"):
            greet(123)  # type: ignore
        with self.assertRaisesRegex(TypeError, "Input 'name' must be a string"):
            greet(None)  # type: ignore
        with self.assertRaisesRegex(TypeError, "Input 'name' must be a string"):
            greet(["a", "list"])  # type: ignore

    def test_greet_raises_value_error_for_empty_string(self):
        with self.assertRaisesRegex(ValueError, "'name' cannot be empty"):
            greet("")


class TestFarewellFunction(unittest.TestCase):
    """Tests for the farewell function."""

    def test_farewell_standard_name(self):
        self.assertEqual(farewell("Charlie"), "Goodbye, Charlie!")

    def test_farewell_raises_type_error(self):
        with self.assertRaises(TypeError):
            farewell(456)  # type: ignore

    def test_farewell_raises_value_error(self):
        with self.assertRaises(ValueError):
            farewell("")


class TestSimpleCounter(unittest.TestCase):
    """Tests for the SimpleCounter class."""

    def test_counter_starts_at_zero(self):
        counter = SimpleCounter()
        self.assertEqual(counter.get_count(), 0)

    def test_increment_increases_count(self):
        counter = SimpleCounter()
        counter.increment()
        self.assertEqual(counter.get_count(), 1)
        counter.increment()
        counter.increment()
        self.assertEqual(counter.get_count(), 3)


if __name__ == '__main__':
    # Allows running tests directly using 'python tests/test_core.py'
    # Note: This might require adjusting sys.path if run this way,
    # it's generally better to use a test runner from the root.
    # Example: python -m unittest discover tests
    unittest.main()
