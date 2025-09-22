# test_library.py
"""Unit tests for major functions."""

import unittest
from book import Book
from member import Member
from library import Library
import issue_return as ir

class TestLibrary(unittest.TestCase):
    def test_add_and_get_book(self):
        lib = Library()
        b = Book("123", "Test Book", "Author", 2)
        lib.add_book(b)
        self.assertIn("123", lib.books)
        self.assertEqual(lib.get_book("123").title, "Test Book")

    def test_issue_and_return(self):
        lib = Library()
        b = Book("123", "T", "A", 1)
        lib.add_book(b)
        m = Member("M1", "Alice")
        lib.members[m.member_id] = m

        ok, msg = ir.issue_book(lib, "123", m)
        self.assertTrue(ok)
        self.assertEqual(lib.get_book("123").copies, 0)
        self.assertIn("123", m.borrowed_books)

        ok2, msg2 = ir.return_book(lib, "123", m)
        self.assertTrue(ok2)
        self.assertEqual(lib.get_book("123").copies, 1)
        self.assertNotIn("123", m.borrowed_books)

    def test_search(self):
        from search import search_by_title, search_by_author
        lib = Library()
        b1 = Book("1", "Alpha", "X", 2)
        b2 = Book("2", "Beta", "Y", 1)
        lib.add_book(b1); lib.add_book(b2)
        res = search_by_title(lib, "alpha")
        self.assertEqual(len(res), 1)
        res2 = search_by_author(lib, "y")
        self.assertEqual(len(res2), 1)

if __name__ == "__main__":
    unittest.main()
