"""
COMP 1023 Lab 10: Library Management System - Test Cases
This module contains comprehensive test cases for the library management system.
Run with: python test_library.py
"""

from book import Book, FictionBook, ReferenceBook, Magazine
from member import Member, StudentMember, TeacherMember, GuestMember
from library import Library


def test_book_basic():
    """Test basic Book functionality."""
    print("Testing Book class...")
    book = Book("Clean Code", "Robert C. Martin", "978-0132350884", 2008)
    
    # Test properties
    assert book.title == "Clean Code", "Book title should be correct"
    assert book.author == "Robert C. Martin", "Book author should be correct"
    assert book.isbn == "978-0132350884", "Book ISBN should be correct"
    assert book.available == True, "Book should be available initially"
    
    # Test borrow
    assert book.borrow() == True, "First borrow should succeed"
    assert book.available == False, "Book should not be available after borrow"
    assert book.borrow() == False, "Second borrow should fail"
    
    # Test return
    book.return_book()
    assert book.available == True, "Book should be available after return"
    
    # Test special methods
    assert str(book) == "'Clean Code' by Robert C. Martin", "str() should be formatted correctly"
    assert repr(book) == "Book('Clean Code', 'Robert C. Martin', '978-0132350884', 2008)", "repr() should be formatted correctly"
    
    # Test equality
    book2 = Book("Other Book", "Other Author", "978-0132350884", 2020)
    assert book == book2, "Books with same ISBN should be equal"
    
    print("✓ Book class tests passed!")


def test_fiction_book():
    """Test FictionBook class."""
    print("Testing FictionBook class...")
    fiction = FictionBook("Harry Potter", "J.K. Rowling", "978-0439708180", 1997, "Fantasy")
    
    assert fiction.genre == "Fantasy", "Genre should be correct"
    assert fiction.title == "Harry Potter", "Title should be inherited correctly"
    assert "[Fiction - Fantasy]" in fiction.get_info(), "Info should include genre"
    
    print("✓ FictionBook class tests passed!")


def test_reference_book():
    """Test ReferenceBook class."""
    print("Testing ReferenceBook class...")
    ref = ReferenceBook("Dictionary", "Oxford Press", "978-0198611868", 1989, "Language")
    
    assert ref.subject == "Language", "Subject should be correct"
    assert ref.borrow() == False, "Reference books cannot be borrowed"
    assert ref.available == True, "Reference book should remain available"
    assert "In-Library Use Only" in ref.get_info(), "Info should indicate in-library use"
    
    print("✓ ReferenceBook class tests passed!")


def test_magazine():
    """Test Magazine class."""
    print("Testing Magazine class...")
    magazine = Magazine("National Geographic", "Nat Geo", "ISSN-0027-9358", 2024, 11, "November")
    
    assert magazine.issue_number == 11, "Issue number should be correct"
    assert magazine.publication_month == "November", "Publication month should be correct"
    assert "Issue #11" in magazine.get_info(), "Info should include issue number"
    assert str(magazine) == "National Geographic Issue #11", "str() should include issue number"
    
    print("✓ Magazine class tests passed!")


def test_member_basic():
    """Test basic Member functionality."""
    print("Testing Member class...")
    member = Member("Alice Wong", "M001", max_books=3)
    book1 = Book("Book 1", "Author 1", "ISBN001", 2020)
    book2 = Book("Book 2", "Author 2", "ISBN002", 2021)
    
    # Test properties
    assert member.name == "Alice Wong", "Member name should be correct"
    assert member.member_id == "M001", "Member ID should be correct"
    assert member.max_books == 3, "Max books should be correct"
    assert member.can_borrow() == True, "Member should be able to borrow initially"
    
    # Test borrowing
    assert member.borrow_book(book1) == True, "First borrow should succeed"
    assert len(member.get_borrowed_books()) == 1, "Should have 1 borrowed book"
    assert book1.available == False, "Book should not be available after borrow"
    
    # Test returning
    assert member.return_book(book1) == True, "Return should succeed"
    assert len(member.get_borrowed_books()) == 0, "Should have 0 borrowed books"
    assert book1.available == True, "Book should be available after return"
    
    # Test borrowing limit
    member.borrow_book(book1)
    member.borrow_book(book2)
    book3 = Book("Book 3", "Author 3", "ISBN003", 2022)
    member.borrow_book(book3)
    book4 = Book("Book 4", "Author 4", "ISBN004", 2023)
    assert member.borrow_book(book4) == False, "Should not exceed borrowing limit"
    
    print("✓ Member class tests passed!")


def test_student_member():
    """Test StudentMember class."""
    print("Testing StudentMember class...")
    student = StudentMember("Bob Chen", "S001", "20012345")
    
    assert student.student_id == "20012345", "Student ID should be correct"
    assert student.max_books == 5, "Students should be able to borrow 5 books"
    assert "[Student -" in student.get_info(), "Info should include student indicator"
    
    print("✓ StudentMember class tests passed!")


def test_teacher_member():
    """Test TeacherMember class."""
    print("Testing TeacherMember class...")
    teacher = TeacherMember("Dr. Johnson", "T001", "Computer Science")
    
    assert teacher.department == "Computer Science", "Department should be correct"
    assert teacher.max_books == 10, "Teachers should be able to borrow 10 books"
    assert "[Teacher -" in teacher.get_info(), "Info should include teacher indicator"
    
    print("✓ TeacherMember class tests passed!")


def test_guest_member():
    """Test GuestMember class."""
    print("Testing GuestMember class...")
    guest = GuestMember("Charlie", "G001")
    
    assert guest.max_books == 2, "Guests should be able to borrow 2 books"
    assert "[Guest]" in guest.get_info(), "Info should include guest indicator"
    
    print("✓ GuestMember class tests passed!")


def test_library_basic():
    """Test basic Library functionality."""
    print("Testing Library class...")
    library = Library("Test Library")
    
    # Test adding books
    book1 = Book("Book 1", "Author 1", "ISBN001", 2020)
    book2 = Book("Book 2", "Author 2", "ISBN002", 2021)
    assert library.add_book(book1) == True, "First book addition should succeed"
    assert library.add_book(book1) == False, "Duplicate book should not be added"
    library.add_book(book2)
    
    # Test registering members
    member1 = StudentMember("Alice", "S001", "20012345")
    member2 = StudentMember("Bob", "S002", "20012346")
    assert library.register_member(member1) == True, "First member registration should succeed"
    assert library.register_member(member1) == False, "Duplicate member should not be registered"
    library.register_member(member2)
    
    # Test finding
    assert library.find_book_by_isbn("ISBN001") == book1, "Should find correct book"
    assert library.find_book_by_isbn("INVALID") == None, "Should return None for invalid ISBN"
    assert library.find_member_by_id("S001") == member1, "Should find correct member"
    assert library.find_member_by_id("INVALID") == None, "Should return None for invalid ID"
    
    print("✓ Library basic tests passed!")


def test_library_lending():
    """Test Library lending functionality."""
    print("Testing Library lending...")
    library = Library("Test Library")
    
    # Set up
    book = FictionBook("Test Book", "Test Author", "ISBN123", 2020, "Fiction")
    ref_book = ReferenceBook("Dictionary", "Oxford", "ISBN456", 2000, "Language")
    student = StudentMember("Alice", "S001", "20012345")
    guest = GuestMember("Bob", "G001")
    
    library.add_book(book)
    library.add_book(ref_book)
    library.register_member(student)
    library.register_member(guest)
    
    # Test successful lending
    success, msg = library.lend_book("S001", "ISBN123")
    assert success == True, "Lending should succeed"
    assert "Successfully lent" in msg, "Message should indicate success"
    
    # Test lending borrowed book
    success, msg = library.lend_book("G001", "ISBN123")
    assert success == False, "Should not lend borrowed book"
    assert "currently borrowed" in msg, "Message should indicate book is borrowed"
    
    # Test lending reference book
    success, msg = library.lend_book("S001", "ISBN456")
    assert success == False, "Reference books cannot be borrowed"
    assert "cannot be borrowed" in msg, "Message should indicate reference book"
    
    # Test invalid member/book
    success, msg = library.lend_book("INVALID", "ISBN123")
    assert success == False, "Invalid member should fail"
    assert "Member not found" in msg, "Message should indicate member not found"
    
    success, msg = library.lend_book("S001", "INVALID")
    assert success == False, "Invalid book should fail"
    assert "Book not found" in msg, "Message should indicate book not found"
    
    print("✓ Library lending tests passed!")


def test_library_returning():
    """Test Library returning functionality."""
    print("Testing Library returning...")
    library = Library("Test Library")
    
    book = Book("Test Book", "Test Author", "ISBN123", 2020)
    member = StudentMember("Alice", "S001", "20012345")
    
    library.add_book(book)
    library.register_member(member)
    library.lend_book("S001", "ISBN123")
    
    # Test successful return
    success, msg = library.return_book("S001", "ISBN123")
    assert success == True, "Return should succeed"
    assert "Successfully returned" in msg, "Message should indicate success"
    
    # Test returning non-borrowed book
    success, msg = library.return_book("S001", "ISBN123")
    assert success == False, "Should not return non-borrowed book"
    assert "did not borrow" in msg, "Message should indicate book was not borrowed"
    
    print("✓ Library returning tests passed!")


def test_library_search():
    """Test Library search functionality."""
    print("Testing Library search...")
    library = Library("Test Library")
    
    book1 = Book("Python Programming", "John Smith", "ISBN001", 2020)
    book2 = Book("Java Programming", "John Doe", "ISBN002", 2021)
    book3 = Book("Python Data Science", "Jane Smith", "ISBN003", 2022)
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    
    # Search by title
    results = library.search_books("Python", search_by='title')
    assert len(results) == 2, "Should find 2 books with 'Python' in title"
    
    # Search by author
    results = library.search_books("Smith", search_by='author')
    assert len(results) == 2, "Should find 2 books by authors named Smith"
    
    # Search with no results
    results = library.search_books("Nonexistent", search_by='title')
    assert len(results) == 0, "Should return empty list for no matches"
    
    print("✓ Library search tests passed!")


def test_library_statistics():
    """Test Library statistics functionality."""
    print("Testing Library statistics...")
    library = Library("Test Library")
    
    # Add books
    book1 = FictionBook("Book 1", "Author 1", "ISBN001", 2020, "Fiction")
    book2 = ReferenceBook("Reference 1", "Author 2", "ISBN002", 2021, "Science")
    book3 = Book("Book 3", "Author 3", "ISBN003", 2022)
    
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    
    # Add members and lend
    student = StudentMember("Alice", "S001", "20012345")
    library.register_member(student)
    library.lend_book("S001", "ISBN001")
    
    stats = library.get_library_stats()
    
    assert stats['total_books'] == 3, "Should have 3 total books"
    assert stats['available_books'] == 1, "Should have 1 available book (excluding reference)"
    assert stats['borrowed_books'] == 1, "Should have 1 borrowed book"
    assert stats['reference_books'] == 1, "Should have 1 reference book"
    assert stats['total_members'] == 1, "Should have 1 member"
    
    # Test get_all_books
    all_books = library.get_all_books()
    assert len(all_books) == 3, "Should return all books"
    
    # Test get_available_books
    available = library.get_available_books()
    assert len(available) == 1, "Should return only available non-reference books"
    
    # Test get_borrowed_books
    borrowed = library.get_borrowed_books()
    assert len(borrowed) == 1, "Should return borrowed books"
    
    print("✓ Library statistics tests passed!")


def test_borrowing_limits():
    """Test member borrowing limits."""
    print("Testing borrowing limits...")
    library = Library("Test Library")
    
    # Create books
    for i in range(15):
        library.add_book(Book(f"Book {i}", f"Author {i}", f"ISBN{i:03d}", 2020))
    
    # Test student limit (5 books)
    student = StudentMember("Student", "S001", "20012345")
    library.register_member(student)
    for i in range(5):
        success, _ = library.lend_book("S001", f"ISBN{i:03d}")
        assert success == True, f"Student should be able to borrow book {i+1}"
    
    success, msg = library.lend_book("S001", "ISBN005")
    assert success == False, "Student should not exceed 5 books limit"
    assert "borrowing limit" in msg, "Message should indicate limit reached"
    
    # Test teacher limit (10 books)
    teacher = TeacherMember("Teacher", "T001", "CS")
    library.register_member(teacher)
    for i in range(5, 15):
        book = library.find_book_by_isbn(f"ISBN{i:03d}")
        if book and book.available:
            success, _ = library.lend_book("T001", f"ISBN{i:03d}")
            if i < 15:
                assert success == True, f"Teacher should be able to borrow book {i+1}"
    
    # Test guest limit (2 books)
    library2 = Library("Test Library 2")
    library2.add_book(Book("Book A", "Author A", "ISBNA", 2020))
    library2.add_book(Book("Book B", "Author B", "ISBNB", 2021))
    library2.add_book(Book("Book C", "Author C", "ISBNC", 2022))
    
    guest = GuestMember("Guest", "G001")
    library2.register_member(guest)
    
    success, _ = library2.lend_book("G001", "ISBNA")
    assert success == True, "Guest should be able to borrow first book"
    success, _ = library2.lend_book("G001", "ISBNB")
    assert success == True, "Guest should be able to borrow second book"
    success, msg = library2.lend_book("G001", "ISBNC")
    assert success == False, "Guest should not exceed 2 books limit"
    
    print("✓ Borrowing limits tests passed!")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*80)
    print("  COMP 1023 Lab 10 - Library Management System Test Suite")
    print("="*80 + "\n")
    
    try:
        # Book tests
        test_book_basic()
        test_fiction_book()
        test_reference_book()
        test_magazine()
        
        # Member tests
        test_member_basic()
        test_student_member()
        test_teacher_member()
        test_guest_member()
        
        # Library tests
        test_library_basic()
        test_library_lending()
        test_library_returning()
        test_library_search()
        test_library_statistics()
        test_borrowing_limits()
        
        print("\n" + "="*80)
        print("  ✓ ALL TESTS PASSED!")
        print("="*80)
        return True
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        print("="*80)
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*80)
        return False


if __name__ == "__main__":
    run_all_tests()

