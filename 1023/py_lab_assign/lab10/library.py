"""
COMP 1023 Lab 10: Library Management System - Library Module
Student Name: _______________
Student ID: _______________

This module contains the Library class for managing the library system.
Complete all the TODO sections below.
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
        # TODO: Initialize the following attributes:
        self.name = name
        self.books = {}    # empty dict for ISBN -> Book
        self.members = {}  # empty dict for member_id -> Member
        
    
    def add_book(self, book:Book):
        """
        Add a book to the library.
        
        Args:
            book (Book): The book to add
            
        Returns:
            bool: True if successful, False if book already exists
        """
        # TODO: If book.isbn is not in self.books, add it and return True
        # Otherwise, return False
        if book.isbn not in self.books:
            self.books[book.isbn]=book
            return True
        return False
    
    def register_member(self, member:Member):
        """
        Register a new member.
        
        Args:
            member (Member): The member to register
            
        Returns:
            bool: True if successful, False if member already exists
        """
        # TODO: If member.member_id is not in self.members, add it and return True
        # Otherwise, return False
        if member.member_id not in self.members:
            self.members[member.member_id]=member
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
        # TODO: Return the book from self.books dict, or None if not found
        # Use: return self.books.get(isbn)
        return self.books.get(isbn)
        
    def find_member_by_id(self, member_id)->Member:
        """
        Find a member by their ID.
        
        Args:
            member_id (str): The member ID to search for
            
        Returns:
            Member or None: The member if found, None otherwise
        """
        # TODO: Return the member from self.members dict, or None if not found
        # Use: return self.members.get(member_id)
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
        # TODO: Implement the following logic:
        # 1. Find the member and book using their respective methods
        # 2. Check if member and book exist (return appropriate error messages)
        # 3. Check if book is available
        # 4. Check if book is a ReferenceBook (cannot be borrowed)
        # 5. Check if member can borrow more books
        # 6. Try to borrow the book using member.borrow_book()
        # 7. Return appropriate success or error messages

        success=(True,'okay')
        fail=(False,'not okay')
        member,book=self.find_member_by_id(member_id),self.find_book_by_isbn(isbn)
        if not member or not book:
            return fail
        
        if member.borrow_book(book):
            return success
        return fail

    
    def return_book(self, member_id, isbn):
        """
        Process a book return.
        
        Args:
            member_id (str): The member ID
            isbn (str): The book ISBN
            
        Returns:
            tuple: (bool, str) - Success status and message
        """
        # TODO: Implement the following logic:
        # 1. Find the member and book
        # 2. Check if they exist
        # 3. Try to return the book using member.return_book()
        # 4. Return appropriate success or error messages
        
        success=(True,'okay')
        fail=(False,'not okay')
        member,book=self.find_member_by_id(member_id),self.find_book_by_isbn(isbn)
        if not member or not book:
            return fail
        
        if member.return_book(book):
            return success
        return fail

    
    def search_books(self, keyword, search_by='title')->list[Book]:
        """
        Search for books by title or author.
        
        Args:
            keyword (str): The search keyword
            search_by (str): 'title' or 'author'
            
        Returns:
            list: List of matching Book objects
        """
        # TODO: Search through all books in self.books
        # If search_by is 'title', check if keyword is in book title (case-insensitive)
        # If search_by is 'author', check if keyword is in book author (case-insensitive)
        # Return list of matching books
        # Hint: use for book in self.books.values():
        keyword=keyword.lower()
        books=self.books.values()
        result=[]
        match search_by:
            case 'title':
                for book in books:
                    if keyword in book.title.lower():
                        result.append(book)

            case 'author':
                for book in books:
                    if keyword in book.author.lower():
                        result.append(book)
        return result
    
    def get_available_books(self):
        """
        Get all available books (excluding reference books).
        
        Returns:
            list: List of available Book objects
        """
        # TODO: Return a list of books that are:
        # - Available (book.available is True)
        # - Not a ReferenceBook (use isinstance())
        # Hint: use list comprehension over self.books.values()
        books=self.books.values()
        return [book for book in books if book.available and not isinstance(book,ReferenceBook)]
    
    def get_all_books(self):
        """
        Get all books in the library.
        
        Returns:
            list: List of all Book objects
        """
        # TODO: Return a list of all books from self.books dict
        # Use: return list(self.books.values())
        return list(self.books.values())
    
    def get_all_members(self):
        """
        Get all registered members.
        
        Returns:
            list: List of all Member objects
        """
        # TODO: Return a list of all members from self.members dict
        # Use: return list(self.members.values())
        return list(self.members.values())
    
    def get_borrowed_books(self):
        """
        Get all currently borrowed books.
        
        Returns:
            list: List of borrowed Book objects
        """
        # TODO: Return a list of books where book.available is False
        # Hint: use list comprehension over self.books.values()
        return [book for book in self.books.values() if not book.available]
    
    def get_library_stats(self):
        """
        Get library statistics.
        
        Returns:
            dict: Dictionary containing library statistics
        """
        # TODO: Calculate and return a dictionary with the following keys:
        # - 'total_books': total number of books
        # - 'available_books': number of available books (from get_available_books())
        # - 'borrowed_books': number of borrowed books (from get_borrowed_books())
        # - 'reference_books': number of reference books
        # - 'total_members': total number of members
        total_books=self.get_all_books()
        available_books=self.get_available_books()
        borrow_books=self.get_borrowed_books()
        referenceBook=[book for book in total_books if isinstance(book,ReferenceBook)]
        total_member=self.get_all_members()
        return {
            'total_books':len(total_books),
            'available_books': len(available_books),
            'borrowed_books': len(borrow_books),
            'reference_books': len(referenceBook),
            'total_members':len(total_member)
        }


    '''
    The __str__ method is a special method that defines a string representation
    of an object, Library type object in this case. The __str__ method is called when
    you use:
    - str(Library type object)
    - print(Library type object)
    - f-strings with the Library type object
    '''    
    def __str__(self):
        """String representation of the library."""
        stats = self.get_library_stats()
        return f"{self.name} - {stats['total_books']} books, {stats['total_members']} members"

    '''
    The __repr__ method is a speical method that defines the "official" string
    representation of an object. It should look like valid Python code that could
    be recreate the object, Library type object in this case. The __repr__ method is 
    called when you use:
    - repr(Library type object)
    '''       
    def __repr__(self):
        """Developer-friendly representation."""
        return f"Library('{self.name}')"


# ============================================================
# OPTIONAL: Test your implementation
# ============================================================
# Uncomment the code below to test your Library class.
# Make sure you've implemented all the methods in book.py, member.py, and library.py before running this!
#
# To test: python library.py
# ============================================================

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
    print(f"Message: {message}")  # Expected: Successfully lent '1984' to Alice
    
    # Test 4: Try to lend reference book (should fail)
    print("\n[Test 4] Try to lend reference book:")
    success, message = library.lend_book("S001", "978-0198611868")
    print(f"Success: {success}")
    print(f"Message: {message}")  # Expected: Reference book 'Dictionary' cannot be borrowed (In-Library Use Only)
    
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
