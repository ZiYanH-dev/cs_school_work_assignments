"""
COMP 1023 Lab 10: Library Management System - Book Module
Student Name: _______________
Student ID: _______________

This module contains the Book class and its subclasses.
Complete all the TODO sections below.
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
        # TODO: Initialize the following attributes:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.available = True        
        
    def borrow(self):
        """
        Mark the book as borrowed.
        
        Returns:
            bool: True if successful, False if already borrowed
        """
        # TODO: If the book is available, set self.available to False and return True
        # Otherwise, return False
        if self.available:
            self.available=False
            return True
        return False
    
    def return_book(self):
        """Mark the book as returned."""
        # TODO: Set self.available to True
        self.available=True
    
    def get_info(self):
        """
        Get formatted information about the book.
        
        Returns:
            str: Formatted book information
        """
        # TODO: Return a formatted string like:
        # "Title by Author (ISBN: isbn, Year: year) - Available/Borrowed"
        # Example: "Clean Code by Robert C. Martin (ISBN: 978-0132350884, Year: 2008) - Available"

        availability='Available'if self.available else 'Borrowed'
        return f"Title by {self.author} (ISBN: {self.isbn}, Year: {self.publication_year}) - {availability}"
    
    '''
    The __str__ method is a special method that defines a string representation
    of an object, Book type object in this case. The __str__ method is called when
    you use:
    - str(Book type object)
    - print(Book type object)
    - f-strings with the Book type object
    '''
    def __str__(self):
        """String representation of the book."""
        return f"'{self.title}' by {self.author}"
    
    '''
    The __repr__ method is a speical method that defines the "official" string
    representation of an object. It should look like valid Python code that could
    be recreate the object, Book type object in this case. The __repr__ method is called
    when you use:
    - repr(Book type object)
    '''
    def __repr__(self):
        """Developer-friendly representation of the book."""
        return f"Book('{self.title}', '{self.author}', '{self.isbn}', {self.publication_year})"
    
    '''
    The __eq__ method is a special method that defines how objects of a class,
    Book class in this case, should be compared for equality using the == operator.
    The __eq__ method is called when you use:
    - Book type object1 == Book type object2
    '''
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

# ============================================================
# OPTIONAL: Test your implementation
# ============================================================
# Uncomment the code below to test your Book classes.
# Make sure you've implemented all the methods before running this!
#
# To test: python book.py
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Book Module")
    print("=" * 60)
    
    # Test 1: Basic Book class
    print("\n[Test 1] Basic Book class:")
    book = Book("Clean Code", "Robert C. Martin", "978-0132350884", 2008)
    print(f"Title: {book.title}")        # Expected: Clean Code
    print(f"Available: {book.available}")    # Expected: True
    book.borrow()
    print(f"Available after borrow: {book.available}")    # Expected: False
    print(f"str(book): {book}")              # Expected: 'Clean Code' by Robert C. Martin
    print(f"repr(book): {repr(book)}")        # Expected: Book('Clean Code', 'Robert C. Martin', '978-0132350884', 2008)
    
    # Test 2: FictionBook class
    print("\n[Test 2] FictionBook class:")
    fiction = FictionBook("Harry Potter", "J.K. Rowling", "978-0439708180", 1997, "Fantasy")
    print(f"Genre: {fiction.genre}")     # Expected: Fantasy
    print(f"Info: {fiction.get_info()}")  # Should include "[Fiction - Fantasy]"
    
    # Test 3: ReferenceBook class
    print("\n[Test 3] ReferenceBook class:")
    reference = ReferenceBook("Oxford Dictionary", "Oxford Press", "978-0198611868", 1989, "Language")
    print(f"Can borrow: {reference.borrow()}")  # Expected: False (cannot be borrowed)
    print(f"Info: {reference.get_info()}")
    
    # Test 4: Magazine class
    print("\n[Test 4] Magazine class:")
    magazine = Magazine("National Geographic", "Nat Geo", "ISSN-0027-9358", 2024, 11, "November")
    print(f"Info: {magazine.get_info()}")  # Should include issue number and month
    print(f"str(magazine): {magazine}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

