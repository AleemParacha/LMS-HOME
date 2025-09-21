# book.py
"""Group A - Book module."""

class Book:
    """
    Represents a book in the library.

    Attributes:
        isbn (str): International Standard Book Number (unique).
        title (str): Book title.
        author (str): Book author.
        copies (int): Number of available copies.
    """
    def __init__(self, isbn: str, title: str, author: str, copies: int):
        self.isbn = str(isbn)
        self.title = title
        self.author = author
        self.copies = int(copies)

    def __repr__(self):
        return f"Book(isbn={self.isbn!r}, title={self.title!r}, author={self.author!r}, copies={self.copies})"
