# library_gui.py

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import io
from lab7_skeleton import (
    add_book, remove_book,
    check_out_book, return_book,
    search_books,
    view_borrowing_history
)

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Library Management System")

        # Create Tabs
        self.tab_control = ttk.Notebook(root, padding = 10, width = 500, height = 500)

        self.tab_add = ttk.Frame(self.tab_control)
        self.tab_remove = ttk.Frame(self.tab_control)
        self.tab_checkout = ttk.Frame(self.tab_control)
        self.tab_return = ttk.Frame(self.tab_control)
        self.tab_list = ttk.Frame(self.tab_control)
        self.tab_search = ttk.Frame(self.tab_control)
        self.tab_history = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_add, text='Add Book')
        self.tab_control.add(self.tab_remove, text='Remove Book')
        self.tab_control.add(self.tab_checkout, text='Check Out')
        self.tab_control.add(self.tab_return, text='Return Book')
        self.tab_control.add(self.tab_list, text='List Available')
        self.tab_control.add(self.tab_history, text='Borrowing History')

        self.tab_control.pack(expand=1, fill='both')

        self.create_add_tab()
        self.create_remove_tab()
        self.create_checkout_tab()
        self.create_return_tab()
        self.create_list_tab()
        self.create_history_tab()

    def capture_output(func, *args, **kwargs):
        """
        Captures the printed output of a function.
        """
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
        return redirected_output.getvalue()
    
    def capture_output(self, func, *args, **kwargs):
        """
        Captures the printed output of a function.
        """
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            func(*args, **kwargs)
        finally:
            sys.stdout = sys.__stdout__
        return captured_output.getvalue()

    def create_add_tab(self):
        add_entry = tk.Frame(self.tab_add)

        lbl_title = tk.Label(add_entry, text="Book Title:")
        lbl_title.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.entry_add_title = tk.Entry(add_entry, width=40)
        self.entry_add_title.grid(column=1, row=0, padx=10, pady=10)

        lbl_author = tk.Label(add_entry, text="Author Name:")
        lbl_author.grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.entry_add_author = tk.Entry(add_entry, width=40)
        self.entry_add_author.grid(column=1, row=1, padx=10, pady=10)

        add_entry.pack(expand=True)

        btn_add = tk.Button(self.tab_add, text="Add Book", command=self.add_book_gui)
        btn_add.pack(padx=10, pady=10)

    def add_book_gui(self):
        title = self.entry_add_title.get().strip()
        author = self.entry_add_author.get().strip()
        if title and author:
            # Capture the printed output
            output = self.capture_output(add_book, title, author)
            if "added to the library." in output:
                messagebox.showinfo("Success", output)
                self.entry_add_title.delete(0, tk.END)
                self.entry_add_author.delete(0, tk.END)
            elif "already exists" in output:
                messagebox.showerror("Error", output)
            else:
                messagebox.showwarning("Warning", output)
            self.refresh_all()
        else:
            messagebox.showwarning("Input Error", "Please enter both title and author.")

    def create_remove_tab(self):
        remove_entry = tk.Frame(self.tab_remove)

        lbl_title = tk.Label(remove_entry, text="Book Title:")
        lbl_title.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.entry_remove_title = tk.Entry(remove_entry, width=40)
        self.entry_remove_title.grid(column=1, row=0, padx=10, pady=10)

        remove_entry.pack(expand=True)

        btn_remove = tk.Button(self.tab_remove, text="Remove Book", command=self.remove_book_gui)
        btn_remove.pack(padx=10, pady=10)

    def remove_book_gui(self):
        title = self.entry_remove_title.get().strip()
        if title:
            # Capture the printed output
            output = self.capture_output(remove_book, title)
            if "has been removed" in output:
                messagebox.showinfo("Success", output)
                self.entry_remove_title.delete(0, tk.END)
            elif "currently checked out" in output or "does not exist" in output:
                messagebox.showerror("Error", output)
            else:
                messagebox.showwarning("Warning", output)
            self.refresh_all()
        else:
            messagebox.showwarning("Input Error", "Please enter the book title.")

    def create_checkout_tab(self):
        checkout_entry = tk.Frame(self.tab_checkout)

        lbl_username = tk.Label(checkout_entry, text="Username:")
        lbl_username.grid(column=0, row=0, padx=10, pady=10, sticky='E')
        self.entry_checkout_username = tk.Entry(checkout_entry, width=40)
        self.entry_checkout_username.grid(column=1, row=0, padx=10, pady=10)

        lbl_title = tk.Label(checkout_entry, text="Book Title:")
        lbl_title.grid(column=0, row=1, padx=10, pady=10, sticky='E')
        self.entry_checkout_title = tk.Entry(checkout_entry, width=40)
        self.entry_checkout_title.grid(column=1, row=1, padx=10, pady=10)

        checkout_entry.pack(expand=True)

        btn_checkout = tk.Button(self.tab_checkout, text="Check Out Book", command=self.check_out_gui)
        btn_checkout.pack(padx=10, pady=10)

    def check_out_gui(self):
        username = self.entry_checkout_username.get().strip()
        title = self.entry_checkout_title.get().strip()
        if username and title:
            # Capture the printed output
            output = self.capture_output(check_out_book, username, title)
            if "has been checked out" in output:
                messagebox.showinfo("Success", output)
                self.entry_checkout_username.delete(0, tk.END)
                self.entry_checkout_title.delete(0, tk.END)
            elif "does not exist" in output or "not available" in output:
                messagebox.showerror("Error", output)
            else:
                messagebox.showwarning("Warning", output)
            self.refresh_all()
        else:
            messagebox.showwarning("Input Error", "Please enter both username and book title.")

    def create_return_tab(self):
        return_entry = tk.Frame(self.tab_return)

        lbl_username = tk.Label(return_entry, text="Username:")
        lbl_username.grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.entry_return_username = tk.Entry(return_entry, width=40)
        self.entry_return_username.grid(column=1, row=0, padx=10, pady=10)

        lbl_title = tk.Label(return_entry, text="Book Title:")
        lbl_title.grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.entry_return_title = tk.Entry(return_entry, width=40)
        self.entry_return_title.grid(column=1, row=1, padx=10, pady=10)

        return_entry.pack(expand=True)

        btn_return = tk.Button(self.tab_return, text="Return Book", command=self.return_book_gui)
        btn_return.pack(padx=10, pady=10)

    def return_book_gui(self):
        username = self.entry_return_username.get().strip()
        title = self.entry_return_title.get().strip()
        if username and title:
            # Capture the printed output
            output = self.capture_output(return_book, username, title)
            if "has been returned" in output:
                messagebox.showinfo("Success", output)
                self.entry_return_username.delete(0, tk.END)
                self.entry_return_title.delete(0, tk.END)
            elif "does not exist" in output or "not currently checked out" in output or "not checked out by user" in output:
                messagebox.showerror("Error", output)
            else:
                messagebox.showwarning("Warning", output)
            self.refresh_all()
        else:
            messagebox.showwarning("Input Error", "Please enter both username and book title.")

    def create_list_tab(self):
        filter_entry = tk.Frame(self.tab_list)
        lbl_filter_title = tk.Label(filter_entry, text="Filter keyword:")
        lbl_filter_title.grid(column=0, row=0, padx=5, sticky='w')
        self.original_filter_name = ""
        self.entry_filter_name = tk.Entry(filter_entry, width=40)
        self.entry_filter_name.grid(column=1, row=0, padx=5, sticky='w')
        lbl_check_available = tk.Label(filter_entry, text="Check available:")
        lbl_check_available.grid(column=0, row=1, padx=5, sticky='w')
        self.checkbox_available_var = tk.BooleanVar()
        checkbox_available = tk.Checkbutton(filter_entry, variable=self.checkbox_available_var)
        checkbox_available.grid(column=1, row=1, padx=5, sticky='w')
        filter_entry.pack(pady=10)

        list_btn = tk.Frame(self.tab_list)
        btn_filter = tk.Button(list_btn, text="Filter", command=self.search_books_gui)
        btn_filter.grid(column=0, row=0, padx=5)
        btn_reset = tk.Button(list_btn, text="Reset", command=self.show_all_available_books)
        btn_reset.grid(column=1, row=0, padx=5)
        btn_refresh = tk.Button(list_btn, text="Refresh", command=self.refresh_all)
        btn_refresh.grid(column=2, row=0, padx=5)
        list_btn.pack()

        self.listbox_available = tk.Listbox(self.tab_list)
        self.listbox_available.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.show_all_available_books()

    def show_all_available_books(self):
        self.entry_filter_name.delete(0, tk.END)
        self.search_books_gui()
    
    def search_books_gui(self):
        keyword = self.entry_filter_name.get().strip()
        check_available = self.checkbox_available_var.get()
        self.original_filter_name = keyword
        self.listbox_available.delete(0, tk.END)
        # Capture the printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        search_books(keyword, check_available)
        sys.stdout = sys.__stdout__
        message = captured_output.getvalue()
        lines = message.split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():
                    self.listbox_available.insert(tk.END, line)
        else:
            self.listbox_available.insert(tk.END, "(No books found with the given keyword)")

    def refresh_available_books(self):
        self.entry_filter_name.delete(0, tk.END)
        self.entry_filter_name.insert(0, self.original_filter_name)
        self.search_books_gui()

    def create_history_tab(self):
        history_entry = tk.Frame(self.tab_history)
        lbl_title = tk.Label(history_entry, text="Book Title:")
        lbl_title.grid(column=0, row=0, padx=10, sticky='w')
        self.entry_history_title = tk.Entry(history_entry, width=40)
        self.entry_history_title.grid(column=1, row=0, padx=10)
        history_entry.pack(pady=10)

        btn_view_history = tk.Button(self.tab_history, text="View History", command=self.view_history_gui)
        btn_view_history.pack()

        self.text_history = tk.Text(self.tab_history, state='disabled')
        self.text_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def view_history_gui(self):
        title = self.entry_history_title.get().strip()
        if title:
            self.text_history.config(state='normal')
            self.text_history.delete(1.0, tk.END)
            # Capture the printed output
            captured_output = io.StringIO()
            sys.stdout = captured_output
            view_borrowing_history(title)
            sys.stdout = sys.__stdout__
            message = captured_output.getvalue()
            self.text_history.insert(tk.END, message)
            self.text_history.config(state='disabled')
        else:
            messagebox.showwarning("Input Error", "Please enter the book title.")

    def refresh_all(self):
        self.refresh_available_books()
        self.refresh_search_results()
        self.refresh_history()

    def refresh_search_results(self):
        # Clear search results
        self.entry_filter_name.delete(0, tk.END)
        self.entry_filter_name.insert(0, self.original_filter_name)

    def refresh_history(self):
        # Clear history text
        self.text_history.config(state='normal')
        self.text_history.delete(1.0, tk.END)
        self.text_history.config(state='disabled')

def main():
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
