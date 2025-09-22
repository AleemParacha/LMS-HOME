# member.py
"""Group B - Member module."""

class Member:
    """
    Represents a library member.

    Attributes:
        member_id (str): Unique member identifier.
        name (str): Member name.
        borrowed_books (list[str]): List of borrowed book ISBNs.
    """
    def __init__(self, member_id: str, name: str):
        self.member_id = str(member_id)
        self.name = name
        self.borrowed_books = []

    def borrow(self, isbn: str):
        """Record borrowing a book by ISBN."""
        self.borrowed_books.append(str(isbn))

    def return_book(self, isbn: str):
        """Remove a borrowed book by ISBN if present."""
        isbn = str(isbn)
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)
            return True
        return False

    def __repr__(self):
        return f"Member(member_id={self.member_id!r}, name={self.name!r}, borrowed_books={self.borrowed_books})"
