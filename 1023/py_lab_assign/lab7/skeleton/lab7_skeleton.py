# Simple Library Management System

books = [
    'The Great Gatsby', 
    'To Kill a Mockingbird', 
    '1984', 
    'Pride and Prejudice', 
    'Moby Dick', 
    'The Catcher in the Rye', 
    'The Hobbit', 
    'Brave New World', 
    'The Lord of the Rings', 
    'Fahrenheit 451', 
    'The Alchemist', 
    'Crime and Punishment', 
    'Linear Algebra Done Right', 
]

authors = [
    'F. Scott Fitzgerald', 
    'Harper Lee', 
    'George Orwell', 
    'Jane Austen', 
    'Herman Melville', 
    'J.D. Salinger', 
    'J.R.R. Tolkien', 
    'Aldous Huxley', 
    'J.R.R. Tolkien', 
    'Ray Bradbury', 
    'Paulo Coelho', 
    'Fyodor Dostoevsky', 
    'Sheldon Axler', 
]

availability = [
    True, 
    True, 
    True, 
    True, 
    True, 
    True, 
    True, 
    True,
    True, 
    True, 
    True, 
    True, 
    False,
]

borrowers = [
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None, 
    None,
    None, 
    None, 
    None, 
    None,
    'Tom', 
]

history = [
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    [], 
    ['Tom'], 
]

users = [
    'Tom', 
]

user_borrow_books = [
    ['Linear Algebra Done Right'], 
]


# Functions

def add_book(title, author):
    """
    Adds a new book to the library.

    Parameters:
    - title (str): The title of the book.
    - author (str): The author of the book.
    """

    # TODO: Task 1

    for i in range(len(books)):
        if books[i]==title:
            print(f"Book '{title}' already exists in the library.")
            return
    
    books.append(title)
    authors.append(author)
    availability.append(True)
    borrowers.append(None)
    history.append([])
    print(f"Book '{title}' added to the library.")

def remove_book(title):
    """
    Removes a book from the library.
    Parameters:
    - title (str): The title of the book.
    """

    # TODO: Task 1
    exisit=False
    available=False
    index=0

    for i in range(len(books)):
        if books[i]==title:
            exisit=True
            index=i
            if availability[i]:
                available=True
                break
           
    if not exisit:
        print(f"Book '{title}' does not exist in the library.")
        return

    #if we get the below line it means the book exisits
    #we just need to check its avalibility
    if available:
        i=index
        books.pop(i)
        authors.pop(i)
        availability.pop(i)
        history.pop(i)
        borrowers.pop(i)
        print(f"Book '{title}' has been removed from the library.")

    else:
        print(f"Cannot remove '{title}' as it is currently checked out.")

def check_out_book(username, title):
    """
    Checks out a book to a user.

    Parameters:
    - username (str): The user's name.
    - title (str): The title of the book.
    """
    #checkout is similar to borrow, once u do it, 
    # the book is no longer avaliable

    # TODO: Task 2

    for i in range(len(books)):
        if books[i]==title:
            if availability[i]:
                availability[i]=False
                borrowers[i]=username
                history[i].append(username)
                if not username in users:
                    users.append(username)
                    user_borrow_books.append([title])

                else:
                    user_idx = users.index(username)
                    user_borrow_books[user_idx].append(title)
                    
                print(f"Book '{title}' has been checked out to user '{username}'.")
                return
            else:
                print(f"Book '{title}' is currently not available.")
                return

    print(f"Book '{title}' does not exist in the library.")

def return_book(username, title):
    """
    Returns a book from a user.

    Parameters:
    - username (str): The user's name.
    - title (str): The title of the book.
    """
    # TODO: Task 2
    if not title in books:
        print(f"Book '{title}' does not exist in the library.")
        return
    
    for i in range(len(books)):
        if books[i]==title:
            if availability[i]:
                print(f"Book '{title}' is not currently checked out.")
            else:
                if borrowers[i]==username:
                    availability[i]=True
                    borrowers[i]=None
                    if username in users:
                        user_idx=users.index(username)
                        if title in user_borrow_books[user_idx]:
                            user_borrow_books[user_idx].remove(title)
                            if not user_borrow_books[user_idx]:
                                #when a user's list become empty
                                users.pop(user_idx)
                                user_borrow_books.pop(user_idx)                        
                    print(f"Book '{title}' has been returned by user '{username}'.")
                
                else:
                    print(f"Book '{title}' is not checked out by user '{username}'.")


def search_books(keyword:str, check_avail):
    """
    Searches for books by keyword in the title.

    Parameters:
    - keyword (str): The keyword to search for.
    - check_avail (bool): Whether we only show available books
    """
    # TODO: Task 3

    match=False
    keyword=keyword.lower()

    print('Search results:')
    for i in range(len(books)):
        if keyword in books[i].lower():
            title=books[i]
            author=authors[i]
            if check_avail:
                if availability[i]:
                    #this step is crucial
                    match=True
                    print(f'- {title} by {author}')
            else:
                match=True
                print(f'- {title} by {author}')
    
    if not match:
        print('(No books found with the given keyword)')

def view_borrowing_history(title):
    """
    Views the borrowing history of a book.

    Parameters:
    - title (str): The title of the book.
    """
    # TODO: Task 4
    exsit=False

    for i in range(len(books)):
        if title==books[i]:
            exsit=True
            historys=history[i]
            print(f"Borrowing history for '{title}':")
            if historys:
                for i,browser in enumerate(historys):
                    print(f'{i+1}. {browser}')
            else:
                print('No borrowing history for this book.')

    if not exsit:
         print(f"Book '{title}' does not exist in the library.")

def main():
    """
    Main function to run the library system.
    """
    while True:
        print("\nWelcome to the Simple Library Management System")
        print("Please choose an option:")
        print("1. Add a Book")
        print("2. Remove a Book")
        print("3. Check Out a Book")
        print("4. Return a Book")
        print("5. Search for Books")
        print("6. View Borrowing History")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            title = input("Enter the book title: ").strip()
            author = input("Enter the author name: ").strip()
            add_book(title, author)
        elif choice == '2':
            title = input("Enter the book title to remove: ").strip()
            remove_book(title)
        elif choice == '3':
            username = input("Enter your username: ").strip()
            title = input("Enter the book title to check out: ").strip()
            check_out_book(username, title)
        elif choice == '4':
            username = input("Enter your username: ").strip()
            title = input("Enter the book title to return: ").strip()
            return_book(username, title)
        elif choice == '5':
            keyword = input("Enter a keyword to search for: ").strip()
            show_avail_response = input("List only the available books? (Y/N) ")
            check_avail = (show_avail_response.lower() == "y")
            search_books(keyword, check_avail)
        elif choice == '6':
            title = input("Enter the book title to view history: ").strip()
            view_borrowing_history(title)
        elif choice == '7':
            print("Thank you for using the library system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    main()
