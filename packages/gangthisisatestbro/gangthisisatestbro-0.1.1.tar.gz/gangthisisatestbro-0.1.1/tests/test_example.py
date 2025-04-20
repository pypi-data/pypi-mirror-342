"""Tests for the example module."""

import unittest
from mypythonpackage import example


class TestExample(unittest.TestCase):
    """Test cases for the example module."""
    
    def test_get_greeting(self):
        """Test that get_greeting returns the expected greeting."""
        self.assertEqual(example.get_greeting("World"), "Hello, World!")
        self.assertEqual(example.get_greeting("Python"), "Hello, Python!")
    
    def test_add_numbers(self):
        """Test that add_numbers correctly adds two numbers."""
        self.assertEqual(example.add_numbers(1, 2), 3)
        self.assertEqual(example.add_numbers(-1, 1), 0)
        self.assertEqual(example.add_numbers(0, 0), 0)


if __name__ == "__main__":
    unittest.main() 