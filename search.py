# search.py
"""Group E - Search module."""

def search_by_title(library, title: str):
    """Return list of Book objects matching title (case-insensitive, substring)."""
    t = title.lower()
    return [book for book in library.books.values() if t in book.title.lower()]

def search_by_author(library, author: str):
    """Return list of Book objects matching author (case-insensitive, substring)."""
    a = author.lower()
    return [book for book in library.books.values() if a in book.author.lower()]

def search_by_isbn(library, isbn: str):
    """Return Book object if ISBN exists, else None."""
    return library.get_book(isbn)
