from expense_original import Expense
import calendar
import datetime

def main():
    print("🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense 
    expense = get_user_expense()
  

    # Write their expense to a file
    save_expense_to_file(expense, expense_file_path)

    # Read file and summarize expense 
    summarize_expense(expense_file_path, budget)
    

def get_user_expense():
    print(f"🎯 Getting User Expense")
    expense_name = input("Enter expense item name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍔 Food", 
        "🏡 Home", 
        "💼 Work", 
        "🎉 Fun", 
        "✨ Misc",
    ]

    while True:
        print("\nSelect a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1
       
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
            return new_expense
        else:
            print("Invalid category. Please try again!")

def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"💾 Saving User Expense: <Expense: {expense.name}, {expense.category}, ${expense.amount:.2f} > to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")

def summarize_expense(expense_file_path, budget):
    print("📊 Summarizing User Expense")
    expenses: list[Expense] = []
    
    # Read and parse expenses from the file
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip():  # Skip empty lines
                expense_name, expense_amount, expense_category = map(str.strip, line.strip().split(","))
                # Standardize category names (strip spaces and make them consistent)
                expense_category = standardize_category_name(expense_category)
                line_expense = Expense(
                    name=expense_name, 
                    amount=float(expense_amount), 
                    category=expense_category,
                )
                expenses.append(line_expense)
    
    # Aggregate expenses by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category.strip()  # Ensure uniformity of category names
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    
    # Display categorized expenses
    print("🧾 Expenses By Category:")
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")

    # Calculate total spent and remaining budget
    total_spent = sum([ex.amount for ex in expenses])
    print(f"\n💵 Total Spent: ${total_spent:.2f}")
    remaining_budget = budget - total_spent
    print(f"💰 Budget Remaining: ${remaining_budget:.2f}")

    # Calculate remaining days in the month and budget per day
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days 

    print(green(f"📅 Budget Per Day: ${daily_budget:.2f}"))

def green(text):
    return f"\033[92m{text}\033[0m"

def standardize_category_name(category_name: str) -> str:
    """Standardize category names to prevent duplicates like '🍔 Food' and 'Food'."""
    category_name = category_name.strip()  # Remove any leading/trailing spaces
    # Optional: You can further normalize category names here if needed
    return category_name

if __name__ == "__main__":
    main()