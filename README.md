# Purpose
`budget.py` is a small, portable application for running calculations on human-writable text files containing budget and expense information.

# How to Use
## Sample File
```
# This entire section is a valid input file.

# Each month has its own budget and expenses.
# Here are the budget entries for January:

01    BUDGET  INCOME 100
01    BUDGET  RENT 20
01    BUDGET  GROCERY 10
01    BUDGET  GIFT 5

# Here are the expense entries for January:

01-01 RENT    Rent 20
01-15 GIFT    Flowers 3.21
01-20 GROCERY Farmer's Market - Apple 1.23

# Although the formatting in January's entries is my favorite,
# February's formatting is also valid:

2 BUDGET INCOME 100
2 BUDGET RENT 20
 2 BUDGET GROCERY 10
02-00 BUDGET GIFT 5
02-01 RENT Rent 20
02-15 GIFT    Flowers                 3.21
02-?  GROCERY Farmer's Market - Apple 1.23

# All twelve months of the year exist in the same file.
# ex. 2025.txt
# When a new year begins, it should exist in a new file.
```

## Run the Application
To view this month's budget and expenses:
```
budget.py -f 2025.txt
```
Replace "2025.txt" with the name of your file.

To view January's budget and expenses:
```
budget.py -f 2025.txt -m 1
```

To view the help page:
```
budget.py --help
```

# Disclaimer
This program is provided "as-is" and comes with no warranty. It is for informational purposes only and should not be considered financial advice. Use at your own risk. The author is not responsible for any financial losses or decisions made as a result of this program.
