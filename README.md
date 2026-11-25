# Grocery Billing System

A menu-driven, command-line grocery billing program written in Python.
A cashier can show the product list, build a customer's shopping cart,
change or remove items, see the total (with an automatic discount), and
print a formatted receipt with the change due.

Developed for **BIT2083/BIT1054/BCS2013 Fundamental of Computational Thinking (Python)
- Assignment 2, Task 1**, City University Malaysia.

| Team member | Student ID |
|-------------|------------|
| _Name 1_    | _ID_       |
| _Name 2_    | _ID_       |

---

## Features

| # | Menu option | What it does |
|---|-------------|--------------|
| 1 | Display available products | Shows 10 grocery products with ID and price in RM |
| 2 | Add product to cart | Choose a product ID and quantity; adding the same product again increases its quantity |
| 3 | View cart | Shows every item, quantity, unit price, line subtotal and cart total |
| 4 | Update product quantity | Change the quantity of an item already in the cart |
| 5 | Remove product from cart | Remove an item (asks for y/n confirmation) |
| 6 | Calculate total price | Shows subtotal, discount and total to pay |
| 7 | Generate receipt | Asks for customer name and cash received, prints the receipt with change, then clears the cart for the next customer |
| 8 | Exit | Ends the program (warns first if the cart is not empty) |

### Shop rules

- **Discount:** 5% off when the subtotal is RM 100.00 or more.
- **Quantity limit:** 1 to 50 units of each product per cart.
- **Payment:** cash received must cover the total and be no more than RM 10,000.
- Product prices are **sample prices** made up for this assignment.

### Input validation

The program never crashes on bad input. It re-asks when the user enters:
text instead of a number, decimals where a whole number is needed, an empty
input, a number outside the allowed range, a product that is not in the cart,
an empty customer name, a payment that is too small or too large, or an answer
other than y/n. Pressing `Ctrl+C` exits cleanly.

---

## File structure

```
GroceryBillingSystem/
├── main.py       # Entry point: shows the menu and calls billing functions
├── billing.py    # Product data and all cart / billing / receipt functions
├── TESTING.md    # Test cases and their actual results
├── README.md     # This file
└── .gitignore    # Files Git should not upload (cache, virtual env)
```

**Why two files?** `main.py` handles *what the user chooses* (the menu), while
`billing.py` handles *how each option works*. This keeps each file short and
lets the billing logic be reused or tested without the menu.

### Functions

| File | Function | Purpose |
|------|----------|---------|
| main.py | `show_menu()` | Prints the 8 menu options using a loop over a list |
| main.py | `main()` | Menu loop: reads the choice and calls the matching feature |
| billing.py | `get_whole_number(prompt, min, max)` | Validated whole-number input within a range |
| billing.py | `get_money_amount(prompt, minimum)` | Validated money input (RM) |
| billing.py | `get_yes_no(prompt)` | Validated y/n answer |
| billing.py | `get_customer_name()` | Non-empty name input |
| billing.py | `display_products()` | Feature 1 |
| billing.py | `add_to_cart(cart)` | Feature 2 |
| billing.py | `view_cart(cart)` | Feature 3 |
| billing.py | `update_quantity(cart)` | Feature 4 |
| billing.py | `remove_from_cart(cart)` | Feature 5 |
| billing.py | `calculate_total(cart)` | Feature 6: returns subtotal, discount, total |
| billing.py | `display_total(cart)` | Feature 6: prints the totals |
| billing.py | `generate_receipt(cart)` | Feature 7 |

---

## How to run

**Requirements:** Python 3.8 or newer. No extra libraries are needed
(only `datetime` from the Python standard library).

1. Download or clone this repository:
   ```
   git clone https://github.com/<your-username>/grocery-billing-system.git
   cd grocery-billing-system
   ```
2. Run the program:
   ```
   python main.py
   ```
   (On some systems the command is `python3 main.py` or `py main.py`.)
3. Type a menu number (1-8) and press Enter.

### Example session

```
Enter your choice (1-8): 2
Enter product ID (1-10): 1
Enter quantity (1-50): 2
Added 2 x Rice (5kg) to the cart. (Now 2 in cart)
```

See [TESTING.md](TESTING.md) for full test cases and results.
