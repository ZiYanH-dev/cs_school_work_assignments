"""
COMP 1023 Lab 10: Library Management System - Book Module
This module contains the Book class and its subclasses.
"""


class Book:
    """Base class representing a book in the library."""
    
    def __init__(self, title, author, isbn, publication_year):
        """
        Initialize a Book object.
        
        Args:
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): The ISBN number
            publication_year (int): The year of publication
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.available = True
    
    def borrow(self):
        """Mark the book as borrowed."""
        if self.available:
            self.available = False
            return True
        return False
    
    def return_book(self):
        """Mark the book as returned."""
        self.available = True
    
    def get_info(self):
        """
        Get formatted information about the book.
        
        Returns:
            str: Formatted book information
        """
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Year: {self.publication_year}) - {status}"
    
    def __str__(self):
        """String representation of the book."""
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self):
        """Developer-friendly representation of the book."""
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', {self.publication_year})"
    
    def __eq__(self, other):
        """Check if two books are equal based on ISBN."""
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False


class FictionBook(Book):
    """A fiction book with a specific genre."""
    
    def __init__(self, title, author, isbn, publication_year, genre):
        """
        Initialize a FictionBook object.
        
        Args:
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): The ISBN number
            publication_year (int): The year of publication
            genre (str): The genre of the fiction (e.g., "Mystery", "Romance", "Sci-Fi")
        """
        super().__init__(title, author, isbn, publication_year)
        self.genre = genre
    
    def get_info(self):
        """Get formatted information including genre."""
        base_info = super().get_info()
        return f"{base_info} [Fiction - {self.genre}]"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"FictionBook('{self.title}', '{self.author}', '{self.isbn}', {self.publication_year}, '{self.genre}')"


class ReferenceBook(Book):
    """A reference book that cannot be borrowed."""
    
    def __init__(self, title, author, isbn, publication_year, subject):
        """
        Initialize a ReferenceBook object.
        
        Args:
            title (str): The title of the book
            author (str): The author of the book
            isbn (str): The ISBN number
            publication_year (int): The year of publication
            subject (str): The subject area of the reference book
        """
        super().__init__(title, author, isbn, publication_year)
        self.subject = subject
    
    def borrow(self):
        """
        Override borrow method - reference books cannot be borrowed.
        
        Returns:
            bool: Always returns False
        """
        return False
    
    def get_info(self):
        """Get formatted information including subject."""
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Year: {self.publication_year}) - [Reference - {self.subject}] (In-Library Use Only)"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"ReferenceBook('{self.title}', '{self.author}', '{self.isbn}', {self.publication_year}, '{self.subject}')"


class Magazine(Book):
    """A magazine with issue number and publication month."""
    
    def __init__(self, title, author, isbn, publication_year, issue_number, publication_month):
        """
        Initialize a Magazine object.
        
        Args:
            title (str): The title of the magazine
            author (str): The publisher/editor
            isbn (str): The ISBN/ISSN number
            publication_year (int): The year of publication
            issue_number (int): The issue number
            publication_month (str): The month of publication
        """
        super().__init__(title, author, isbn, publication_year)
        self.issue_number = issue_number
        self.publication_month = publication_month
    
    def get_info(self):
        """Get formatted information including issue details."""
        status = "Available" if self.available else "Borrowed"
        return f"{self.title} (Issue #{self.issue_number}, {self.publication_month} {self.publication_year}) - {status} [Magazine]"
    
    def __str__(self):
        """String representation of the magazine."""
        return f"{self.title} Issue #{self.issue_number}"
    
    def __repr__(self):
        """Developer-friendly representation."""
        return f"Magazine('{self.title}', '{self.author}', '{self.isbn}', {self.publication_year}, {self.issue_number}, '{self.publication_month}')"


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Book Module")
    print("=" * 60)
    
    # Test 1: Basic Book class
    print("\n[Test 1] Basic Book class:")
    book = Book("Clean Code", "Robert C. Martin", "978-0132350884", 2008)
    print(f"Title: {book.title}")        # Output: Clean Code
    print(f"Available: {book.available}")    # Output: True
    book.borrow()
    print(f"Available after borrow: {book.available}")    # Output: False
    print(f"str(book): {book}")              # Output: 'Clean Code' by Robert C. Martin
    print(f"repr(book): {repr(book)}")        # Output: Book('Clean Code', 'Robert C. Martin', '978-0132350884', 2008)
    
    # Test 2: FictionBook class
    print("\n[Test 2] FictionBook class:")
    fiction = FictionBook("Harry Potter", "J.K. Rowling", "978-0439708180", 1997, "Fantasy")
    print(f"Genre: {fiction.genre}")     # Output: Fantasy
    print(f"Info: {fiction.get_info()}")  # Includes "[Fiction - Fantasy]"
    
    # Test 3: ReferenceBook class
    print("\n[Test 3] ReferenceBook class:")
    reference = ReferenceBook("Oxford Dictionary", "Oxford Press", "978-0198611868", 1989, "Language")
    print(f"Can borrow: {reference.borrow()}")  # Output: False (cannot be borrowed)
    print(f"Info: {reference.get_info()}")
    
    # Test 4: Magazine class
    print("\n[Test 4] Magazine class:")
    magazine = Magazine("National Geographic", "Nat Geo", "ISSN-0027-9358", 2024, 11, "November")
    print(f"Info: {magazine.get_info()}")  # Includes issue number and month
    print(f"str(magazine): {magazine}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
