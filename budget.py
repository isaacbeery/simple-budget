#!/usr/bin/env python3
# Disclaimer:
# This program is provided "as-is" and comes with no warranty.
# It is for informational purposes only and should not be considered financial
# advice. Use at your own risk. The author is not responsible for any
# financial losses or decisions made as a result of this program.

import argparse
from datetime import datetime
from decimal import Decimal


def currency(amount):
    return f"{amount:,.2f}"


def print_large_table(category, budgeted, spent="", remaining="", percent=""):
    print(
        f"{category:<11}"
        f"{budgeted:>11}"
        f"{spent:>11}"
        f"{remaining:>11}"
        f" {percent:>8}"
    )


def print_small_table(category, month, ytd, projection):
    print(
        f"{category:<8}",
        f"{month:>13}",
        f"{ytd:>13}",
        f"{projection:>13}"
    )


SAVINGS_INDEX = "SAVINGS"
INCOME_INDEX = "INCOME"
BUDGET_INDEX = "BUDGET"

parser = argparse.ArgumentParser(
    prog="budget",
    description="Run calculations on a budget file.",
    epilog='Updates and documentation at https://github.com/isaacbeery'
)
parser.add_argument(
    "-f",
    "--file",
    required=True,
    help="path to budget file"
)
parser.add_argument(
    "-m",
    "--month",
    type=int,
    default=datetime.now().month,
    help="calculate a month other than the current"
)

args = parser.parse_args()
currentMonth = args.month

budget = {}
expenses = {}
monthsInFile = set()
totalIncomeYTD = 0
totalBudgeted = 0
totalSpent = 0
totalSpentYTD = 0

with open(args.file, newline="") as budgetFile:
    for line in budgetFile:
        row = line.split()

        if row and row[0][0] != "#":
            month = int(row[0].split("-")[0])

            if month <= currentMonth:
                monthsInFile.add(month)
                category = row[1]
                amount = Decimal(row[-1])

                if category == BUDGET_INDEX:
                    description = row[2]

                    if description == INCOME_INDEX:
                        totalIncomeYTD += amount

                    if month == currentMonth:
                        budget[description] = amount
                        if description != INCOME_INDEX:
                            totalBudgeted += amount
                else:
                    totalSpentYTD += amount

                    if month == currentMonth:
                        totalSpent += amount

                        if category in expenses:
                            expenses[category] += amount
                        else:
                            expenses[category] = amount

budget[SAVINGS_INDEX] = budget[INCOME_INDEX] - totalBudgeted
expenses[SAVINGS_INDEX] = budget[INCOME_INDEX] - totalSpent

print_large_table("CATEGORY", "BUDGETED", "SPENT", "REMAINING", "PERCENT")

for category in expenses:
    budgeted = budget[category]
    spent = expenses[category]
    percent = round(spent / (totalSpent + expenses[SAVINGS_INDEX]) * 100)

    remaining = ""
    if category != SAVINGS_INDEX:
        remaining = budgeted - spent

    print_large_table(category, budgeted, spent, remaining, f"{percent} %")

for category in budget:
    if category not in expenses and category != INCOME_INDEX:
        print_large_table(category, budget[category])

projectedIncome = round(totalIncomeYTD / len(monthsInFile) * 12, 2)
projectedSpent = round(totalSpentYTD / len(monthsInFile) * 12, 2)

print()
print_small_table("SUMMARY", "MONTH", "YTD", "PROJECTED")
print_small_table(
    "Income",
    currency(budget[INCOME_INDEX]),
    currency(totalIncomeYTD),
    currency(projectedIncome)
)
print_small_table(
    "Spent",
    currency(totalSpent),
    currency(totalSpentYTD),
    currency(projectedSpent)
)
print_small_table(
    "Saved",
    currency(expenses[SAVINGS_INDEX]),
    currency(totalIncomeYTD - totalSpentYTD),
    currency(projectedIncome - projectedSpent)
)
