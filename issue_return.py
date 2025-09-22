# issue_return.py
"""Group D - Issue and Return module."""

def issue_book(library, isbn: str, member):
    """
    Issue a book to a member if available.

    Args:
        library (Library): Library instance.
        isbn (str): Book ISBN.
        member (Member): Member instance.

    Returns:
        tuple(bool, str): (success, message)
    """
    isbn = str(isbn)
    book = library.get_book(isbn)
    if book is None:
        return False, "Book not found."
    if book.copies <= 0:
        return False, "No copies available."
    # issue
    book.copies -= 1
    member.borrow(isbn)
    return True, f"Book '{book.title}' issued to {member.name}."

def return_book(library, isbn: str, member):
    """
    Return a book from a member.

    Args:
        library (Library): Library instance.
        isbn (str): Book ISBN.
        member (Member): Member instance.

    Returns:
        tuple(bool, str): (success, message)
    """
    isbn = str(isbn)
    if member.return_book(isbn):
        book = library.get_book(isbn)
        if book:
            book.copies += 1
        return True, f"Book (ISBN: {isbn}) returned by {member.name}."
    return False, "This member did not borrow this book."
