# library_management_system.py
"""Main Application Interface with Tkinter GUI."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from book import Book
from member import Member
from library import Library
import issue_return as ir
import search as search_mod
import auth_system

class LMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("900x600")
        self.library = Library()
        self.user_db = dict(auth_system.DEFAULT_USER_DB)  # mutable copy
        self.current_user = None  # dict from user_db entries
        self._build_demo_data()
        self._build_ui()

    def _build_demo_data(self):
        # Demo books and members for faster testing
        demo_books = [
            Book("9780140449136", "The Odyssey", "Homer", 3),
            Book("9780679783275", "Pride and Prejudice", "Jane Austen", 2),
            Book("9780553213119", "Dracula", "Bram Stoker", 1),
        ]
        for b in demo_books:
            self.library.add_book(b)

        # demo members
        demo_members = [
            Member("M001", "Alice"),
            Member("M002", "Bob"),
        ]
        for m in demo_members:
            self.library.members[m.member_id] = m
            # add user account for members
            self.user_db[f"user_{m.member_id}"] = {"password": "password", "role": "member", "member_id": m.member_id}

    def _build_ui(self):
        # Top menu
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        account_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Account", menu=account_menu)
        account_menu.add_command(label="Login", command=self.login_dialog)
        account_menu.add_command(label="Logout", command=self.logout)
        account_menu.add_separator()
        account_menu.add_command(label="Exit", command=self.quit)

        # Left frame: controls
        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left, text="Library Actions", font=("TkDefaultFont", 12, "bold")).pack(pady=(0,10))
        ttk.Button(left, text="Add Book", command=self.add_book_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="Remove Book", command=self.remove_book_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="Add Member", command=self.add_member_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="Search Books", command=self.search_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="Issue Book", command=self.issue_book_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="Return Book", command=self.return_book_dialog).pack(fill=tk.X, pady=2)
        ttk.Button(left, text="Refresh List", command=self.refresh_lists).pack(fill=tk.X, pady=2)

        # Right frame: lists
        right = ttk.Frame(self, padding=10)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.books_tree = ttk.Treeview(right, columns=("ISBN", "Title", "Author", "Copies"), show="headings", height=10)
        for col in ("ISBN", "Title", "Author", "Copies"):
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=150 if col != "Copies" else 60)
        ttk.Label(right, text="Books").pack(anchor=tk.W)
        self.books_tree.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        self.members_tree = ttk.Treeview(right, columns=("Member ID", "Name", "Borrowed"), show="headings", height=6)
        for col in ("Member ID", "Name", "Borrowed"):
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=200)
        ttk.Label(right, text="Members").pack(anchor=tk.W)
        self.members_tree.pack(fill=tk.BOTH, expand=True)

        # status bar
        self.status_var = tk.StringVar(value="Not logged in")
        status = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

        self.refresh_lists()

    # ------------------ account ------------------
    def login_dialog(self):
        dlg = LoginDialog(self, self.user_db)
        self.wait_window(dlg)
        if dlg.result:
            username, user_rec = dlg.result
            self.current_user = {"username": username, **user_rec}
            self.status_var.set(f"Logged in as {username} ({user_rec['role']})")
            messagebox.showinfo("Login", f"Welcome {username}!")
        else:
            # canceled or failed
            pass

    def logout(self):
        if self.current_user:
            self.current_user = None
            self.status_var.set("Not logged in")
            messagebox.showinfo("Logout", "Logged out successfully.")
        else:
            messagebox.showinfo("Logout", "No user currently logged in.")

    # ------------------ dialogs and actions ------------------
    def add_book_dialog(self):
        if not self._require_librarian():
            return
        dlg = AddBookDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            isbn, title, author, copies = dlg.result
            book = Book(isbn, title, author, int(copies))
            self.library.add_book(book)
            self.refresh_lists()
            messagebox.showinfo("Add Book", f"Added book: {title}")

    def remove_book_dialog(self):
        if not self._require_librarian():
            return
        isbn = simpledialog.askstring("Remove Book", "Enter ISBN to remove:")
        if isbn:
            if self.library.remove_book(isbn):
                self.refresh_lists()
                messagebox.showinfo("Remove Book", "Book removed.")
            else:
                messagebox.showerror("Remove Book", "Book not found.")

    def add_member_dialog(self):
        if not self._require_librarian():
            return
        member_id = simpledialog.askstring("New Member", "Enter member ID:")
        name = simpledialog.askstring("New Member", "Enter member name:")
        if member_id and name:
            if member_id in self.library.members:
                messagebox.showerror("Add Member", "Member ID already exists.")
                return
            m = Member(member_id, name)
            self.library.members[member_id] = m
            # create a user account for this member (default password)
            self.user_db[f"user_{member_id}"] = {"password": "password", "role": "member", "member_id": member_id}
            self.refresh_lists()
            messagebox.showinfo("Add Member", f"Member {name} added with ID {member_id} (default password: 'password').")

    def search_dialog(self):
        dlg = SearchDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            mode, query = dlg.result
            if mode == "title":
                results = search_mod.search_by_title(self.library, query)
            elif mode == "author":
                results = search_mod.search_by_author(self.library, query)
            else:
                b = search_mod.search_by_isbn(self.library, query)
                results = [b] if b else []
            if not results:
                messagebox.showinfo("Search", "No results.")
                return
            # show results
            res_str = "\n".join([f"{b.isbn} | {b.title} | {b.author} | copies: {b.copies}" for b in results])
            messagebox.showinfo("Search Results", res_str)

    def issue_book_dialog(self):
        if not self._require_authenticated():
            return
        isbn = simpledialog.askstring("Issue Book", "Enter ISBN to issue:")
        member_id = simpledialog.askstring("Issue Book", "Enter member ID:")
        if not (isbn and member_id):
            return
        member = self.library.members.get(member_id)
        if not member:
            messagebox.showerror("Issue Book", "Member not found.")
            return
        success, msg = ir.issue_book(self.library, isbn, member)
        self.refresh_lists()
        if success:
            messagebox.showinfo("Issue Book", msg)
        else:
            messagebox.showerror("Issue Book", msg)

    def return_book_dialog(self):
        if not self._require_authenticated():
            return
        isbn = simpledialog.askstring("Return Book", "Enter ISBN to return:")
        member_id = simpledialog.askstring("Return Book", "Enter member ID:")
        if not (isbn and member_id):
            return
        member = self.library.members.get(member_id)
        if not member:
            messagebox.showerror("Return Book", "Member not found.")
            return
        success, msg = ir.return_book(self.library, isbn, member)
        self.refresh_lists()
        if success:
            messagebox.showinfo("Return Book", msg)
        else:
            messagebox.showerror("Return Book", msg)

    # ------------------ helpers ------------------
    def refresh_lists(self):
        # books
        for r in self.books_tree.get_children():
            self.books_tree.delete(r)
        for b in self.library.list_books():
            self.books_tree.insert("", tk.END, values=(b.isbn, b.title, b.author, b.copies))
        # members
        for r in self.members_tree.get_children():
            self.members_tree.delete(r)
        for m in self.library.members.values():
            borrowed = ", ".join(m.borrowed_books) if m.borrowed_books else "-"
            self.members_tree.insert("", tk.END, values=(m.member_id, m.name, borrowed))

    def _require_librarian(self):
        if self.current_user and self.current_user.get("role") == "librarian":
            return True
        messagebox.showerror("Permission Denied", "Librarian login required for this action.")
        return False

    def _require_authenticated(self):
        if self.current_user:
            return True
        messagebox.showerror("Authentication Required", "Please login to perform this action.")
        return False

# ---------- Dialog classes ----------
class LoginDialog(tk.Toplevel):
    def __init__(self, parent, user_db):
        super().__init__(parent)
        self.title("Login")
        self.user_db = user_db
        self.result = None
        self.build()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username = ttk.Entry(frm)
        self.username.grid(row=0, column=1)
        ttk.Label(frm, text="Password:").grid(row=1, column=0, sticky=tk.W)
        self.password = ttk.Entry(frm, show="*")
        self.password.grid(row=1, column=1)
        btn = ttk.Button(frm, text="Login", command=self._attempt)
        btn.grid(row=2, column=0, columnspan=2, pady=5)

    def _attempt(self):
        u = self.username.get()
        p = self.password.get()
        ok, rec = auth_system.authenticate(u, p, self.user_db)
        if ok:
            self.result = (u, rec)
            self.destroy()
        else:
            messagebox.showerror("Login failed", "Invalid credentials.")

class AddBookDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Book")
        self.result = None
        self.build()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="ISBN:").grid(row=0, column=0, sticky=tk.W)
        self.isbn = ttk.Entry(frm); self.isbn.grid(row=0, column=1)
        ttk.Label(frm, text="Title:").grid(row=1, column=0, sticky=tk.W)
        self.title_e = ttk.Entry(frm); self.title_e.grid(row=1, column=1)
        ttk.Label(frm, text="Author:").grid(row=2, column=0, sticky=tk.W)
        self.author = ttk.Entry(frm); self.author.grid(row=2, column=1)
        ttk.Label(frm, text="Copies:").grid(row=3, column=0, sticky=tk.W)
        self.copies = ttk.Entry(frm); self.copies.grid(row=3, column=1)
        ttk.Button(frm, text="Add", command=self._on_add).grid(row=4, column=0, columnspan=2, pady=5)

    def _on_add(self):
        try:
            copies = int(self.copies.get())
        except ValueError:
            messagebox.showerror("Invalid", "Copies must be an integer.")
            return
        if not (self.isbn.get() and self.title_e.get() and self.author.get()):
            messagebox.showerror("Invalid", "All fields are required.")
            return
        self.result = (self.isbn.get(), self.title_e.get(), self.author.get(), copies)
        self.destroy()

class SearchDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Search Books")
        self.result = None
        self.build()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="Search by:").grid(row=0, column=0, sticky=tk.W)
        self.mode = tk.StringVar(value="title")
        ttk.Radiobutton(frm, text="Title", variable=self.mode, value="title").grid(row=0, column=1)
        ttk.Radiobutton(frm, text="Author", variable=self.mode, value="author").grid(row=0, column=2)
        ttk.Radiobutton(frm, text="ISBN", variable=self.mode, value="isbn").grid(row=0, column=3)
        ttk.Label(frm, text="Query:").grid(row=1, column=0, sticky=tk.W)
        self.query = ttk.Entry(frm); self.query.grid(row=1, column=1, columnspan=3, sticky=tk.EW)
        ttk.Button(frm, text="Search", command=self._on_search).grid(row=2, column=0, columnspan=4, pady=5)

    def _on_search(self):
        q = self.query.get().strip()
        if not q:
            messagebox.showerror("Invalid", "Query must not be empty.")
            return
        self.result = (self.mode.get(), q)
        self.destroy()

# ------------- run -------------
if __name__ == "__main__":
    app = LMSApp()
    app.mainloop()
