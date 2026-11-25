# Testing Record

**Date tested:** 25 November 2026
**Environment:** Windows 11, Python 3.12.10

## How the tests were run

Each test case is a fixed list of inputs. The inputs were fed into the real
`main.py` / `billing.py` by a small test script (not part of this project),
and the full console output was saved and checked line by line. One extra
run used the normal `python main.py` command with input redirected from a file.
The money calculation was also checked automatically against 20,000 random carts.

Screenshots for the report should be taken by running `python main.py`
yourself and typing the inputs listed below.

## Test cases and actual results

| ID | Test | Inputs (in order) | Expected | Actual result | Pass? |
|----|------|-------------------|----------|---------------|-------|
| T01 | Full normal flow | 1; 2→1→2; 2→7→3; 3; 4→1→1; 5→7→y; 6; 7→Siti→30; 3; 8 | All 8 features work | Products listed. Cart showed Rice 2 × 18.90 = 37.80, Chicken 3 × 10.90 = 32.70, total 70.50. Rice updated 2→1. Chicken removed. Total 18.90 with message "Spend RM 81.10 more to get a 5% discount". Receipt printed, change RM 11.10. Cart empty after receipt. Exit message shown. | Pass |
| T02 | Invalid menu choices | `abc`, *(empty)*, `0`, `9`, `2.5`, `-1`, `8` | Each rejected, program keeps running | `abc`, empty and `2.5` → "Invalid input…". `0`, `9`, `-1` → "Out of range…". `8` exited normally. | Pass |
| T03 | Add-to-cart validation and limit | 2→`x`,`11`,`0`,3→`-1`,`0`,`51`,`abc`,5; 2→3→`46`,45; 2→3; 3; 8→y | Bad IDs/quantities rejected; max 50 per product | All bad inputs re-asked. Adding Sugar again offered range 1-45 (5 already in cart) and rejected 46. After reaching 50, a third add printed "You already have the maximum of 50…". Cart: Sugar 50 × 2.85 = 142.50. | Pass |
| T04 | Options with an empty cart | 3, 4, 5, 6, 7, 8 | Friendly message, no crash | "Your cart is empty." / "Nothing to update." / "Nothing to remove." / "Total: RM 0.00" / "Add products before generating a receipt." Exit without warning. | Pass |
| T05 | Update/remove item not in cart | 2→2→1; 4→9; 4→2→`0`,`51`,10; 5→9; 5→2→`maybe`,n; 3; 8→y | Rejects missing items and bad quantity | "That product is not in your cart." for ID 9 (both update and remove). Quantities 0 and 51 rejected, 10 accepted (1→10). `maybe` re-asked, `n` → "Nothing was removed." | Pass |
| T06 | Discount + receipt validation | 2→1→6; 6; 7→*(empty)*,*(spaces)*,Ali→`abc`,`50`,`20000`,120; 3; 8 | 5% discount; bad name and payments rejected | Subtotal 113.40, discount 5.67, total 107.73. Empty or space-only name rejected. `abc` → "Invalid amount". `50` → "Not enough… at least RM 107.73". `20000` → "Amount too large". 120 accepted, change RM 12.27. | Pass |
| T07 | Discount just above RM 100 | 2→1→5; 2→3→2; 6; 2→9→1; 6; 7→Ahmad→100; 8 | Discount applies at ≥ RM 100; receipt adds up | 100.20 − 5.01 = 95.19. Then 102.10 − 5.11 = 96.99, change 3.01. | Pass *(after fix, see below)* |
| T08 | Exit with items in cart | 2→5→1; 8→n; 8→y | Warn before exit | Warning shown. `n` returned to menu, `y` exited. | Pass |
| T09 | Input ends suddenly (like Ctrl+C) | 2→5, then input stops | Clean exit, no error trace | "Program stopped. Goodbye!" | Pass |
| T10 | Totals check (automatic) | 20,000 random carts, plus empty cart and a cart worth exactly RM 100.00 | Subtotal − discount = total to the cent; discount only when ≥ RM 100 | 0 mismatches. Empty cart → (0.0, 0.0, 0.0). Exactly RM 100.00 → discount 5.00, total 95.00. | Pass |

## Bug found and fixed during testing

**T07, first run:** the receipt showed Subtotal 102.10, Discount 5.11 and
**TOTAL 97.00**. That is wrong, because 102.10 − 5.11 = 96.99.

**Cause:** the discount (102.10 × 5% = 5.105) was rounded to 5.11 for display,
but the total was calculated from the unrounded 5.105, which gave 96.995 → 97.00.

**Fix:** in `calculate_total()`, round the subtotal and the discount to 2 decimal
places first, and only then subtract to get the total. After the fix, T07 shows
96.99 (change 3.01), and T10 found no mismatches.

## Other observation

When input is piped in from **Windows PowerShell 5.1** (`"2" | python main.py`),
PowerShell adds an invisible byte-order-mark character before the first line,
so the first menu choice is reported as "Invalid input". The program handles
this safely and keeps running. Typing at the keyboard or using `cmd`
redirection (`python main.py < input.txt`) is not affected, so no code change
was made.
