# Library Management System

A modular, object-oriented Library Management System developed collaboratively using Python and GitHub. This project demonstrates collaborative software development practices with multiple teams working on different modules that integrate into a single working application.

## 🚀 Features

- **Book Management**: Add, remove, and track library books with ISBN, title, author, and copies
- **Member Management**: Register and manage library members with borrowing history
- **Issue & Return System**: Handle book borrowing and returning with availability tracking
- **Search Functionality**: Search books by title, author, or ISBN
- **Authentication System**: Basic login system for librarians and members
- **User Interface**: Interactive menu-driven application
- **Unit Testing**: Comprehensive test coverage for all modules

## 📁 Project Structure

```
library-management-system/
├── book.py                        # Book class implementation
├── member.py                      # Member class implementation  
├── library.py                     # Library class implementation
├── issue_return.py                # Book issue and return functionality
├── search.py                      # Search functionality
├── auth_system.py                 # Authentication system
├── library_management_system.py   # Main application interface
├── test_library.py                # Unit tests
├── README.md                      # Project documentation
└── .github/
    └── PULL_REQUEST_TEMPLATE.md   # PR template
```

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```

2. **Requirements**
   - Python 3.6 or higher
   - No external dependencies required

3. **Run the application**
   ```bash
   python library_management_system.py
   ```

## 🎮 Usage

### Running the Main Application
```bash
python library_management_system.py
```

### Running Tests
```bash
python -m pytest test_library.py
```

### Example Usage
```python
from book import Book
from member import Member
from library import Library

# Create library instance
library = Library()

# Add a book
book = Book('9781234567890', 'Python Programming', 'John Doe', 3)
library.add_book(book)

# Register a member
member = Member('M001', 'Alice Smith')

# Issue a book
issue_book(library, '9781234567890', member)
```

## 📚 Module Details

### Group A: Book Module (`book.py`)
**Purpose**: Define the structure of a book
- Manages book attributes: ISBN, title, author, copies
- Stores book data for the library system

### Group B: Member Module (`member.py`)  
**Purpose**: Manage library members
- Tracks member ID, name, and borrowed books
- Maintains borrowing history

### Group C: Library Module (`library.py`)
**Purpose**: Manage library's book collection  
- Add, remove, and list books
- Central book repository management

### Group D: Issue and Return Module (`issue_return.py`)
**Purpose**: Handle book issuance and return
- Updates book availability
- Manages borrowing transactions

### Group E: Search Module (`search.py`)
**Purpose**: Enable book search functionality
- Search by title, author, or ISBN
- Case-insensitive search capabilities

### Group F: Authentication Module (`auth_system.py`)
**Purpose**: User authentication system
- Basic login for librarians and members
- User credential verification

### Group G: Main Application Interface (`library_management_system.py`)
**Purpose**: Integrate all modules
- User-friendly menu system
- Coordinate all library operations

### Group H: Unit Testing Module (`test_library.py`)
**Purpose**: Ensure system reliability
- Comprehensive test coverage
- Validates all module functionality

## 🔧 Development Guidelines

### Code Standards
- Use consistent variable names: `isbn`, `title`, `author`, `copies`, `member_id`
- Follow agreed class/function names: `Book`, `Member`, `Library`
- Document all functions and classes with proper docstrings
- Report interface changes to Group G immediately
- Avoid changes after first integration unless approved

### Variable Naming Convention
```python
# Books
isbn, title, author, copies

# Members  
member_id, name, borrowed_books

# Library operations
library, book, member
```

## 🤝 Contributing

This project follows a structured collaborative workflow:

### Branch Structure
- `main` - Production branch (protected)
- `group-a-book` - Book module development
- `group-b-member` - Member module development  
- `group-c-library` - Library module development
- `group-d-issue-return` - Issue/Return functionality
- `group-e-search` - Search functionality
- `group-f-auth` - Authentication system
- `group-g-main-interface` - Main application interface
- `group-h-testing` - Unit testing

### Workflow Process

1. **Development**: Work only on assigned branches
2. **Pull Requests**: Submit PR to `main` when module is complete
3. **Code Review**: All PRs must be reviewed before merging  
4. **Testing**: Group H ensures integrated functionality
5. **Integration**: Merge only after successful review and testing

### Pull Request Guidelines
- Use clear, descriptive PR descriptions
- Include type of change (feature, bugfix, etc.)
- Complete the PR checklist
- Reference related issues
- Ensure all tests pass

## 🧪 Testing

The project includes comprehensive unit tests covering:
- Book creation and management
- Member registration and tracking
- Library operations
- Issue and return functionality  
- Search capabilities
- Authentication system

Run tests with:
```bash
python -m pytest test_library.py -v
```

## 🏗️ Architecture

The system follows object-oriented design principles:

- **Separation of Concerns**: Each module has a specific responsibility
- **Modularity**: Components can be developed and tested independently  
- **Integration**: All modules work together through well-defined interfaces
- **Testability**: Each module includes comprehensive test coverage

## 📋 Final Deliverables

- ✅ Individual module files (`book.py`, `member.py`, etc.)
- ✅ Integrated application (`library_management_system.py`)
- ✅ Comprehensive testing suite (`test_library.py`)
- ✅ Complete documentation (`README.md`, PR template)
- ✅ GitHub workflow setup with branch protection

## 📄 License

This project is developed as part of a collaborative learning exercise.

## 👥 Contributors

- **Group A**: Book Module Implementation
- **Group B**: Member Module Implementation  
- **Group C**: Library Module Implementation
- **Group D**: Issue & Return Functionality
- **Group E**: Search Functionality
- **Group F**: Authentication System
- **Group G**: Main Application Interface
- **Group H**: Unit Testing & Quality Assurance

## 📞 Support

For questions about specific modules or integration issues, please:
1. Check existing GitHub issues
2. Create a new issue with appropriate labels
3. Contact the relevant group for module-specific questions
4. Reach out to Group G for integration concerns

---

**Happy coding! 📚✨**