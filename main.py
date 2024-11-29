import tkinter as tk
from tkinter import ttk, messagebox
import os


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.users_file_path = "users.csv"
        self.expense_file_path = None
        self.budget = 2000
        self.logged_in_user = None
        

        # Configure styles
        self.configure_styles()

        # Display login page initially
        self.display_login_page()

    def configure_styles(self):
        """Configure styles for the application."""
        self.root.configure(bg="white")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black", font=("Helvetica", 13))
        style.configure("TButton", background="#088ef7", foreground="white", font=("Helvetica", 11, "bold"))
        style.map("TButton", background=[("active", "#088ef7")], foreground=[("active", "white")])
        style.configure("TEntry", fieldbackground="white", foreground="black", font=("Helvetica", 20))
        style.configure("TCombobox", fieldbackground="white", foreground="black", font=("Helvetica", 13))

    def clear_window(self):
        """Clear all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def center_frame(self, frame):
        """Center a frame in the window."""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        frame.columnconfigure(0, weight=1)

    # LOGIN AND SIGNUP 
    def display_login_page(self):
        """Display the login page."""
        self.clear_window()
        login_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(login_frame)

        ttk.Label(login_frame, text="Welcome back", font=("Helvetica", 24, "bold"), foreground="black").grid(column=0, row=0, columnspan=2, pady=10, sticky=tk.N)
        ttk.Label(login_frame, text="").grid(column=0, row=1, pady=5)
        ttk.Label(login_frame, text="Username:").grid(column=0, row=2, pady = 10, sticky=tk.W)
        self.username = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.username, width=30).grid(column=1, row=2, pady = 10, sticky=tk.N)

        ttk.Label(login_frame, text="Password:").grid(column=0, row=3, pady = 10, sticky=tk.W)
        self.password = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.password, width=30, show="*").grid(column=1, row=3, pady = 10, sticky=tk.N)

        ttk.Label(login_frame, text="").grid(column=0, row=4, pady=5)
        ttk.Label(login_frame, text="").grid(column=0, row=5, pady=5)

        ttk.Button(login_frame, text="Login", command=self.login).grid(column=0, row=6, pady=10, columnspan=3, sticky=tk.N, padx=5)
        ttk.Button(login_frame, text="Sign Up", command=self.display_signup_page).grid(column=0, row=7, pady=5, columnspan=3, sticky=tk.N, padx=5)



    def display_signup_page(self):
        """Display the sign-up page."""
        self.clear_window()
        signup_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(signup_frame)

        
        ttk.Label(signup_frame, text="                Sign Up", font=("Helvetica", 24, "bold")).grid(column=0, row=0, pady=10, sticky=tk.N)
        ttk.Label(signup_frame, text="").grid(column=0, row=1, pady=5)
        ttk.Label(signup_frame, text="Username:").grid(column=0, row=2, pady = 10, sticky=tk.W)
        self.username = tk.StringVar()
        ttk.Entry(signup_frame, textvariable=self.username, width=30).grid(column=1, row=2, pady = 10, sticky=tk.N)

        ttk.Label(signup_frame, text="Password:").grid(column=0, row=3, pady = 10, sticky=tk.W)
        self.password = tk.StringVar()
        ttk.Entry(signup_frame, textvariable=self.password, width=30, show="*").grid(column=1, row=3, pady = 10, sticky=tk.N)

        ttk.Label(signup_frame, text="").grid(column=0, row=4, pady=5)
        ttk.Label(signup_frame, text="").grid(column=0, row=5, pady=5)
        ttk.Button(signup_frame, text="      Sign Up      ", command=self.signup).grid(column=0, row=6, pady=10, columnspan=3, sticky=tk.N, padx=5)
        ttk.Button(signup_frame, text=" Back to Login ", command=self.display_login_page).grid(column=0, row=7, pady=5, columnspan=3, sticky=tk.N, padx=5)


    def login(self):
        """Handle user login."""
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not os.path.exists(self.users_file_path):
            messagebox.showerror("Error", "No users found. Please sign up first.")
            return

        with open(self.users_file_path, "r") as f:
            for line in f:
                user, passw = line.strip().split(",")
                if user == username and passw == password:
                    self.logged_in_user = username
                    self.expense_file_path = f"{username}_expenses.csv"
                    self.display_navigation_page()
                    return

        messagebox.showerror("Error", "Invalid username or password.")


    def signup(self):
        """Handle user sign-up."""
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if os.path.exists(self.users_file_path):
            with open(self.users_file_path, "r") as f:
                for line in f:
                    user, _ = line.strip().split(",")
                    if user == username:
                        messagebox.showerror("Error", "Username already exists.")
                        return

        with open(self.users_file_path, "a") as f:
            f.write(f"{username},{password}\n")

        messagebox.showinfo("Success", "Sign-up successful! Please log in.")
        self.display_login_page()


    # NAVIGATION PAGE 
    def display_navigation_page(self):
        """Display the navigation page."""
        self.clear_window()
        nav_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(nav_frame)

        ttk.Label(nav_frame, text=f"Welcome, {self.logged_in_user}!", font=("Helvetica", 24, "bold")).grid(column=0, row=0, pady=10, sticky=tk.N)
        
        ttk.Label(nav_frame, text="").grid(column=0, row=1, pady=5)
        ttk.Button(nav_frame, text="    Add New Expense    ", command=self.display_main_app, width=25, padding=(10, 15)).grid(column=0, row=2, pady=10)
        ttk.Button(nav_frame, text="  Budget Management   ", command=self.display_budget_management_page, width=25, padding=(10, 15)).grid(column=0, row=4, pady=5)
        ttk.Label(nav_frame, text="").grid(column=0, row=5, pady=5)
        ttk.Label(nav_frame, text="").grid(column=0, row=6, pady=5)
        ttk.Button(nav_frame, text="Back", command=self.display_login_page).grid(column=0, row=7, pady=5)


    # MAIN APP (EXPENSE TRACKING)
    def display_main_app(self):
        """Display the main expense tracking page."""
        self.clear_window()
        main_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(main_frame)

        ttk.Label(main_frame, text="Add New Expense", font=("Helvetica", 24, "bold"), foreground="black").grid(column=0, row=0, columnspan=2, pady=10, sticky=tk.N)
        ttk.Label(main_frame, text="Name:").grid(column=0, row=1, pady=5, sticky=tk.W)
        self.expense_name = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.expense_name, width=30).grid(column=1, row=1, sticky=tk.W)

        ttk.Label(main_frame, text="Amount:").grid(column=0, row=2, pady=5, sticky=tk.W)
        self.expense_amount = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.expense_amount, width=30).grid(column=1, row=2, sticky=tk.W)

        ttk.Label(main_frame, text="Category:").grid(column=0, row=3, pady=5, sticky=tk.W)
        self.expense_category = tk.StringVar()
        ttk.Combobox(main_frame, textvariable=self.expense_category, values=["Food", "Home", "Work", "Fun", "Misc"]).grid(column=1, row=3, sticky=tk.W)

        ttk.Label(main_frame, text="").grid(column=0, row=4, pady=5)
        ttk.Label(main_frame, text="").grid(column=0, row=5, pady=5)

        ttk.Button(main_frame, text="  Save Expense  ", command=self.save_expense).grid(column=1, row=6, pady=10, sticky=tk.E)
        ttk.Button(main_frame, text="Back", command=self.display_navigation_page).grid(column=0, row=6, pady=10, columnspan=3, sticky=tk.W, padx=5)

    


    def save_expense(self):
        """Save the expense to the user's file."""
        name = self.expense_name.get().strip()
        amount = self.expense_amount.get().strip()
        category = self.expense_category.get()

        if not name or not amount or not category:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        with open(self.expense_file_path, "a") as f:
            f.write(f"{name},{amount},{category}\n")

        messagebox.showinfo("Success", "Expense saved successfully!")
        self.display_navigation_page()



    # VIEW EXPENSES 
    def view_expenses(self):
        """View all expenses of the logged-in user, including total spent and remaining budget."""
        self.clear_window()
        expenses_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(expenses_frame)

        ttk.Label(expenses_frame, text="Expense Overview", font=("Helvetica", 24, "bold"), foreground="black").grid(column=0, row=0, columnspan=2, pady=10)
        
        # Calculate total expenses and remaining budget
        total_expenses = self.calculate_total_expenses()
        remaining_budget = self.budget - total_expenses
        ttk.Label(expenses_frame, text=f"Total Expenses: ${total_expenses:.2f}", font=("Helvetica", 12), foreground="black").grid(column=0, row=1, columnspan=2, pady=5, sticky=tk.W)
        ttk.Label(expenses_frame, text=f"Remaining Budget: ${remaining_budget:.2f}", font=("Helvetica", 12), foreground="black").grid(column=0, row=2, columnspan=2, pady=5, sticky=tk.W)
                                                                        

        # Display expenses in a Treeview for better formatting
        tree = ttk.Treeview(expenses_frame, columns=("Name", "Amount", "Category"), show="headings", height=10)
        tree.heading("Name", text="Expense Name")
        tree.heading("Amount", text="Amount ($)")
        tree.heading("Category", text="Category")
        tree.column("Name", width=150, anchor=tk.CENTER)
        tree.column("Amount", width=100, anchor=tk.CENTER)
        tree.column("Category", width=100, anchor=tk.CENTER)
        tree.grid(column=0, row=3, columnspan=2, pady=10)

        # Populate Treeview with expense data from the user's file
        if os.path.exists(self.expense_file_path):
            with open(self.expense_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    name, amount, category = line.strip().split(",")
                    tree.insert("", tk.END, values=(name, f"{float(amount):.2f}", category))

        # Remove selected expense functionality
        # Remove selected expense functionality
        def remove_expense():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an expense to remove.")
                return

            # Get the selected expense's data
            expense_data = tree.item(selected_item, "values")
            tree.delete(selected_item)

            # Remove the selected expense from the file
            if os.path.exists(self.expense_file_path):
                with open(self.expense_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                with open(self.expense_file_path, "w", encoding="utf-8") as f:
                    for line in lines:
                        # Match exact expense details
                        name, amount, category = line.strip().split(",")
                        if not (
                            name == expense_data[0]
                            and f"{float(amount):.2f}" == expense_data[1]
                            and category == expense_data[2]
                        ):
                            f.write(line)

            messagebox.showinfo("Success", "Expense removed successfully!")
            self.view_expenses()

        ttk.Button(expenses_frame, text="Remove Selected", command=remove_expense).grid(column=1, row=4, pady=10, sticky=tk.E)
        ttk.Button(expenses_frame, text="Back", command=self.display_navigation_page).grid(column=0, row=4, pady=10, sticky=tk.W)



    def calculate_total_expenses(self):
        total = 0
        if os.path.exists(self.expense_file_path):
            try:
                with open(self.expense_file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        _, amount, _ = line.strip().split(",")
                        total += float(amount)
            except (UnicodeDecodeError, ValueError):
                messagebox.showerror("Error", "Failed to process the expense file. Please check for any data issues.")
        return total


    def view_budget(self):
        """View and update the current budget."""
        self.clear_window()
        budget_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(budget_frame)

    
        ttk.Label(budget_frame, text="Budget Overview", font=("Helvetica", 24, "bold"), foreground="black").grid(column=0, row=0, columnspan=2, pady=10, sticky=tk.N)
        ttk.Label(budget_frame, text=f"Current Budget: ${self.budget}", font=("Helvetica", 12), foreground="black").grid(column=0, row=1, sticky=tk.W, pady=5)
        

        # Entry for new budget
        ttk.Label(budget_frame, text="New Budget:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.new_budget = tk.StringVar()
        ttk.Entry(budget_frame, textvariable=self.new_budget, width=20).grid(column=1, row=2, sticky=tk.W)

        # Update budget button
        def update_budget():
            try:
                new_budget_value = float(self.new_budget.get())
                if new_budget_value < 0:
                    raise ValueError("Budget cannot be negative.")
                self.budget = new_budget_value
                messagebox.showinfo("Success", f"Budget updated to ${self.budget}!")
                self.view_budget()  # Refresh the view
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive number.")

        ttk.Label(budget_frame, text="").grid(column=0, row=3, pady=5)
        ttk.Button(budget_frame, text="Update Budget", command=update_budget).grid(column=1, row=4, pady=10, sticky=tk.E)
        ttk.Button(budget_frame, text="Back", command=self.display_budget_management_page).grid(column=0, row=4, sticky=tk.W)



    # BUDGET MANAGEMENT
    def display_budget_management_page(self):
        """Display the budget management page."""
        self.clear_window()
        budget_frame = ttk.Frame(self.root, padding="20 10 20 10")
        self.center_frame(budget_frame)

        ttk.Label(budget_frame, text="Budget Management", font=("Helvetica", 24, "bold"), foreground="black").grid(column=0, row=0, columnspan=2, pady=10)
        ttk.Label(budget_frame, text="").grid(column=0, row=1, pady=5)
        ttk.Button(budget_frame, text="    View Budget   ", command=self.view_budget, width=25, padding=(10, 15)).grid(column=0, row=2, pady=10)
        ttk.Button(budget_frame, text="  View Expenses   ", command=self.view_expenses, width=25, padding=(10, 15)).grid(column=0, row=4, pady=5)
        ttk.Label(budget_frame, text="").grid(column=0, row=5, pady=5)
        ttk.Label(budget_frame, text="").grid(column=0, row=6, pady=5)
        ttk.Button(budget_frame, text="Back", command=self.display_navigation_page).grid(column=0, row=7, pady=9, columnspan=3, sticky=tk.N, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()