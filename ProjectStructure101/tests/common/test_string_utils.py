import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))

from src.common.string_utils import (
    reverse_string,
    capitalize_words,
    count_vowels,
    remove_whitespace,
)


class TestStringUtils(unittest.TestCase):

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("Python"), "nohtyP")

    def test_capitalize_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")
        self.assertEqual(capitalize_words("python programming"), "Python Programming")

    def test_count_vowels(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("world"), 1)

    def test_remove_whitespace(self):
        self.assertEqual(remove_whitespace("hello world"), "helloworld")
        self.assertEqual(remove_whitespace("python programming"), "pythonprogramming")


if __name__ == "__main__":
    unittest.main()
