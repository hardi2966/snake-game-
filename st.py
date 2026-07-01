import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class ExpenseTracker:
    def _init_(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        # Initialize an empty DataFrame to store expenses
        self.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])
        self.categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Healthcare', 'Education', 'Other']
        
        # Create GUI components
        self.create_widgets()
    
    def create_widgets(self):
        # Frame for adding expenses
        frame_add = tk.Frame(self.root)
        frame_add.pack(pady=10)

        tk.Label(frame_add, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame_add)
        self.date_entry.grid(row=0, column=1)

        tk.Label(frame_add, text="Category:").grid(row=1, column=0)
        self.category_combobox = ttk.Combobox(frame_add, values=self.categories)
        self.category_combobox.grid(row=1, column=1)

        tk.Label(frame_add, text="Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(frame_add)
        self.amount_entry.grid(row=2, column=1)

        tk.Label(frame_add, text="Description:").grid(row=3, column=0)
        self.description_entry = tk.Entry(frame_add)
        self.description_entry.grid(row=3, column=1)

        self.add_button = tk.Button(frame_add, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=4, columnspan=2, pady=10)

        # Frame for viewing expenses
        frame_view = tk.Frame(self.root)
        frame_view.pack(pady=10)

        self.view_button = tk.Button(frame_view, text="View All Expenses", command=self.view_all_expenses)
        self.view_button.pack(side=tk.LEFT, padx=5)

        self.summary_button = tk.Button(frame_view, text="Show Summary Charts", command=self.show_summary)
        self.summary_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(frame_view, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side=tk.LEFT, padx=5)

    def add_expense(self):
        """Add a new expense with user input"""
        date = self.date_entry.get().strip() or datetime.now().strftime("%Y-%m-%d")
        category = self.category_combobox.get().strip()
        amount = self.amount_entry.get().strip()
        description = self.description_entry.get().strip()

        if not category or not amount:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")
            return

        new_expense = pd.DataFrame({
            'Date': [date],
            'Category': [category],
            'Amount': [amount],
            'Description': [description if description else 'No description']
        })

        self.expenses = pd.concat([self.expenses, new_expense], ignore_index=True)
        messagebox.showinfo("Success", f"Expense added: ₹{amount} for {category} on {date}")

        # Clear input fields
        self.date_entry.delete(0, tk.END)
        self.category_combobox.set('')
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def view_all_expenses(self):
        """Display all expenses in a message box"""
        if self.expenses.empty:
            messagebox.showinfo("No Expenses", "No expenses recorded yet!")
            return
        
        expenses_str = "\n".join(
            f"{row['Date']} | {row['Category']:15} | ₹{row['Amount']:8.2f} | {row['Description']}"
            for _, row in self.expenses.iterrows()
        )
        total_expenses = self.expenses['Amount'].sum()
        messagebox.showinfo("All Expenses", f"Total expenses: ₹{total_expenses:.2f}\n\n{expenses_str}")

    def show_summary(self):
        """Show summary charts using matplotlib"""
        if self.expenses.empty:
            messagebox.showinfo("No Expenses", "No expenses to show! Please add some expenses first.")
            return
        
        summary = self.expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        total_expenses = summary.sum()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        fig.suptitle('Expense Summary Dashboard', fontsize=16, fontweight='bold')

        # Pie chart
        colors = plt.cm.Set3(range(len(summary)))
        ax1.pie(summary.values, labels=summary.index, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.set_title('Expense Distribution by Category', fontweight='bold')

        # Bar chart
        bars = ax2.bar(range(len(summary)), summary.values, color=colors)
        ax2.set_title('Expense Amount by Category', fontweight='bold')
        ax2.set_xlabel('Categories')
        ax2.set_ylabel('Amount (₹)')
        ax2.set_xticks(range(len(summary)))
        ax2.set_xticklabels(summary.index, rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'₹{height:.2f}', ha='center', va='bottom')

        plt.figtext(0.5, 0.01, f'Total Expenses: ₹{total_expenses:.2f}', 
                    ha='center', fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))

        plt.tight_layout()
        plt.show()

    def export_to_csv(self):
        """Export expenses to CSV file"""
        if self.expenses.empty:
            messagebox.showinfo("No Expenses", "No expenses to export!")
            return
        
        filename = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.expenses.to_csv(filename, index=False)
        messagebox.showinfo("Export Successful", f"Expenses exported to {filename}")

# Main execution
if _name_ == "_main_":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()