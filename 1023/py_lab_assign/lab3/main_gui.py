import tkinter as tk
from tkinter import ttk
# Import your lab 1 code implementation
from lab3 import task1, task2, task3, task4

class Product:
    """
    A class representing a product of the system
    """
    def __init__(self, name: str, qty: int, cost: float) -> None:
        """
        The initializer
        :param name: The name of the product
        :param qty: The quantity of the product
        :param cost: The cost of the product
        """
        self.__name = name
        self.__qty = qty
        self.__cost = cost

    def __getitem__(self, item: int) -> str | int | float | None:
        """
        Behaviour when the [] operator is used to retrieve information from a Product instance.
        :param item: The index in the operator
        :return: The product name if the item is 0, product quantity if the item is 1, product cost if the item is 2, None otherwise.
        """
        match item:
            case 0:
                return self.__name
            case 1:
                return self.__qty
            case 2:
                return self.__cost
        return None

    def __setitem__(self, key: int, value: str | int | float) -> None:
        """
        Behaviour when the [] operator is used to mutate information in a Product instance.
        :param key: The key in the operator
        :param value: The value being assigned
        """
        match key:
            case 0:
                self.__name = value
            case 1:
                self.__qty = value
            case 2:
                self.__cost = value
            case _:
                raise TypeError("Invalid key.")

    def unpack(self) -> tuple[str, int, float]:
        """
        Unpacks the three data members as a tuple. Used for Lab 1 tasks.
        :return: A tuple containing the name, quantity and cost of the product
        """
        return self.__name, self.__qty, self.__cost


def create_gui(product1: Product, product2: Product) -> None:
    # Create Main Window
    root = tk.Tk()
    root.title("Point-of-Sale System")
    root.geometry(f"{root.winfo_screenwidth() // 2}x{root.winfo_screenheight() // 2}")
    root.minsize(1000, 900)

    # Data storage
    products = [product1, product2]
    paid_amount = tk.StringVar(value="0.00")
    change_amount = tk.StringVar(value="0.00")

    table_font = calc_font = ("Arial", 16)
    table_font_bold = ("Arial", 16, "bold")
    numpad_font = error_font = ("Arial", 24)
    product_font = ("Arial", 18)

    # Configure style
    style = ttk.Style()

    # General theme settings
    style.theme_use('clam')  # Modern theme

    # Colors
    bg_color = "#f0f0f0"
    accent_color = "#4a6fa5"
    button_color = "#e1e5f2"
    button_active_color_dark = "#3a5a8f"
    button_active_color_light = "#d1d7ed"
    total_color = "#2a628f"
    header_color = "#1d3557"
    # Configure root window background
    root.configure(bg=bg_color)

    # Frame styles
    style.configure('TFrame', background=bg_color)
    style.configure('Table.TFrame', background='white', relief='solid', borderwidth=1)

    # Label styles
    style.configure("TLabel", padding=5, font=table_font, background='white')
    style.configure("HeaderCenter.TLabel", font=table_font_bold, anchor='center',
                    foreground='white', background=header_color)
    style.configure("Header.TLabel", font=table_font_bold, anchor='e',
                    foreground='white', background=header_color)
    style.configure("Total.TLabel", font=table_font_bold, foreground=total_color, background='white')
    style.configure("Product.TLabel", font=product_font, background=bg_color)

    # Button styles
    style.configure("Numpad.TButton", font=numpad_font, width=5, background=button_color)
    style.configure("Product.TButton", font=product_font, width=3, background=button_color)
    style.configure("CalculateChange.TButton", font=calc_font, width=18,
                    foreground='white', background=accent_color)
    style.configure("Exit.TButton", font=table_font_bold, foreground='white',
                    background=accent_color, padding=5)

    # Button active states
    style.map('Numpad.TButton',
              background=[('active', button_active_color_light)])
    style.map('Product.TButton',
              background=[('active', button_active_color_light)])
    style.map('CalculateChange.TButton',
              background=[('active', button_active_color_dark)])
    style.map('Exit.TButton',
              background=[('active', button_active_color_dark)])

    # Create a frame for the table with better styling
    table_frame = ttk.Frame(root, padding="10", style='Table.TFrame')
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Create header row in the table frame
    ttk.Label(table_frame, text="Product", style="HeaderCenter.TLabel").grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    ttk.Label(table_frame, text="Cost ($)", style="Header.TLabel").grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    ttk.Label(table_frame, text="Quantity", style="Header.TLabel").grid(row=0, column=2, sticky="ew", padx=5, pady=5)
    ttk.Label(table_frame, text="Total Cost", style="Header.TLabel").grid(row=0, column=3, sticky="ew", padx=5, pady=5)

    # Create table rows for products
    product_labels = {}
    for i, product in enumerate([product1, product2], start=1):
        name, qty, cost = product.unpack()
        ttk.Label(table_frame, text=name, anchor="center").grid(row=i, column=0, sticky="ew", padx=5, pady=5)
        ttk.Label(table_frame, text=f"{cost:.2f}", anchor="e").grid(row=i, column=1, sticky="e", padx=5, pady=5)

        # Quantity and Total labels that will be updated
        qty_label = ttk.Label(table_frame, text=qty, anchor="e")
        qty_label.grid(row=i, column=2, sticky="e", padx=5, pady=5)

        total_label = ttk.Label(table_frame, text=f"{task2(qty, cost):.2f}", anchor="e")
        total_label.grid(row=i, column=3, sticky="e", padx=5, pady=5)

        product_labels[i] = (qty_label, total_label)

    # Create total row
    total_row = len(product_labels) + 1
    ttk.Label(table_frame, text="", style="Total.TLabel").grid(row=total_row, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(table_frame, text="", style="Total.TLabel").grid(row=total_row, column=1, sticky="e", padx=5, pady=5)
    ttk.Label(table_frame, text="Total:", style="Total.TLabel").grid(row=total_row, column=2, sticky="e", padx=5, pady=5)
    grand_total = task3(*(sum(([p[1], p[2]] for p in products), [])))
    grand_total_label = ttk.Label(table_frame, text=f"{grand_total:.2f}", style="Total.TLabel")
    grand_total_label.grid(row=total_row, column=3, sticky="e", padx=5, pady=5)

    # Create paid row
    paid_row = total_row + 1
    ttk.Label(table_frame, text="", style="Total.TLabel").grid(row=paid_row, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(table_frame, text="", style="Total.TLabel").grid(row=paid_row, column=1, sticky="e", padx=5, pady=5)
    ttk.Label(table_frame, text="Paid:", style="Total.TLabel").grid(row=paid_row, column=2, sticky="e", padx=5, pady=5)
    paid_label = ttk.Label(table_frame, textvariable=paid_amount, style="Total.TLabel")
    paid_label.grid(row=paid_row, column=3, sticky="e", padx=5, pady=5)

    # Create change row
    change_row = paid_row + 1
    ttk.Label(table_frame, text="", style="Total.TLabel").grid(row=change_row, column=0, sticky="w", padx=5, pady=5)
    ttk.Label(table_frame, text="", style="Total.TLabel").grid(row=change_row, column=1, sticky="e", padx=5, pady=5)
    ttk.Label(table_frame, text="Change:", style="Total.TLabel").grid(row=change_row, column=2, sticky="e", padx=5, pady=5)
    change_label = ttk.Label(table_frame, textvariable=change_amount, style="Total.TLabel")
    change_label.grid(row=change_row, column=3, sticky="e", padx=5, pady=5)

    # Configure column weights to make them expand
    for i in range(4):
        table_frame.grid_columnconfigure(i, weight=1)

    # Create a frame for the numpad and product controls with better styling
    control_frame = ttk.Frame(root, padding="20")
    control_frame.pack(fill='x', padx=20, pady=10)

    # Numpad frame with better styling
    numpad_frame = ttk.Frame(control_frame, style='Table.TFrame', padding=10)
    numpad_frame.grid(row=0, column=0, padx=20, sticky='n')

    numpad_buttons = [
        ['7', '8', '9', 'X'],
        ['4', '5', '6', 'C'],
        ['1', '2', '3', ' '],
        [' ', '0', '.', ' ']
    ]

    def handle_numpad_input(key: str) -> None:
        current = paid_amount.get()
        # Reset everything
        if key == 'C':
            paid_amount.set("0.00")
            change_amount.set("0.00")
        # Backspace
        elif key == 'X':
            paid_amount.set(current[:-1])
            change_amount.set("0.00")
        # Add decimal point
        elif key == '.':
            if '.' not in current:
                paid_amount.set(current + '.')
        # Number key
        else:
            if current == "0.00":
                paid_amount.set(key)
            # Avoid leading 00
            elif set(current) == {'0'} and key == '0':
                return
            elif '.' in current and current.index('.') == len(current) - 3:
                paid_amount.set(current[:-1] + key)
            else:
                paid_amount.set(current + key)

    # Update numpad buttons with better styling
    for row_idx, row in enumerate(numpad_buttons):
        for col_idx, button_text in enumerate(row):
            if button_text == ' ':
                continue
            btn = ttk.Button(numpad_frame,text=button_text if button_text != 'X' else '\u232B',
                             style="Numpad.TButton",command=lambda text=button_text: handle_numpad_input(text))
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew", ipady=10)

    # Product controls frame with better styling
    product_controls_frame = ttk.Frame(control_frame, style='Table.TFrame', padding=10)
    product_controls_frame.grid(row=0, column=1, padx=20, sticky='n')

    def update_product(product_idx: int, change: int) -> None:
        # Update quantity
        products[product_idx][1] = max(0, products[product_idx][1] + change)
        # Update GUI
        product_labels[product_idx+1][0].config(text=str(products[product_idx][1]))
        # Calculate total
        total = task2(products[product_idx][1], products[product_idx][2])
        product_labels[product_idx+1][1].config(text=f"{total:.2f}")
        # Update the grand total
        grand_total = task3(*(sum(([p[1], p[2]] for p in products), [])))
        grand_total_label.config(text=f"{grand_total:.2f}")

    # Create product controls
    for idx, product in enumerate([product1, product2]):
        name = product[0]
        frame = ttk.Frame(product_controls_frame)
        frame.pack(fill="x", pady=10, ipady=5)

        ttk.Button(frame, text="-", style="Product.TButton",
                   command=lambda idx_=idx: update_product(idx_, -1)).pack(side="left", padx=5)

        ttk.Label(frame, text=name, font=product_font, width=10, anchor='center', style="Product.TLabel").pack(side="left", padx=10)

        ttk.Button(frame, text="+", style="Product.TButton",
                   command=lambda idx_=idx: update_product(idx_, 1)).pack(side="left", padx=5)

    def calculate_change() -> None:
        def create_error_dialog(err_title: str, error_msg: str) -> tk.Toplevel:
            error_root = tk.Toplevel(root)
            error_root.title(f"{err_title} Error")
            error_root.configure(bg=bg_color)

            # The symbol
            error_icon = tk.Label(error_root, text="\u26A0", font=error_font,
                                  fg="#d9534f", bg=bg_color)
            error_icon.pack(pady=(10, 0))

            # The error message
            error_msg_label = tk.Label(error_root, text=error_msg,
                                 font=table_font, bg=bg_color)
            error_msg_label.pack(pady=(0, 10), padx=20)

            # The OK button
            ok_btn = ttk.Button(error_root, text="OK",
                                command=error_root.destroy,
                                style="Header.TButton")
            ok_btn.pack(pady=(0, 10), ipadx=20)

            error_root.geometry(f"+{root.winfo_rootx()+root.winfo_width()//2-150}+{root.winfo_rooty()+root.winfo_height()//2-100}")
            error_root.resizable(False, False)

            return error_root
        try:
            paid = round(float(paid_amount.get()), 2)
            total = float(grand_total_label.cget("text"))
            change = paid - total
            paid_amount.set(f"{paid:.2f}")
            if change >= 0:
                change_amount.set(f"{change:.2f}")
            else:
                create_error_dialog("Payment Error", "Insufficient payment amount.")
        except ValueError:
            create_error_dialog("Input Error", "Please enter a valid payment amount.")

    payment_button = ttk.Button(product_controls_frame, text="Calculate Change", style="CalculateChange.TButton",
                                command=lambda: calculate_change())
    payment_button.pack(pady=10, ipady=5)

    # Create a frame for the exit button at the bottom with better styling
    button_frame = ttk.Frame(root, padding="20")
    button_frame.pack(fill="x", padx=20, pady=10)

    # Add exit button to the button frame
    exit_button = ttk.Button(button_frame, text="Exit", style="Exit.TButton", command=root.destroy)
    exit_button.pack(side="right", padx=5, pady=5, ipadx=20, ipady=5)

    task4(products[0][0], products[0][1], products[0][2], products[1][0], products[1][1], products[1][2])
    root.mainloop()


def main():
    # Get Variables
    user_input = task1()
    product1 = Product(*(user_input[:3]))
    product2 = Product(*(user_input[3:]))
    create_gui(product1, product2)

if __name__ == "__main__":
    main()
