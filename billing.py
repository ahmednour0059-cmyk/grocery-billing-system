"""
billing.py
----------
This module holds the grocery product list and every function that
works with the shopping cart: showing products, adding, viewing,
updating, removing, calculating the total and printing the receipt.

main.py imports this module and calls these functions from its menu.
"""

from datetime import datetime

# ------------------------------------------------------------------
# PRODUCT CATALOGUE (dictionary)
# Key   -> product ID (int)
# Value -> a dictionary with the product name (str) and price (float, RM)
# The prices are sample prices made up for this assignment.
# ------------------------------------------------------------------
PRODUCTS = {
    1: {"name": "Rice (5kg)", "price": 18.90},
    2: {"name": "Cooking Oil (1kg)", "price": 7.50},
    3: {"name": "Sugar (1kg)", "price": 2.85},
    4: {"name": "Fresh Milk (1L)", "price": 7.20},
    5: {"name": "Bread (Loaf)", "price": 4.10},
    6: {"name": "Eggs (10 pcs)", "price": 5.20},
    7: {"name": "Chicken (1kg)", "price": 10.90},
    8: {"name": "Instant Noodles (5 pack)", "price": 5.60},
    9: {"name": "Mineral Water (1.5L)", "price": 1.90},
    10: {"name": "Teh Tarik Mix (10 pack)", "price": 9.50},
}

# ------------------------------------------------------------------
# SHOP RULES (constants)
# ------------------------------------------------------------------
MAX_QUANTITY = 50            # most units of one product allowed in the cart
DISCOUNT_THRESHOLD = 100.00  # spend at least this much (RM) to get a discount
DISCOUNT_RATE = 0.05         # 5% discount
MAX_PAYMENT = 10000.00       # largest cash amount the cashier will accept
LINE = "-" * 60              # separator line used when printing tables


# ==================================================================
# INPUT HELPER FUNCTIONS (error handling and input validation)
# ==================================================================

def get_whole_number(prompt, min_value, max_value):
    """Keep asking until the user types a whole number between
    min_value and max_value (inclusive). Returns that number as an int."""
    while True:
        user_input = input(prompt).strip()
        try:
            number = int(user_input)
        except ValueError:
            # int() fails for text such as "abc", "2.5" or an empty input
            print(f"Invalid input. Please enter a whole number from {min_value} to {max_value}.")
            continue

        if number < min_value or number > max_value:
            print(f"Out of range. Please enter a number from {min_value} to {max_value}.")
        else:
            return number


def get_money_amount(prompt, minimum):
    """Keep asking until the user types a valid amount of money (RM)
    that is at least `minimum`. Returns the amount as a float."""
    while True:
        user_input = input(prompt).strip()
        try:
            amount = float(user_input)
        except ValueError:
            print("Invalid amount. Please enter a number, for example 50 or 50.00.")
            continue

        amount = round(amount, 2)
        if amount < minimum:
            print(f"Not enough. The amount must be at least RM {minimum:.2f}.")
        elif amount > MAX_PAYMENT:
            print(f"Amount too large. The maximum accepted is RM {MAX_PAYMENT:.2f}.")
        else:
            return amount


def get_yes_no(prompt):
    """Ask a yes/no question. Returns True for yes and False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        elif answer in ("n", "no"):
            return False
        else:
            print("Please answer y (yes) or n (no).")


def get_customer_name():
    """Ask for the customer's name. It cannot be empty."""
    while True:
        name = input("Enter customer name: ").strip()
        if name == "":
            print("Name cannot be empty. Please try again.")
        else:
            return name


# ==================================================================
# FEATURE 1: DISPLAY PRODUCTS
# ==================================================================

def display_products():
    """Print every product with its ID and price in RM."""
    print("\n" + LINE)
    print("AVAILABLE PRODUCTS".center(60))
    print(LINE)
    print(f"{'ID':<5}{'Product':<35}{'Price (RM)':>12}")
    print(LINE)
    for product_id in PRODUCTS:
        product = PRODUCTS[product_id]
        print(f"{product_id:<5}{product['name']:<35}{product['price']:>12.2f}")
    print(LINE)


# ==================================================================
# FEATURE 2: ADD TO CART
# The cart is a dictionary: {product_id: quantity}
# ==================================================================

def add_to_cart(cart):
    """Let the user pick a product and a quantity, then add it to the cart."""
    display_products()
    product_id = get_whole_number(f"Enter product ID (1-{len(PRODUCTS)}): ", 1, len(PRODUCTS))

    # How many of this product are already in the cart (0 if none)
    already_in_cart = cart.get(product_id, 0)
    space_left = MAX_QUANTITY - already_in_cart

    if space_left == 0:
        print(f"You already have the maximum of {MAX_QUANTITY} of this product in the cart.")
        return

    quantity = get_whole_number(f"Enter quantity (1-{space_left}): ", 1, space_left)
    cart[product_id] = already_in_cart + quantity

    name = PRODUCTS[product_id]["name"]
    print(f"Added {quantity} x {name} to the cart. (Now {cart[product_id]} in cart)")


# ==================================================================
# FEATURE 3: VIEW CART
# ==================================================================

def view_cart(cart):
    """Print every item in the cart with its quantity and subtotal."""
    if len(cart) == 0:
        print("\nYour cart is empty.")
        return

    print("\n" + LINE)
    print("YOUR SHOPPING CART".center(60))
    print(LINE)
    print(f"{'ID':<5}{'Product':<27}{'Qty':>5}{'Price':>10}{'Subtotal':>13}")
    print(LINE)
    for product_id in cart:
        name = PRODUCTS[product_id]["name"]
        price = PRODUCTS[product_id]["price"]
        quantity = cart[product_id]
        item_subtotal = price * quantity
        print(f"{product_id:<5}{name:<27}{quantity:>5}{price:>10.2f}{item_subtotal:>13.2f}")
    print(LINE)

    subtotal, discount, total = calculate_total(cart)
    print(f"{'Cart total (RM):':<47}{subtotal:>13.2f}")
    print(LINE)


# ==================================================================
# FEATURE 4: UPDATE QUANTITY
# ==================================================================

def update_quantity(cart):
    """Change the quantity of a product that is already in the cart."""
    if len(cart) == 0:
        print("\nYour cart is empty. Nothing to update.")
        return

    view_cart(cart)
    product_id = get_whole_number(f"Enter product ID to update (1-{len(PRODUCTS)}): ", 1, len(PRODUCTS))

    if product_id not in cart:
        print("That product is not in your cart.")
        return

    name = PRODUCTS[product_id]["name"]
    old_quantity = cart[product_id]
    new_quantity = get_whole_number(f"Enter new quantity for {name} (1-{MAX_QUANTITY}): ", 1, MAX_QUANTITY)
    cart[product_id] = new_quantity
    print(f"Updated {name}: {old_quantity} -> {new_quantity}")


# ==================================================================
# FEATURE 5: REMOVE FROM CART
# ==================================================================

def remove_from_cart(cart):
    """Remove one product completely from the cart."""
    if len(cart) == 0:
        print("\nYour cart is empty. Nothing to remove.")
        return

    view_cart(cart)
    product_id = get_whole_number(f"Enter product ID to remove (1-{len(PRODUCTS)}): ", 1, len(PRODUCTS))

    if product_id not in cart:
        print("That product is not in your cart.")
        return

    name = PRODUCTS[product_id]["name"]
    if get_yes_no(f"Remove {name} from the cart? (y/n): "):
        del cart[product_id]
        print(f"{name} has been removed from the cart.")
    else:
        print("Nothing was removed.")


# ==================================================================
# FEATURE 6: CALCULATE TOTAL
# ==================================================================

def calculate_total(cart):
    """Work out the subtotal, discount and final total of the cart.
    Returns three floats: (subtotal, discount, total), each rounded to 2 d.p."""
    subtotal = 0.0
    for product_id in cart:
        subtotal = subtotal + PRODUCTS[product_id]["price"] * cart[product_id]
    subtotal = round(subtotal, 2)

    # Decision: a discount only applies when the subtotal reaches the threshold
    if subtotal >= DISCOUNT_THRESHOLD:
        discount = round(subtotal * DISCOUNT_RATE, 2)
    else:
        discount = 0.0

    # Round each value BEFORE subtracting, so the receipt always adds up
    # (e.g. 102.10 - 5.11 = 96.99, not 97.00)
    total = round(subtotal - discount, 2)
    return subtotal, discount, total


def display_total(cart):
    """Print the subtotal, discount and total to pay."""
    if len(cart) == 0:
        print("\nYour cart is empty. Total: RM 0.00")
        return

    subtotal, discount, total = calculate_total(cart)
    print("\n" + LINE)
    print(f"{'Subtotal (RM):':<47}{subtotal:>13.2f}")
    if discount > 0:
        print(f"{'Discount 5% (RM):':<47}{-discount:>13.2f}")
    else:
        amount_needed = DISCOUNT_THRESHOLD - subtotal
        print(f"Spend RM {amount_needed:.2f} more to get a 5% discount.")
    print(f"{'TOTAL TO PAY (RM):':<47}{total:>13.2f}")
    print(LINE)


# ==================================================================
# FEATURE 7: GENERATE RECEIPT
# ==================================================================

def generate_receipt(cart):
    """Ask for the customer's name and cash payment, then print a
    formatted receipt. Returns True if a receipt was printed, otherwise False."""
    if len(cart) == 0:
        print("\nYour cart is empty. Add products before generating a receipt.")
        return False

    subtotal, discount, total = calculate_total(cart)
    print(f"\nAmount to pay: RM {total:.2f}")
    customer_name = get_customer_name()
    cash_paid = get_money_amount("Enter cash received (RM): ", total)
    change = round(cash_paid - total, 2)
    now = datetime.now().strftime("%d/%m/%Y %I:%M %p")

    # Build the receipt as a list of text lines, then print them all
    receipt_lines = []
    receipt_lines.append("=" * 60)
    receipt_lines.append("GROCERY BILLING SYSTEM".center(60))
    receipt_lines.append("CUSTOMER RECEIPT".center(60))
    receipt_lines.append("=" * 60)
    receipt_lines.append(f"Customer : {customer_name}")
    receipt_lines.append(f"Date     : {now}")
    receipt_lines.append(LINE)
    receipt_lines.append(f"{'Product':<30}{'Qty':>5}{'Price':>10}{'Amount':>15}")
    receipt_lines.append(LINE)
    for product_id in cart:
        name = PRODUCTS[product_id]["name"]
        price = PRODUCTS[product_id]["price"]
        quantity = cart[product_id]
        receipt_lines.append(f"{name:<30}{quantity:>5}{price:>10.2f}{price * quantity:>15.2f}")
    receipt_lines.append(LINE)
    receipt_lines.append(f"{'Subtotal (RM):':<45}{subtotal:>15.2f}")
    receipt_lines.append(f"{'Discount (RM):':<45}{discount:>15.2f}")
    receipt_lines.append(f"{'TOTAL (RM):':<45}{total:>15.2f}")
    receipt_lines.append(f"{'Cash (RM):':<45}{cash_paid:>15.2f}")
    receipt_lines.append(f"{'Change (RM):':<45}{change:>15.2f}")
    receipt_lines.append("=" * 60)
    receipt_lines.append("Thank you for shopping with us!".center(60))
    receipt_lines.append("=" * 60)

    print()
    for line in receipt_lines:
        print(line)
    return True
