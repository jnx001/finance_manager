import csv
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict

class Expense:
    
    CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Utilities', 'Healthcare', 'Education', 'Other']
    
    def __init__(self, amount: float, category: str, date: str, description: str):
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.date = self._validate_date(date)
        self.description = description.strip()
    
    def _validate_amount(self, amount) -> float:
        try:
            amt = float(amount)
            if amt <= 0:
                raise ValueError("Amount must be positive")
            return round(amt, 2)
        except (ValueError, TypeError):
            raise ValueError("Invalid amount. Must be a positive number.")
    
    def _validate_category(self, category: str) -> str:
        cat = category.strip().title()
        if cat not in self.CATEGORIES:
            raise ValueError(f"Invalid category. Choose from: {', '.join(self.CATEGORIES)}")
        return cat
    
    def _validate_date(self, date: str) -> str:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
    
    def __str__(self) -> str:
        return f"{self.date} | {self.category:15} | ₹{self.amount:>10.2f} | {self.description}"
    
    def to_dict(self) -> Dict:
        return {
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description
        }

class FileManager:
    """Handles all file operations for expense data"""
    
    def __init__(self, filename: str = 'expenses.csv', backup_dir: str = 'backups'):
        self.filename = filename
        self.backup_dir = backup_dir
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directories if they don't exist"""
        os.makedirs(os.path.dirname(self.filename) if os.path.dirname(self.filename) else '.', exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def save_expenses(self, expenses: List[Expense]) -> bool:
        """Save all expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Amount', 'Description'])
                for expense in expenses:
                    writer.writerow([expense.date, expense.category, expense.amount, expense.description])
            return True
        except Exception as e:
            print(f"❌ Error saving expenses: {e}")
            return False
    
    def load_expenses(self) -> List[Expense]:
        """Load expenses from CSV file"""
        expenses = []
        if not os.path.exists(self.filename):
            return expenses
        
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        expense = Expense(
                            amount=row['Amount'],
                            category=row['Category'],
                            date=row['Date'],
                            description=row['Description']
                        )
                        expenses.append(expense)
                    except ValueError as e:
                        print(f"⚠️  Warning: Skipping invalid entry - {e}")
        except Exception as e:
            print(f"❌ Error loading expenses: {e}")
        
        return expenses
    
    def backup_data(self) -> bool:
        """Create a backup of the current expense file"""
        if not os.path.exists(self.filename):
            print("⚠️  No data file to backup")
            return False
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f'expenses_backup_{timestamp}.csv')
            shutil.copy2(self.filename, backup_file)
            print(f"✅ Backup created: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def restore_from_backup(self, backup_filename: str) -> bool:
        """Restore expenses from a backup file"""
        backup_path = os.path.join(self.backup_dir, backup_filename)
        if not os.path.exists(backup_path):
            print(f"❌ Backup file not found: {backup_filename}")
            return False
        
        try:
            shutil.copy2(backup_path, self.filename)
            print(f"✅ Data restored from: {backup_filename}")
            return True
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """List all available backup files"""
        try:
            backups = [f for f in os.listdir(self.backup_dir) if f.startswith('expenses_backup_')]
            return sorted(backups, reverse=True)
        except Exception:
            return []


class ReportGenerator:
    
    @staticmethod
    def generate_summary(expenses: List[Expense]) -> Dict:
        """Generate overall summary statistics"""
        if not expenses:
            return {'total': 0, 'count': 0, 'average': 0, 'categories': {}}
        
        total = sum(exp.amount for exp in expenses)
        count = len(expenses)
        average = total / count
        
        categories = defaultdict(float)
        for exp in expenses:
            categories[exp.category] += exp.amount
        
        return {
            'total': total,
            'count': count,
            'average': average,
            'categories': dict(categories)
        }
    
    @staticmethod
    def generate_monthly_report(expenses: List[Expense], year: int, month: int) -> Dict:
        """Generate report for a specific month"""
        monthly_expenses = [
            exp for exp in expenses
            if datetime.strptime(exp.date, '%Y-%m-%d').year == year
            and datetime.strptime(exp.date, '%Y-%m-%d').month == month
        ]
        return ReportGenerator.generate_summary(monthly_expenses)
    
    @staticmethod
    def get_top_expenses(expenses: List[Expense], n: int = 5) -> List[Expense]:
        """Get top N expenses by amount"""
        return sorted(expenses, key=lambda x: x.amount, reverse=True)[:n]
    
    @staticmethod
    def search_expenses(expenses: List[Expense], keyword: str = '', 
                       category: str = '', start_date: str = '', end_date: str = '') -> List[Expense]:
        """Search expenses by various criteria"""
        results = expenses
        
        if keyword:
            results = [exp for exp in results if keyword.lower() in exp.description.lower()]
        
        if category:
            results = [exp for exp in results if exp.category == category]
        
        if start_date:
            results = [exp for exp in results if exp.date >= start_date]
        
        if end_date:
            results = [exp for exp in results if exp.date <= end_date]
        
        return results


class FinanceManagerUI:
    """Command-line interface for the finance manager"""
    
    def __init__(self):
        self.file_manager = FileManager(filename='data/expenses.csv')
        self.expenses = self.file_manager.load_expenses()
        self.report_gen = ReportGenerator()
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print application header"""
        print("\n" + "=" * 50)
        print("     PERSONAL FINANCE MANAGER".center(50))
        print("=" * 50 + "\n")
    
    def print_menu(self):
        """Display main menu"""
        self.print_header()
        print("MAIN MENU:")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Category-wise Summary")
        print("4. Generate Monthly Report")
        print("5. Search Expenses")
        print("6. View Top Expenses")
        print("7. Backup Data")
        print("8. Restore from Backup")
        print("9. Delete Expense")
        print("0. Exit")
        print("\n" + "-" * 50)
    
    def add_expense(self):
        """Add a new expense"""
        print("\n" + "=" * 50)
        print("ADD NEW EXPENSE")
        print("=" * 50)
        
        try:
            amount = input("Enter amount: ₹")
            
            print(f"\nCategories: {', '.join(Expense.CATEGORIES)}")
            category = input("Enter category: ")
            
            date = input("Enter date (YYYY-MM-DD) [or press Enter for today]: ").strip()
            if not date:
                date = datetime.now().strftime('%Y-%m-%d')
            
            description = input("Enter description: ")
            
            expense = Expense(amount, category, date, description)
            self.expenses.append(expense)
            self.file_manager.save_expenses(self.expenses)
            
            print("\n✅ Expense added successfully!")
            
        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
    
    def view_all_expenses(self):
        """Display all expenses"""
        print("\n" + "=" * 50)
        print("ALL EXPENSES")
        print("=" * 50 + "\n")
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        print(f"{'Date':<12} | {'Category':<15} | {'Amount':>12} | {'Description'}")
        print("-" * 80)
        
        for i, expense in enumerate(sorted(self.expenses, key=lambda x: x.date, reverse=True), 1):
            print(f"[{i:3d}] {expense}")
        
        summary = self.report_gen.generate_summary(self.expenses)
        print("-" * 80)
        print(f"Total Expenses: ₹{summary['total']:.2f} | Count: {summary['count']} | Average: ₹{summary['average']:.2f}")
    
    def view_category_summary(self):
        """Display category-wise expense summary"""
        print("\n" + "=" * 50)
        print("CATEGORY-WISE SUMMARY")
        print("=" * 50 + "\n")
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        summary = self.report_gen.generate_summary(self.expenses)
        total = summary['total']
        
        print(f"{'Category':<20} | {'Amount':>12} | {'Percentage':>10}")
        print("-" * 50)
        
        for category in sorted(summary['categories'].keys()):
            amount = summary['categories'][category]
            percentage = (amount / total * 100) if total > 0 else 0
            print(f"{category:<20} | ₹{amount:>11.2f} | {percentage:>9.1f}%")
        
        print("-" * 50)
        print(f"{'TOTAL':<20} | ₹{total:>11.2f} | {100:>9.1f}%")
    
    def generate_monthly_report(self):
        """Generate and display monthly report"""
        print("\n" + "=" * 50)
        print("MONTHLY REPORT")
        print("=" * 50 + "\n")
        
        try:
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            
            if not (1 <= month <= 12):
                print("❌ Invalid month. Must be between 1 and 12.")
                return
            
            report = self.report_gen.generate_monthly_report(self.expenses, year, month)
            
            month_name = datetime(year, month, 1).strftime('%B %Y')
            print(f"\nReport for {month_name}")
            print("-" * 50)
            
            if report['count'] == 0:
                print("No expenses for this month.")
                return
            
            print(f"Total Expenses: ₹{report['total']:.2f}")
            print(f"Number of Transactions: {report['count']}")
            print(f"Average per Transaction: ₹{report['average']:.2f}")
            
            print("\nCategory Breakdown:")
            for category, amount in sorted(report['categories'].items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / report['total'] * 100)
                print(f"  {category:<20}: ₹{amount:>10.2f} ({percentage:>5.1f}%)")
        
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
    
    def search_expenses(self):
        """Search expenses by criteria"""
        print("\n" + "=" * 50)
        print("SEARCH EXPENSES")
        print("=" * 50 + "\n")
        
        keyword = input("Enter keyword (or press Enter to skip): ").strip()
        
        print(f"\nCategories: {', '.join(Expense.CATEGORIES)}")
        category = input("Enter category (or press Enter to skip): ").strip().title()
        
        start_date = input("Enter start date (YYYY-MM-DD) (or press Enter to skip): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD) (or press Enter to skip): ").strip()
        
        results = self.report_gen.search_expenses(
            self.expenses, 
            keyword=keyword, 
            category=category if category in Expense.CATEGORIES else '',
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"\nFound {len(results)} matching expenses:\n")
        
        if results:
            print(f"{'Date':<12} | {'Category':<15} | {'Amount':>12} | {'Description'}")
            print("-" * 80)
            for expense in sorted(results, key=lambda x: x.date, reverse=True):
                print(expense)
        else:
            print("No matching expenses found.")
    
    def view_top_expenses(self):
        """Display top expenses"""
        print("\n" + "=" * 50)
        print("TOP EXPENSES")
        print("=" * 50 + "\n")
        
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        
        try:
            n = int(input("How many top expenses to display? (default: 5): ") or "5")
            top = self.report_gen.get_top_expenses(self.expenses, n)
            
            print(f"\nTop {len(top)} Expenses:")
            print(f"{'Date':<12} | {'Category':<15} | {'Amount':>12} | {'Description'}")
            print("-" * 80)
            
            for i, expense in enumerate(top, 1):
                print(f"[{i}] {expense}")
        
        except ValueError:
            print("❌ Invalid number")
    
    def backup_data(self):
        """Create data backup"""
        print("\n" + "=" * 50)
        print("BACKUP DATA")
        print("=" * 50 + "\n")
        
        self.file_manager.backup_data()
    
    def restore_from_backup(self):
        """Restore data from backup"""
        print("\n" + "=" * 50)
        print("RESTORE FROM BACKUP")
        print("=" * 50 + "\n")
        
        backups = self.file_manager.list_backups()
        
        if not backups:
            print("No backup files found.")
            return
        
        print("Available backups:")
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup}")
        
        try:
            choice = int(input("\nEnter backup number to restore: "))
            if 1 <= choice <= len(backups):
                if self.file_manager.restore_from_backup(backups[choice - 1]):
                    self.expenses = self.file_manager.load_expenses()
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Invalid input")
    
    def delete_expense(self):
        """Delete an expense"""
        print("\n" + "=" * 50)
        print("DELETE EXPENSE")
        print("=" * 50 + "\n")
        
        if not self.expenses:
            print("No expenses to delete.")
            return
        
        self.view_all_expenses()
        
        try:
            choice = int(input("\nEnter expense number to delete (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.expenses):
                sorted_expenses = sorted(self.expenses, key=lambda x: x.date, reverse=True)
                expense_to_delete = sorted_expenses[choice - 1]
                
                confirm = input(f"\nDelete: {expense_to_delete}\nAre you sure? (yes/no): ").lower()
                if confirm == 'yes':
                    self.expenses.remove(expense_to_delete)
                    self.file_manager.save_expenses(self.expenses)
                    print("✅ Expense deleted successfully!")
                else:
                    print("❌ Deletion cancelled.")
            else:
                print("❌ Invalid expense number")
        except ValueError:
            print("❌ Invalid input")
    
    def run(self):
        """Main application loop"""
        while True:
            self.print_menu()
            
            try:
                choice = input("Enter your choice (0-9): ").strip()
                
                if choice == '1':
                    self.add_expense()
                elif choice == '2':
                    self.view_all_expenses()
                elif choice == '3':
                    self.view_category_summary()
                elif choice == '4':
                    self.generate_monthly_report()
                elif choice == '5':
                    self.search_expenses()
                elif choice == '6':
                    self.view_top_expenses()
                elif choice == '7':
                    self.backup_data()
                elif choice == '8':
                    self.restore_from_backup()
                elif choice == '9':
                    self.delete_expense()
                elif choice == '0':
                    print("\n" + "=" * 50)
                    print("Thank you for using Personal Finance Manager!")
                    print("=" * 50 + "\n")
                    break
                else:
                    print("\n❌ Invalid choice. Please try again.")
                
                if choice != '0':
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {e}")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = FinanceManagerUI()
    app.run()