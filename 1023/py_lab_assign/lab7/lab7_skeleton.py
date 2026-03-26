
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
            title = input("Enter the book title to pop: ").strip()
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
