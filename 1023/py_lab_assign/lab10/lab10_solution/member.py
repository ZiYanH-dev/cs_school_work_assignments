"""
COMP 1023 Lab 10: Library Management System - Member Module
This module contains the Member class and its subclasses.
"""


class Member:
    """Base class representing a library member."""
    
    def __init__(self, name, member_id, max_books=3):
        """
        Initialize a Member object.
        
        Args:
            name (str): The name of the member
            member_id (str): The unique member ID
            max_books (int): Maximum number of books that can be borrowed
        """
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
        self.max_books = max_books
    
    def can_borrow(self):
        """
        Check if the member can borrow more books.
        
        Returns:
            bool: True if member can borrow more books, False otherwise
        """
        return len(self.borrowed_books) < self.max_books
    
    def borrow_book(self, book):
        """
        Borrow a book.
        
        Args:
            book (Book): The book to borrow
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.can_borrow() and book.borrow():
            self.borrowed_books.append(book)
            return True
        return False
    
    def return_book(self, book):
        """
        Return a borrowed book.
        
        Args:
            book (Book): The book to return
            
        Returns:
            bool: True if successful, False otherwise
        """
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)
            return True
        return False
    
    def get_borrowed_books(self):
        """
        Get the list of borrowed books.
        
        Returns:
            list: List of borrowed Book objects
        """
        return self.borrowed_books.copy()
    
    def get_info(self):
        """
        Get formatted information about the member.
        
        Returns:
            str: Formatted member information
        """
        borrowed_count = len(self.borrowed_books)
        return f"{self.name} (ID: {self.member_id}) - {borrowed_count}/{self.max_books} books borrowed"
    
    def __str__(self):
        """String representation of the member."""
        return f"{self.name} ({self.member_id})"
    
    def __repr__(self):
        """Developer-friendly representation of the member."""
        return f"Member('{self.name}', '{self.member_id}', max_books={self.max_books})"
    
    def __eq__(self, other):
        """Check if two members are equal based on member ID."""
        if isinstance(other, Member):
            return self.member_id == other.member_id
        return False


class StudentMember(Member):
    """A student member who can borrow up to 5 books."""
    
    def __init__(self, name, member_id, student_id):
        """
        Initialize a StudentMember object.
        
        Args:
            name (str): The name of the student
            member_id (str): The unique member ID
            student_id (str): The student ID number
        """
        super().__init__(name, member_id, max_books=5)
        self.student_id = student_id
    
    def get_info(self):
        """Get formatted information including student ID."""
        base_info = super().get_info()
        return f"{base_info} [Student - {self.student_id}]"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"StudentMember('{self.name}', '{self.member_id}', '{self.student_id}')"


class TeacherMember(Member):
    """A teacher member who can borrow up to 10 books."""
    
    def __init__(self, name, member_id, department):
        """
        Initialize a TeacherMember object.
        
        Args:
            name (str): The name of the teacher
            member_id (str): The unique member ID
            department (str): The department name
        """
        super().__init__(name, member_id, max_books=10)
        self.department = department
    
    def get_info(self):
        """Get formatted information including department."""
        base_info = super().get_info()
        return f"{base_info} [Teacher - {self.department}]"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"TeacherMember('{self.name}', '{self.member_id}', '{self.department}')"


class GuestMember(Member):
    """A guest member who can borrow up to 2 books."""
    
    def __init__(self, name, member_id):
        """
        Initialize a GuestMember object.
        
        Args:
            name (str): The name of the guest
            member_id (str): The unique member ID
        """
        super().__init__(name, member_id, max_books=2)
    
    def get_info(self):
        """Get formatted information with guest indicator."""
        base_info = super().get_info()
        return f"{base_info} [Guest]"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"GuestMember('{self.name}', '{self.member_id}')"


# Example usage and testing
if __name__ == "__main__":
    # Import Book for testing
    from book import Book
    
    print("=" * 60)
    print("Testing Member Module")
    print("=" * 60)
    
    # Test 1: Basic Member class
    print("\n[Test 1] Basic Member class:")
    member = Member("Alice Wong", "M001", max_books=3)
    book = Book("Clean Code", "Robert C. Martin", "978-0132350884", 2008)
    member.borrow_book(book)
    print(f"Borrowed books count: {len(member.get_borrowed_books())}")  # Output: 1
    print(f"Can borrow more: {member.can_borrow()}")                # Output: True
    print(f"str(member): {str(member)}")                        # Output: Alice Wong (M001)
    print(f"repr(member): {repr(member)}")                       # Output: Member('Alice Wong', 'M001', max_books=3)
    
    # Test 2: StudentMember class
    print("\n[Test 2] StudentMember class:")
    student = StudentMember("Bob Chen", "S001", "20012345")
    print(f"Max books: {student.max_books}")  # Output: 5
    print(f"Student ID: {student.student_id}")  # Output: 20012345
    print(f"Info: {student.get_info()}")
    print(f"repr: {repr(student)}")
    
    # Test 3: TeacherMember class
    print("\n[Test 3] TeacherMember class:")
    teacher = TeacherMember("Dr. Johnson", "T001", "Computer Science")
    print(f"Max books: {teacher.max_books}")  # Output: 10
    print(f"Department: {teacher.department}")
    print(f"Info: {teacher.get_info()}")
    print(f"repr: {repr(teacher)}")
    
    # Test 4: GuestMember class
    print("\n[Test 4] GuestMember class:")
    guest = GuestMember("Charlie", "G001")
    print(f"Max books: {guest.max_books}")    # Output: 2
    print(f"Info: {guest.get_info()}")
    print(f"repr: {repr(guest)}")
    
    # Test 5: Borrowing limits
    print("\n[Test 5] Testing borrowing limits:")
    guest2 = GuestMember("Diana", "G002")
    book1 = Book("Book 1", "Author 1", "ISBN-001", 2020)
    book2 = Book("Book 2", "Author 2", "ISBN-002", 2021)
    book3 = Book("Book 3", "Author 3", "ISBN-003", 2022)
    
    print(f"Borrow book 1: {guest2.borrow_book(book1)}")  # True
    print(f"Borrow book 2: {guest2.borrow_book(book2)}")  # True
    print(f"Can borrow more: {guest2.can_borrow()}")      # False (limit reached)
    print(f"Borrow book 3: {guest2.borrow_book(book3)}")  # False (over limit)
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
