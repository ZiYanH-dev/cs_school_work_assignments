"""
COMP 1023 Lab 10: Library Management System - Library Module
This module contains the Library class for managing the library system.
"""

from book import Book, FictionBook, ReferenceBook, Magazine
from member import Member, StudentMember, TeacherMember, GuestMember


class Library:
    """Main library management system."""
    
    def __init__(self, name):
        """
        Initialize a Library object.
        
        Args:
            name (str): The name of the library
        """
        self.name = name
        self.books = {}  # ISBN -> Book object
        self.members = {}  # member_id -> Member object
    
    def add_book(self, book):
        """
        Add a book to the library.
        
        Args:
            book (Book): The book to add
            
        Returns:
            bool: True if successful, False if book already exists
        """
        if book.isbn not in self.books:
            self.books[book.isbn] = book
            return True
        return False
    
    def register_member(self, member):
        """
        Register a new member.
        
        Args:
            member (Member): The member to register
            
        Returns:
            bool: True if successful, False if member already exists
        """
        if member.member_id not in self.members:
            self.members[member.member_id] = member
            return True
        return False
    
    def find_book_by_isbn(self, isbn):
        """
        Find a book by its ISBN.
        
        Args:
            isbn (str): The ISBN to search for
            
        Returns:
            Book or None: The book if found, None otherwise
        """
        return self.books.get(isbn)
    
    def find_member_by_id(self, member_id):
        """
        Find a member by their ID.
        
        Args:
            member_id (str): The member ID to search for
            
        Returns:
            Member or None: The member if found, None otherwise
        """
        return self.members.get(member_id)
    
    def lend_book(self, member_id, isbn):
        """
        Process a book lending request.
        
        Args:
            member_id (str): The member ID
            isbn (str): The book ISBN
            
        Returns:
            tuple: (bool, str) - Success status and message
        """
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_isbn(isbn)
        
        if member is None:
            return False, "Member not found"
        
        if book is None:
            return False, "Book not found"
        
        if not book.available:
            return False, f"Book '{book.title}' is currently borrowed"
        
        if isinstance(book, ReferenceBook):
            return False, f"Reference book '{book.title}' cannot be borrowed (In-Library Use Only)"
        
        if not member.can_borrow():
            return False, f"Member has reached borrowing limit ({member.max_books} books)"
        
        if member.borrow_book(book):
            return True, f"Successfully lent '{book.title}' to {member.name}"
        
        return False, "Failed to lend book"
    
    def return_book(self, member_id, isbn):
        """
        Process a book return.
        
        Args:
            member_id (str): The member ID
            isbn (str): The book ISBN
            
        Returns:
            tuple: (bool, str) - Success status and message
        """
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_isbn(isbn)
        
        if member is None:
            return False, "Member not found"
        
        if book is None:
            return False, "Book not found"
        
        if member.return_book(book):
            return True, f"Successfully returned '{book.title}' from {member.name}"
        
        return False, f"Member did not borrow this book"
    
    def search_books(self, keyword, search_by='title'):
        """
        Search for books by title or author.
        
        Args:
            keyword (str): The search keyword
            search_by (str): 'title' or 'author'
            
        Returns:
            list: List of matching Book objects
        """
        results = []
        keyword_lower = keyword.lower()
        
        for book in self.books.values():
            if search_by == 'title' and keyword_lower in book.title.lower():
                results.append(book)
            elif search_by == 'author' and keyword_lower in book.author.lower():
                results.append(book)
        
        return results
    
    def get_available_books(self):
        """
        Get all available books (excluding reference books).
        
        Returns:
            list: List of available Book objects
        """
        return [book for book in self.books.values() 
                if book.available and not isinstance(book, ReferenceBook)]
    
    def get_all_books(self):
        """
        Get all books in the library.
        
        Returns:
            list: List of all Book objects
        """
        return list(self.books.values())
    
    def get_all_members(self):
        """
        Get all registered members.
        
        Returns:
            list: List of all Member objects
        """
        return list(self.members.values())
    
    def get_borrowed_books(self):
        """
        Get all currently borrowed books.
        
        Returns:
            list: List of borrowed Book objects
        """
        return [book for book in self.books.values() if not book.available]
    
    def get_library_stats(self):
        """
        Get library statistics.
        
        Returns:
            dict: Dictionary containing library statistics
        """
        total_books = len(self.books)
        available_books = len(self.get_available_books())
        borrowed_books = len(self.get_borrowed_books())
        total_members = len(self.members)
        reference_books = sum(1 for book in self.books.values() if isinstance(book, ReferenceBook))
        
        return {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'reference_books': reference_books,
            'total_members': total_members
        }
    
    def __str__(self):
        """String representation of the library."""
        stats = self.get_library_stats()
        return f"{self.name} - {stats['total_books']} books, {stats['total_members']} members"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"Library('{self.name}')"


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Library Management System")
    print("=" * 60)
    
    # Initialize library
    library = Library("HKUST Library")
    print(f"\nCreated: {library}")
    
    # Test 1: Add books
    print("\n[Test 1] Adding books:")
    book1 = FictionBook("1984", "George Orwell", "978-0451524935", 1949, "Dystopian")
    book2 = FictionBook("Harry Potter", "J.K. Rowling", "978-0439708180", 1997, "Fantasy")
    book3 = ReferenceBook("Dictionary", "Oxford", "978-0198611868", 1989, "Language")
    book4 = Magazine("National Geographic", "Nat Geo", "ISSN-0027-9358", 2024, 11, "November")
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_book(book4)
    print(f"Total books: {len(library.get_all_books())}")
    
    # Test 2: Register members
    print("\n[Test 2] Registering members:")
    student = StudentMember("Alice", "S001", "20012345")
    teacher = TeacherMember("Dr. Johnson", "T001", "Computer Science")
    guest = GuestMember("Charlie", "G001")
    
    library.register_member(student)
    library.register_member(teacher)
    library.register_member(guest)
    print(f"Total members: {len(library.get_all_members())}")
    
    # Test 3: Lend book (success)
    print("\n[Test 3] Lending book to student:")
    success, message = library.lend_book("S001", "978-0451524935")
    print(f"Success: {success}")
    print(f"Message: {message}")  # Output: Successfully lent '1984' to Alice
    
    # Test 4: Try to lend reference book (should fail)
    print("\n[Test 4] Try to lend reference book:")
    success, message = library.lend_book("S001", "978-0198611868")
    print(f"Success: {success}")
    print(f"Message: {message}")  # Output: Reference book 'Dictionary' cannot be borrowed (In-Library Use Only)
    
    # Test 5: Try to lend already borrowed book
    print("\n[Test 5] Try to lend already borrowed book:")
    success, message = library.lend_book("T001", "978-0451524935")
    print(f"Success: {success}")
    print(f"Message: {message}")
    
    # Test 6: Search books
    print("\n[Test 6] Search books by title:")
    results = library.search_books("Harry", search_by='title')
    print(f"Found {len(results)} book(s)")
    for book in results:
        print(f"  - {book}")
    
    # Test 7: Get available books
    print("\n[Test 7] Available books:")
    available = library.get_available_books()
    print(f"Available: {len(available)} books")
    for book in available:
        print(f"  - {book}")
    
    # Test 8: Return book
    print("\n[Test 8] Return book:")
    success, message = library.return_book("S001", "978-0451524935")
    print(f"Success: {success}")
    print(f"Message: {message}")
    
    # Test 9: Get statistics
    print("\n[Test 9] Library statistics:")
    stats = library.get_library_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test 10: Member's borrowed books
    print("\n[Test 10] Member's borrowed books:")
    library.lend_book("T001", "978-0439708180")  # Teacher borrows Harry Potter
    library.lend_book("T001", "ISSN-0027-9358")  # Teacher borrows magazine
    teacher_member = library.find_member_by_id("T001")
    borrowed = teacher_member.get_borrowed_books()
    print(f"{teacher_member.name} has borrowed {len(borrowed)} book(s):")
    for book in borrowed:
        print(f"  - {book}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
