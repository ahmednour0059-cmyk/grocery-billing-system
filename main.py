"""
main.py
-------
Entry point of the Grocery Billing System.
Run this file to start the program:   python main.py

This file only handles the menu. The real work (cart, totals,
receipt) is done by the functions in billing.py.
"""

import billing

# The menu options are stored in a list so the menu can be printed with a loop
MENU_OPTIONS = [
    "Display available products",
    "Add product to cart",
    "View cart",
    "Update product quantity",
    "Remove product from cart",
    "Calculate total price",
    "Generate receipt",
    "Exit",
]


def show_menu():
    """Print the main menu."""
    print("\n" + "=" * 40)
    print("GROCERY BILLING SYSTEM".center(40))
    print("=" * 40)
    option_number = 1
    for option in MENU_OPTIONS:
        print(f"{option_number}. {option}")
        option_number = option_number + 1
    print("=" * 40)


def main():
    """Run the menu loop until the user chooses Exit."""
    cart = {}  # empty shopping cart: {product_id: quantity}

    print("Welcome to the Grocery Billing System!")

    while True:
        show_menu()
        choice = billing.get_whole_number(f"Enter your choice (1-{len(MENU_OPTIONS)}): ", 1, len(MENU_OPTIONS))

        if choice == 1:
            billing.display_products()
        elif choice == 2:
            billing.add_to_cart(cart)
        elif choice == 3:
            billing.view_cart(cart)
        elif choice == 4:
            billing.update_quantity(cart)
        elif choice == 5:
            billing.remove_from_cart(cart)
        elif choice == 6:
            billing.display_total(cart)
        elif choice == 7:
            receipt_printed = billing.generate_receipt(cart)
            if receipt_printed:
                cart.clear()  # sale finished, start an empty cart for the next customer
                print("Cart cleared, ready for the next customer.")
        elif choice == 8:
            # Warn the user if they are leaving with unpaid items
            if len(cart) > 0:
                if not billing.get_yes_no("Your cart still has items. Exit anyway? (y/n): "):
                    continue
            print("Thank you for using the Grocery Billing System. Goodbye!")
            break


# Only start the program when this file is run directly (not when imported)
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C or end of input: stop cleanly instead of showing an error
        print("\nProgram stopped. Goodbye!")
