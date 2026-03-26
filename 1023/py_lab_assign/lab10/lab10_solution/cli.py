"""
COMP 1023 Lab 10: Library Management System - CLI Testing Program
This program provides a command-line interface to test the library management system.
"""

from book import Book, FictionBook, ReferenceBook, Magazine
from member import Member, StudentMember, TeacherMember, GuestMember
from library import Library


def print_separator():
    """Print a separator line."""
    print("=" * 80)


def print_header(text):
    """Print a formatted header."""
    print_separator()
    print(f"  {text}")
    print_separator()


def initialize_sample_library():
    """Initialize a library with sample data."""
    library = Library("HKUST Library")
    
    # Add sample books
    books = [
        FictionBook("Harry Potter and the Philosopher's Stone", "J.K. Rowling", "978-0439708180", 1997, "Fantasy"),
        FictionBook("The Hobbit", "J.R.R. Tolkien", "978-0547928227", 1937, "Fantasy"),
        FictionBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian"),
        FictionBook("To Kill a Mockingbird", "Harper Lee", "978-0061120084", 1960, "Classic"),
        ReferenceBook("Oxford English Dictionary", "Oxford University Press", "978-0198611868", 1989, "Language"),
        ReferenceBook("Encyclopedia Britannica", "Britannica Group", "978-1593398378", 2010, "General Knowledge"),
        Magazine("National Geographic", "National Geographic Society", "ISSN-0027-9358", 2024, 11, "November"),
        Magazine("Time Magazine", "Time USA, LLC", "ISSN-0040-781X", 2024, 45, "December"),
        Book("Clean Code", "Robert C. Martin", "978-0132350884", 2008),
        Book("Introduction to Algorithms", "Thomas H. Cormen", "978-0262033844", 2009),
    ]
    
    for book in books:
        library.add_book(book)
    
    # Add sample members
    members = [
        StudentMember("Alice Wong", "S001", "20012345"),
        StudentMember("Bob Chen", "S002", "20012346"),
        StudentMember("Carol Liu", "S003", "20012347"),
        TeacherMember("Dr. Sarah Johnson", "T001", "Computer Science"),
        TeacherMember("Prof. David Lee", "T002", "Mathematics"),
        GuestMember("Charlie Brown", "G001"),
        GuestMember("Diana Prince", "G002"),
    ]
    
    for member in members:
        library.register_member(member)
    
    return library


def display_all_books(library):
    """Display all books in the library."""
    print_header("ALL BOOKS IN LIBRARY")
    books = library.get_all_books()
    
    if not books:
        print("No books in the library.")
        return
    
    for i, book in enumerate(books, 1):
        print(f"{i}. {book.get_info()}")


def display_available_books(library):
    """Display all available books."""
    print_header("AVAILABLE BOOKS")
    books = library.get_available_books()
    
    if not books:
        print("No available books.")
        return
    
    for i, book in enumerate(books, 1):
        print(f"{i}. {book.get_info()}")


def display_all_members(library):
    """Display all members."""
    print_header("ALL MEMBERS")
    members = library.get_all_members()
    
    if not members:
        print("No registered members.")
        return
    
    for i, member in enumerate(members, 1):
        print(f"{i}. {member.get_info()}")


def display_member_borrowed_books(library):
    """Display a member's borrowed books."""
    print_header("VIEW MEMBER'S BORROWED BOOKS")
    member_id = input("Enter member ID: ").strip()
    
    member = library.find_member_by_id(member_id)
    if member is None:
        print(f"Error: Member '{member_id}' not found.")
        return
    
    borrowed_books = member.get_borrowed_books()
    
    print(f"\n{member.get_info()}")
    print(f"Borrowed books:")
    
    if not borrowed_books:
        print("  No books borrowed.")
    else:
        for i, book in enumerate(borrowed_books, 1):
            print(f"  {i}. {book.get_info()}")


def search_books(library):
    """Search for books."""
    print_header("SEARCH BOOKS")
    print("1. Search by title")
    print("2. Search by author")
    
    choice = input("Enter your choice (1-2): ").strip()
    
    if choice == '1':
        keyword = input("Enter title keyword: ").strip()
        results = library.search_books(keyword, search_by='title')
    elif choice == '2':
        keyword = input("Enter author keyword: ").strip()
        results = library.search_books(keyword, search_by='author')
    else:
        print("Invalid choice.")
        return
    
    print(f"\nSearch results ({len(results)} found):")
    if not results:
        print("No books found.")
    else:
        for i, book in enumerate(results, 1):
            print(f"{i}. {book.get_info()}")


def borrow_book(library):
    """Process a book borrowing request."""
    print_header("BORROW A BOOK")
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()
    
    success, message = library.lend_book(member_id, isbn)
    
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")


def return_book(library):
    """Process a book return."""
    print_header("RETURN A BOOK")
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()
    
    success, message = library.return_book(member_id, isbn)
    
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")


def display_library_stats(library):
    """Display library statistics."""
    print_header("LIBRARY STATISTICS")
    stats = library.get_library_stats()
    
    print(f"Library Name: {library.name}")
    print(f"Total Books: {stats['total_books']}")
    print(f"  - Available: {stats['available_books']}")
    print(f"  - Borrowed: {stats['borrowed_books']}")
    print(f"  - Reference (In-Library Only): {stats['reference_books']}")
    print(f"Total Members: {stats['total_members']}")


def run_tests():
    """Run automated tests to demonstrate functionality."""
    print_header("RUNNING AUTOMATED TESTS")
    
    library = initialize_sample_library()
    
    print("\n[TEST 1] Student borrows a fiction book")
    success, msg = library.lend_book("S001", "978-0439708180")
    print(f"  Result: {msg}")
    
    print("\n[TEST 2] Teacher borrows multiple books")
    library.lend_book("T001", "978-0547928227")
    library.lend_book("T001", "978-0132350884")
    success, msg = library.lend_book("T001", "978-0262033844")
    print(f"  Result: {msg}")
    
    print("\n[TEST 3] Guest tries to borrow reference book")
    success, msg = library.lend_book("G001", "978-0198611868")
    print(f"  Result: {msg}")
    
    print("\n[TEST 4] Guest borrows magazine")
    success, msg = library.lend_book("G001", "ISSN-0027-9358")
    print(f"  Result: {msg}")
    
    print("\n[TEST 5] Guest tries to exceed borrowing limit")
    library.lend_book("G001", "ISSN-0040-781X")
    success, msg = library.lend_book("G001", "978-0451524935")
    print(f"  Result: {msg}")
    
    print("\n[TEST 6] Student returns a book")
    success, msg = library.return_book("S001", "978-0439708180")
    print(f"  Result: {msg}")
    
    print("\n[TEST 7] Search books by title")
    results = library.search_books("Harry", search_by='title')
    print(f"  Found {len(results)} book(s) matching 'Harry'")
    
    print("\n[TEST 8] Display library statistics")
    stats = library.get_library_stats()
    print(f"  Total books: {stats['total_books']}, Borrowed: {stats['borrowed_books']}")
    
    print_separator()
    print("Tests completed! You can now use the interactive menu.")
    
    return library


def main():
    """Main function to run the CLI."""
    print_header("COMP 1023 Lab 10: Library Management System")
    print("\nWelcome to the Library Management System CLI!")
    
    # Ask if user wants to run tests
    run_test = input("\nWould you like to run automated tests first? (y/n): ").strip().lower()
    
    if run_test == 'y':
        library = run_tests()
    else:
        print("\nInitializing library with sample data...")
        library = initialize_sample_library()
        print("Library initialized successfully!")
    
    # Main menu loop
    while True:
        print("\n")
        print_header("MAIN MENU")
        print("1. Display all books")
        print("2. Display available books")
        print("3. Display all members")
        print("4. View member's borrowed books")
        print("5. Search books")
        print("6. Borrow a book")
        print("7. Return a book")
        print("8. Display library statistics")
        print("9. Exit")
        print_separator()
        
        choice = input("Enter your choice (1-9): ").strip()
        
        if choice == '1':
            display_all_books(library)
        elif choice == '2':
            display_available_books(library)
        elif choice == '3':
            display_all_members(library)
        elif choice == '4':
            display_member_borrowed_books(library)
        elif choice == '5':
            search_books(library)
        elif choice == '6':
            borrow_book(library)
        elif choice == '7':
            return_book(library)
        elif choice == '8':
            display_library_stats(library)
        elif choice == '9':
            print("\nThank you for using the Library Management System!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

