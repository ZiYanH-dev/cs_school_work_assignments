"""
COMP 1023 Lab 10: Library Management System - GUI Testing Program
This program provides a graphical user interface to test the library management system.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from book import Book, FictionBook, ReferenceBook, Magazine
from member import Member, StudentMember, TeacherMember, GuestMember
from library import Library


class LibraryGUI:
    """GUI application for the Library Management System."""
    
    def __init__(self, master):
        """Initialize the GUI application."""
        self.master = master
        master.title("Library Management System")
        master.geometry("1000x700")
        
        # Initialize library with sample data
        self.library = self.initialize_sample_library()
        
        # Create GUI components
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        
        # Display welcome message
        self.display_welcome()
    
    def initialize_sample_library(self):
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
    
    def create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        
        # Books menu
        books_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Books", menu=books_menu)
        books_menu.add_command(label="View All Books", command=self.show_all_books)
        books_menu.add_command(label="View Available Books", command=self.show_available_books)
        books_menu.add_command(label="Search Books", command=self.search_books_dialog)
        
        # Members menu
        members_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Members", menu=members_menu)
        members_menu.add_command(label="View All Members", command=self.show_all_members)
        members_menu.add_command(label="View Member's Books", command=self.view_member_books_dialog)
        
        # Transactions menu
        transactions_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Transactions", menu=transactions_menu)
        transactions_menu.add_command(label="Borrow Book", command=self.borrow_book_dialog)
        transactions_menu.add_command(label="Return Book", command=self.return_book_dialog)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Library Statistics", command=self.show_statistics)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_main_frame(self):
        """Create the main content frame."""
        # Top button frame
        button_frame = tk.Frame(self.master, bg='#2c3e50', pady=10)
        button_frame.pack(fill=tk.X)
        
        buttons = [
            ("📚 All Books", self.show_all_books),
            ("✅ Available Books", self.show_available_books),
            ("👥 All Members", self.show_all_members),
            ("📊 Statistics", self.show_statistics),
            ("🔍 Search", self.search_books_dialog),
            ("📤 Borrow", self.borrow_book_dialog),
            ("📥 Return", self.return_book_dialog),
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, 
                          bg='#3498db', fg='black', font=('Arial', 10, 'bold'),
                          padx=10, pady=5, relief=tk.RAISED, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=5)
        
        # Content frame with scrollbar
        content_frame = tk.Frame(self.master)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for displaying information
        self.text_display = tk.Text(content_frame, wrap=tk.WORD, 
                                    yscrollcommand=scrollbar.set,
                                    font=('Courier New', 11),
                                    bg='#ffffff', fg='#000000',
                                    relief=tk.SOLID, borderwidth=1)
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_display.yview)
    
    def create_status_bar(self):
        """Create the status bar."""
        self.status_bar = tk.Label(self.master, text="Ready", 
                                   bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                   bg='#34495e', fg='white', font=('Arial', 9))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_status(self, message):
        """Update the status bar message."""
        self.status_bar.config(text=message)
    
    def clear_display(self):
        """Clear the text display."""
        self.text_display.delete(1.0, tk.END)
    
    def display_text(self, text, tag=None):
        """Display text in the text widget."""
        self.text_display.insert(tk.END, text + "\n", tag)
        self.text_display.see(tk.END)
    
    def display_welcome(self):
        """Display welcome message."""
        self.clear_display()
        self.text_display.tag_config("title", font=('Arial', 16, 'bold'), foreground='#1a237e')
        self.text_display.tag_config("subtitle", font=('Arial', 12), foreground='#455a64')
        
        self.display_text("=" * 60, "title")
        self.display_text("  LIBRARY MANAGEMENT SYSTEM", "title")
        self.display_text("  COMP 1023 Lab 10", "subtitle")
        self.display_text("=" * 60, "title")
        self.display_text("")
        self.display_text(f"Welcome to {self.library.name}!")
        self.display_text("")
        self.display_text("Use the buttons above or the menu bar to:")
        self.display_text("  • View books and members")
        self.display_text("  • Search for books")
        self.display_text("  • Borrow and return books")
        self.display_text("  • View library statistics")
        self.display_text("")
        
        stats = self.library.get_library_stats()
        self.display_text(f"Current Status:")
        self.display_text(f"  Total Books: {stats['total_books']}")
        self.display_text(f"  Total Members: {stats['total_members']}")
        
        self.update_status("Ready")
    
    def show_all_books(self):
        """Display all books in the library."""
        self.clear_display()
        self.text_display.tag_config("header", font=('Arial', 14, 'bold'), foreground='#0d47a1')
        
        self.display_text("=" * 80, "header")
        self.display_text("ALL BOOKS IN LIBRARY", "header")
        self.display_text("=" * 80, "header")
        self.display_text("")
        
        books = self.library.get_all_books()
        
        if not books:
            self.display_text("No books in the library.")
        else:
            for i, book in enumerate(books, 1):
                self.display_text(f"{i}. {book.get_info()}")
        
        self.update_status(f"Displaying {len(books)} books")
    
    def show_available_books(self):
        """Display all available books."""
        self.clear_display()
        self.text_display.tag_config("header", font=('Arial', 14, 'bold'), foreground='#2e7d32')
        
        self.display_text("=" * 80, "header")
        self.display_text("AVAILABLE BOOKS", "header")
        self.display_text("=" * 80, "header")
        self.display_text("")
        
        books = self.library.get_available_books()
        
        if not books:
            self.display_text("No available books.")
        else:
            for i, book in enumerate(books, 1):
                self.display_text(f"{i}. {book.get_info()}")
        
        self.update_status(f"Displaying {len(books)} available books")
    
    def show_all_members(self):
        """Display all members."""
        self.clear_display()
        self.text_display.tag_config("header", font=('Arial', 14, 'bold'), foreground='#0d47a1')
        
        self.display_text("=" * 80, "header")
        self.display_text("ALL MEMBERS", "header")
        self.display_text("=" * 80, "header")
        self.display_text("")
        
        members = self.library.get_all_members()
        
        if not members:
            self.display_text("No registered members.")
        else:
            for i, member in enumerate(members, 1):
                self.display_text(f"{i}. {member.get_info()}")
                borrowed = member.get_borrowed_books()
                if borrowed:
                    for book in borrowed:
                        self.display_text(f"     → {book.title}")
        
        self.update_status(f"Displaying {len(members)} members")
    
    def search_books_dialog(self):
        """Show search dialog and display results."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Search Books")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Search Books", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Search type
        tk.Label(dialog, text="Search by:").pack()
        search_type = tk.StringVar(value="title")
        tk.Radiobutton(dialog, text="Title", variable=search_type, value="title").pack()
        tk.Radiobutton(dialog, text="Author", variable=search_type, value="author").pack()
        
        # Keyword input
        tk.Label(dialog, text="Enter keyword:").pack(pady=(10, 0))
        keyword_entry = tk.Entry(dialog, width=40)
        keyword_entry.pack(pady=5)
        keyword_entry.focus()
        
        def perform_search():
            keyword = keyword_entry.get().strip()
            if not keyword:
                messagebox.showwarning("Input Required", "Please enter a search keyword.")
                return
            
            dialog.destroy()
            self.search_books(keyword, search_type.get())
        
        tk.Button(dialog, text="Search", command=perform_search, 
                 bg='#3498db', fg='black', padx=20, pady=5).pack(pady=10)
        
        keyword_entry.bind('<Return>', lambda e: perform_search())
    
    def search_books(self, keyword, search_by):
        """Display search results."""
        self.clear_display()
        self.text_display.tag_config("header", font=('Arial', 14, 'bold'), foreground='#c62828')
        
        self.display_text("=" * 80, "header")
        self.display_text(f"SEARCH RESULTS - {search_by.upper()}: '{keyword}'", "header")
        self.display_text("=" * 80, "header")
        self.display_text("")
        
        results = self.library.search_books(keyword, search_by=search_by)
        
        if not results:
            self.display_text("No books found matching your search.")
        else:
            for i, book in enumerate(results, 1):
                self.display_text(f"{i}. {book.get_info()}")
        
        self.update_status(f"Found {len(results)} book(s)")
    
    def view_member_books_dialog(self):
        """Show dialog to view a member's borrowed books."""
        member_id = simpledialog.askstring("View Member's Books", 
                                          "Enter member ID:",
                                          parent=self.master)
        
        if member_id:
            self.view_member_books(member_id.strip())
    
    def view_member_books(self, member_id):
        """Display a member's borrowed books."""
        member = self.library.find_member_by_id(member_id)
        
        if member is None:
            messagebox.showerror("Error", f"Member '{member_id}' not found.")
            return
        
        self.clear_display()
        self.text_display.tag_config("header", font=('Arial', 14, 'bold'), foreground='#6a1b9a')
        
        self.display_text("=" * 80, "header")
        self.display_text(f"MEMBER'S BORROWED BOOKS", "header")
        self.display_text("=" * 80, "header")
        self.display_text("")
        self.display_text(member.get_info())
        self.display_text("")
        self.display_text("Borrowed books:")
        
        borrowed_books = member.get_borrowed_books()
        
        if not borrowed_books:
            self.display_text("  No books borrowed.")
        else:
            for i, book in enumerate(borrowed_books, 1):
                self.display_text(f"  {i}. {book.get_info()}")
        
        self.update_status(f"Displaying books for {member.name}")
    
    def borrow_book_dialog(self):
        """Show dialog to borrow a book."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Borrow Book")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Borrow Book", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(dialog, text="Member ID:").pack()
        member_entry = tk.Entry(dialog, width=40)
        member_entry.pack(pady=5)
        member_entry.focus()
        
        tk.Label(dialog, text="Book ISBN:").pack()
        isbn_entry = tk.Entry(dialog, width=40)
        isbn_entry.pack(pady=5)
        
        def perform_borrow():
            member_id = member_entry.get().strip()
            isbn = isbn_entry.get().strip()
            
            if not member_id or not isbn:
                messagebox.showwarning("Input Required", "Please enter both Member ID and Book ISBN.")
                return
            
            dialog.destroy()
            success, message = self.library.lend_book(member_id, isbn)
            
            if success:
                messagebox.showinfo("Success", message)
                self.update_status(message)
            else:
                messagebox.showerror("Error", message)
                self.update_status(f"Error: {message}")
        
        tk.Button(dialog, text="Borrow", command=perform_borrow,
                 bg='#27ae60', fg='black', padx=20, pady=5).pack(pady=10)
    
    def return_book_dialog(self):
        """Show dialog to return a book."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Return Book")
        dialog.geometry("400x200")
        
        tk.Label(dialog, text="Return Book", font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(dialog, text="Member ID:").pack()
        member_entry = tk.Entry(dialog, width=40)
        member_entry.pack(pady=5)
        member_entry.focus()
        
        tk.Label(dialog, text="Book ISBN:").pack()
        isbn_entry = tk.Entry(dialog, width=40)
        isbn_entry.pack(pady=5)
        
        def perform_return():
            member_id = member_entry.get().strip()
            isbn = isbn_entry.get().strip()
            
            if not member_id or not isbn:
                messagebox.showwarning("Input Required", "Please enter both Member ID and Book ISBN.")
                return
            
            dialog.destroy()
            success, message = self.library.return_book(member_id, isbn)
            
            if success:
                messagebox.showinfo("Success", message)
                self.update_status(message)
            else:
                messagebox.showerror("Error", message)
                self.update_status(f"Error: {message}")
        
        tk.Button(dialog, text="Return", command=perform_return,
                 bg='#e67e22', fg='black', padx=20, pady=5).pack(pady=10)
    
    def show_statistics(self):
        """Display library statistics."""
        self.clear_display()
        self.text_display.tag_config("header", font=('Arial', 14, 'bold'), foreground='#00695c')
        
        self.display_text("=" * 80, "header")
        self.display_text("LIBRARY STATISTICS", "header")
        self.display_text("=" * 80, "header")
        self.display_text("")
        
        stats = self.library.get_library_stats()
        
        self.display_text(f"Library Name: {self.library.name}")
        self.display_text("")
        self.display_text("Books:")
        self.display_text(f"  Total Books: {stats['total_books']}")
        self.display_text(f"  Available Books: {stats['available_books']}")
        self.display_text(f"  Borrowed Books: {stats['borrowed_books']}")
        self.display_text(f"  Reference Books (In-Library Only): {stats['reference_books']}")
        self.display_text("")
        self.display_text(f"Members:")
        self.display_text(f"  Total Members: {stats['total_members']}")
        
        self.update_status("Displaying library statistics")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """Library Management System
        
COMP 1023 Lab 10
Object-Oriented Programming

This system demonstrates:
• Class design and encapsulation
• Inheritance and polymorphism
• Special methods
• Object relationships

Developed for HKUST COMP 1023"""
        
        messagebox.showinfo("About", about_text)


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

