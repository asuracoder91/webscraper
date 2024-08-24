# 👇🏻 YOUR CODE 👇🏻:
INCOME_THRESHOLD = 100000
ADDITIONAL_TAX_RATIO = 0.1
NORMAL_TAX_RATIO = 0.15
YEAR_TO_MONTHS = 12


def get_yearly_revenue(monthly_revenue: int) -> int:
    return monthly_revenue * YEAR_TO_MONTHS


def get_yearly_expenses(monthly_expenses: int) -> int:
    return monthly_expenses * YEAR_TO_MONTHS


def get_tax_amount(profit: int) -> float:
    if profit > INCOME_THRESHOLD:
        return ((profit - INCOME_THRESHOLD) * ADDITIONAL_TAX_RATIO) + (
            profit * NORMAL_TAX_RATIO
        )
    else:
        return profit * NORMAL_TAX_RATIO


def apply_tax_credits(tax_amount: float, tax_credits: float) -> float:
    return tax_amount * tax_credits


# /YOUR CODE

# BLUEPRINT | DONT EDIT

monthly_revenue = 5500000
monthly_expenses = 2700000
tax_credits = 0.01

yearly_revenue = get_yearly_revenue(monthly_revenue)
yearly_expenses = get_yearly_expenses(monthly_expenses)

profit = yearly_revenue - yearly_expenses

tax_amount = get_tax_amount(profit)

final_tax_amount = tax_amount - apply_tax_credits(tax_amount, tax_credits)

print(f"Your tax bill is: ${final_tax_amount}")

# /BLUEPRINT
