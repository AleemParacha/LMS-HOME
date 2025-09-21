# library.py
"""Group C - Library module."""

from book import Book

class Library:
    """
    Manages the library's book collection.

    Attributes:
        books (dict[str, Book]): Map ISBN -> Book object.
        members (dict[str, Member]): Map member_id -> Member object (populated externally).
    """
    def __init__(self):
        self.books = {}    # isbn -> Book
        self.members = {}  # member_id -> Member

    def add_book(self, book: Book):
        """Add a book to the collection. If ISBN exists, increment copies."""
        if book.isbn in self.books:
            self.books[book.isbn].copies += book.copies
        else:
            self.books[book.isbn] = book

    def remove_book(self, isbn: str):
        """Remove a book from the collection by ISBN."""
        isbn = str(isbn)
        if isbn in self.books:
            del self.books[isbn]
            return True
        return False

    def list_books(self):
        """Return list of Book objects."""
        return list(self.books.values())

    def get_book(self, isbn: str):
        """Return Book or None."""
        return self.books.get(str(isbn))
