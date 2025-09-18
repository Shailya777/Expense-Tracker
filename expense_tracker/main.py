# ==================================================== Imports ====================================================#

import sys
from datetime import datetime
from decimal import Decimal

from unicodedata import category

# Importing Services:
from services.user_service import UserService
from services.account_service import AccountService
from services.transaction_service import TransactionService
from services.budget_service import BudgetService
from services.category_service import CategoryService
from services.merchant_service import MerchantService
from services.analytics_service import AnalyticsService

# Importing Core Modules:
from core.db_conn import DatabaseConnection
from core.auth import AuthManager
from core.exceptions import *

# Importing Utilities:
from utils.cli_helpers import *
from utils.validators import *

# Importing Analytics Functions:
from analytics import reports, charts

# =================================================================================================================#

class ExpenseTrackerCLI:

    def __init__(self):
        self.user_service = UserService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.budget_service = BudgetService()
        self.category_service = CategoryService()
        self.merchant_servie = MerchantService()
        self.analytics_service = AnalyticsService()

#===================================================================================================================#
    def run(self):

        while True:
            if not AuthManager.is_authenticated():
                self._startup_menu()
            else:
                self._main_menu()


    def _startup_menu(self):

        clear_screen(); print_title('Welcome to Expense Tracker!!')
        print('1. Register')
        print('2. Login')
        print('3. Exit')

        choice = get_input('> ', error_message= 'Please Enter a Number:')

        if choice == '1': self._handle_registration()
        elif choice == '2': self._handle_login()
        elif choice == '3':
            print('Goodbye! Have a Nice Day!!')
            sys.exit(0)


    def _main_menu(self):

        user = AuthManager.get_current_user()
        clear_screen(); print_title(f'Main Menu (Logged in as: {user.username})')
        print('1. Manage Accounts')
        print('2. Manage Categories')
        print('3. Add/View Transactions')
        print('4. Manage Budgets')
        print('5. Run Expense Analysis')
        print('6. Export/Import CSV')

        if AuthManager.is_admin():
            print('8. Admin: Manage Users')

        print('9. Logout')

        choice = get_input('> ')

        if choice == '1': self._manage_accounts()
        elif choice == '2': self._manage_categories()
        elif choice == '3': self._manage_transactions()
        elif choice == '4': self._manage_budgets()
        elif choice == '5': self._run_expense_analysis()
        elif choice == '6': self._handle_csv_operations()
        elif choice == '8' and AuthManager.is_admin(): self._admin_manage_users()
        elif choice == '9': self._handle_logout()

# ===================================================================================================================#
    def _handle_registration(self):

        clear_screen(); print_title('Register New User')

        try:
            username = get_input('Username', validate_not_empty, 'UserName Can Not be Empty.')

            email = get_input('Email', validate_email, 'Invalid Email Format.')

            password = get_password_input()

            if not validate_password(password):
                raise ValidationError('Password Must be at least 8 Characters Long.')

            user = self.user_service.register(username, email, password)

            print(f"\nUser '{user.username}' Registered Successfully!!")

        except (ValueError, ValidationError) as e:
            print(f"\nRegistration Failed: {e}")

        input('\nPress Enter to Continue...')


    def _handle_login(self):

        clear_screen(); print_title('User Login')

        try:
            email = get_input('Email', validate_email, 'Invalid Email Format.')
            password = get_password_input()
            user = self.user_service.login(email, password)

            if user:
                AuthManager.login(user)
                print(f'\nWelcome Back, {user.username}')

            else:
                raise AuthenticationError('Invalid Email or password.')

        except AuthenticationError as e:
            print(f'\nLogin Failed: {e}')

        input('\nPress Enter to Continue...')


    def _handle_logout(self):
        AuthManager.logout()
        print('\nYou Have Been Logged Out.')
        input('Press Enter to Continue...')

# ===================================================================================================================#
    def _handle_add_account(self):
        """
        Handles the logic for adding a new financial account.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Add New Account')

        try:
            name = get_input('Enter Account Name')
            if not validate_not_empty(name):
                raise ValueError("Account name cannot be empty.")

            print('Available Account Types: [1]Cash, [2]Bank, [3]Credit Card')
            type_choice = get_input('Choose Account Type', lambda c: c if c in ['1','2','3'] else None)

            type_map = {'1': 'CashAccount',
                        '2': 'BankAccount',
                        '3': 'CreditCardAccount'}

            account_type = type_map[type_choice]

            balance_str = get_input('Enter Initial Balance (e.g. 500.00)') or '0.0'
            balance = Decimal(balance_str)

            self.account_service.create_account(user.id, name, account_type, balance)
            print('\nAccount Created Successfully!')

        except Exception as e:
            print(f'\nError Creating Account: {e}')

        input('\nPress Enter to Continue...')

    def _handle_edit_account(self):
        """
        Handles the logic for editing an account's name.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Edit Account Name')

        account_id_str = get_input('Enter Account ID to Edit', lambda i: i if i.isdigit() else None)
        if not account_id_str:
            return

        new_name = get_input('Enter New Name for The Account')
        if not validate_not_empty(new_name):
            raise ValueError("Account name cannot be empty.")

        if self.account_service.update_account_name(int(account_id_str), user.id, new_name):
            print('\nAccount Updated Successfully!')
        else:
            print('\nFailed To Update Account. Please Check The ID.')

        input('\nPress Enter to Continue...')

    def _handle_delete_account(self):
        """
        Handles the logic for deleting an account.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Delete Account')

        account_id_str = get_input('Enter Account ID to Delete', lambda i: i if i.isdigit() else None)
        if not account_id_str:
            return

        confirm = get_input(f'Are You Sure You Want to Delete Account {account_id_str}?? This will Also Delete all Associated Transactions. [y/n]').lower()
        if confirm == 'y':
            if self.account_service.delete_account(int(account_id_str), user.id):
                print('\nAccount Deleted Successfully!')
            else:
                print('\nFailed to Delete Account. Please Check The ID.')
        else:
            print('\nDeletion Cancelled.')

        input('\nPress Enter to Continue...')

    def _manage_accounts(self):
        """
        Sub-menu for viewing, adding, editing, and deleting accounts.
        """

        user = AuthManager.get_current_user()

        while True:
            clear_screen(); print_title('Manage Accounts')

            accounts = self.account_service.get_user_accounts(user.id)
            headers = ['ID','Name','Type','Balance']
            data = [{'id': acc.id,
                 'name': acc.name,
                 'type': acc.account_type,
                 'balance': f"{acc.balance:.2f}"}
                for acc in accounts]
            print_table(data= data, headers= headers)

            print('\nOptions: [A]dd, [E]dit, [D]elete, [B]ack to Main Menu')
            choice = get_input('> ').lower()

            if choice == 'a':
                self._handle_add_account()
            elif choice == 'e':
                self._handle_edit_account()
            elif choice == 'd':
                self._handle_delete_account()
            elif choice == 'b':
                break
            else:
                print('Invalid Option.')
                input('\nPress Enter to Continue...')

# ===================================================================================================================#
    def _manage_categories(self):

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Manage Categories')

        categories = self.category_service.get_user_categories(user.id)
        headers = ['ID','Name','Type','Parent ID']
        data = [{
            'id': cat.id,
            'name': cat.name,
            'type': cat.type,
            'parent_id': cat.parent_id or 'N/A'
        } for cat in categories]
        print_table(data= data, headers= headers)

        print('\nOptions: [A]dd, [D]elete, [B]ack')
        choice = get_input('> ').lower()

        if choice == 'a':
            raw_name = input('Category Name: ').strip()
            if not validate_not_empty(raw_name):
                raise ValueError("Category name cannot be empty.")
            name = raw_name
            cat_type = get_input('Type (income/expense)', lambda t : t if t in ['income', 'expense'] else None)
            parent_id_str = get_input('Parent ID (Optional, Press Enter to Skip)')
            parent_id = int(parent_id_str) if parent_id_str.isdigit() else None

            try:
                self.category_service.create_category(user.id, name, cat_type, parent_id)
                print('Category Added Successfully.')

            except Exception as e:
                print(f'Error: {e}')

            input('\nPress Enter To Continue...')

        elif choice == 'd':
            cat_id_str = get_input('Enter Category ID to Delete', lambda i : i if i.isdigit() else None)

            if cat_id_str:
                if self.category_service.delete_category(int(cat_id_str), user.id):
                    print('Category Deleted.')

                else:
                    print('Category Not Found OR Could Not be Deleted.')

                input('\nPress Enter to Continue...')

# ===================================================================================================================#

    def _handle_add_transaction(self):
        """
        Handles the logic for adding a new transaction.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Add New Transaction')

        try:
            # Showing Available Accounts to User:
            print('Your Accounts:')
            accounts = self.account_service.get_user_accounts(user.id)
            acc_headers = ['ID','Name','Type']
            acc_data = [{
                'id': acc.id,
                'name': acc.name,
                'type': acc.account_type
            } for acc in accounts]

            print_table(data= acc_data, headers= acc_headers)

            account_id = int(get_input('\nEnter Account ID', lambda i: i if i.isdigit() else None))

            # Showing Available Categories to User:
            print('\nYour Categories:')
            categories = self.category_service.get_user_categories(user.id)
            cat_headers = ['ID','Name','Type']
            cat_data = [{
                'id': cat.id,
                'name': cat.name,
                'type': cat.type
            } for cat in categories]
            print_table(data= cat_data, headers= cat_headers)
            category_id = int(get_input('\nEnter Category ID', lambda i: i if i.isdigit() else None))

            amount_str = get_input('\nEnter Amount', error_message= 'Please Enter a Valid Number.')
            amount = validate_amount(amount_str)
            if amount is None:
                raise ValidationError('Amount Must be a Positive Number.')

            trans_type = get_input('Enter Type (income/expense)', lambda t: t if t in ['income','expense'] else None)

            date_str = get_input('Enter Date(YYYY-MM-DD, Press Enter for Today)')
            trans_date = validate_date(date_str) if date_str else datetime.now()

            description = get_input('Enter Description(optional)')

            self.transaction_service.add_transaction(
                user_id= user.id,
                account_id= account_id,
                category_id= category_id,
                amount= amount,
                transaction_type= trans_type,
                transaction_date= trans_date,
                description= description
            )
            print('\nTransaction Added Successfully!!')

        except(ValidationError, ValueError) as e:
            print(f'\nError: {e}')
        except Exception as e:
            print(f'An Unexpected Error Occurred while Adding The Transaction: {e}')

        input('\nPress Enter to Continue...')


    def _handle_delete_transaction(self):
        """
        Handles the logic for deleting a transaction.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Delete Transaction')

        trans_id_str = get_input('Enter The ID of the Transaction You Want to Delete', lambda i: i if i.isdigit() else None)

        if trans_id_str:
            trans_id = int(trans_id_str)

            if self.transaction_service.delete_transaction(trans_id, user.id):
                print(f'\nTransaction with ID {trans_id} has been Deleted Successfully.')

            else:
                print(f'\nCould Not Delete Transaction. Make Sure The ID is Correct and Belongs to Your Transaction.')

        input('\nPress Enter to Continue...')


    def _handle_edit_transaction(self):
        """
        Edits An Already Created Transaction.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Edit Transaction')

        trans_id_str = get_input('Enter Transaction ID to Edit', lambda i: i if i.isdigit() else None)

        if not trans_id_str:
            return

        trans = self.transaction_service.get_transaction_by_id(int(trans_id_str), user.id)
        if not trans:
            print('Transaction Not Found.')
            input('Press Enter...')
            return

        print('\nEditing Transaction. Press Enter to Keep The Current Value.')

        # Editing Date:
        new_date_str = get_input(f'Date (YYYY-MM-DD) (Current: {trans.transaction_date.strftime('%Y-%m-%d')})')
        new_date = validate_date(new_date_str) if new_date_str else trans.transaction_date

        # Editing Account:
        print('\nYour Accounts:')
        accounts = self.account_service.get_user_accounts(user.id)
        print_table([{
            'id': acc.id,
            'name': acc.name
        } for acc in accounts], headers= ['ID','Name'])
        new_account_id_str = get_input(f'Account ID (Current: {trans.account_id})')
        new_account_id = int(new_account_id_str) if new_account_id_str else trans.account_id

        # Editing Category:
        print('\nYour Categories:')
        categories = self.category_service.get_user_categories(user.id)
        print_table([{
            'id': cat.id,
            'name': cat.name,
            'type': cat.type
        } for cat in categories], headers= ['ID','Name','Type'])
        new_category_id_str = get_input(f'Category ID (Current: {trans.category_id})')
        new_category_id = int(new_category_id_str) if new_account_id_str else trans.category_id

        # Editing Amount and Description:
        new_amount_str = get_input(f'Amount (Current: {trans.amount})')
        new_amount = validate_amount(new_amount_str) if new_amount_str else trans.amount

        new_desc = get_input(f'Description (Current: {trans.description})')
        final_desc = new_desc if new_desc is not None else trans.description

        new_data = {
            'transaction_date': new_date,
            'account_id': new_account_id,
            'category_id': new_category_id,
            'amount': new_amount,
            'description': final_desc
        }

        if self.transaction_service.update_transaction(trans.id, user.id, new_data):
            print('\nTransaction Updated Successfully.')
        else:
            print('\nFailed to Update Transaction.')

        input('\nPress Enter to Continue..')


    def _manage_transactions(self):

        user = AuthManager.get_current_user()

        while True:
            clear_screen(); print_title('Manage Transactions')

            transactions = self.transaction_service.get_user_transaction(user.id)
            headers = ['ID','Date','Type','Amount','Category','Account','Description']
            data = [{
                'id': t.id,
                'date': t.transaction_date.strftime('%Y-%m-%d'),
                'type': t.transaction_type,
                'amount': f"{t.amount:.2f}",
                'category': getattr(t, 'category_name','N/A'),
                'account': getattr(t, 'account_name', 'N/A'),
                'description': t.description
            } for t in transactions]
            print_table(data= data, headers= headers)

            print('\n Options: [A]dd, [E]dit, [D]elete, [B]ack to Main Menu')
            choice = get_input('> ').lower()

            if choice == 'a':
                self._handle_add_transaction()
            elif choice == 'e':
                self._handle_edit_transaction()
            elif choice == 'd':
                self._handle_delete_transaction()
            elif choice == 'b':
                break

# ===================================================================================================================#
    def _handle_set_budget(self):
        """
        Handles the logic for setting or updating a budget for a given category and month.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Set/Update Budget')

        try:
            year_str = get_input('Enter Year for The Budget (e.g 2025)', lambda y: y if y.isdigit() and len(y) == 4 else None)
            month_str = get_input('Enter Month for The Budget (1-12)', lambda m: m if m.isdigit() and 1<= int(m) <= 12 else None)

            print('\nYour Expense Categories:')
            categories = [c for c in self.category_service.get_user_categories(user.id) if c.type == 'expense']
            print_table(data= [{
                'id': cat.id,
                'name': cat.name
            } for cat in categories], headers= ['ID','Name'])

            category_id_str = get_input('Enter Category ID to Set Budget for', lambda i: i if i.sidigit() else None)
            amount_str = get_input('Enter Budget Amount', error_message= 'Please Enter a Valid Number.')
            amount = validate_amount(amount_str)

            if not all([year_str, month_str, category_id_str, amount]):
                raise ValidationError('All Fields are Required and Must be Valid.')

            self.budget_service.set_budget(
                user_id= user.id,
                category_id= int(category_id_str),
                amount= amount,
                year= int(year_str),
                month= int(month_str)
            )
            print('\nBudget Set/Updated Successfully!')

        except (ValidationError, ValueError) as e:
            print(f'Error: {e}')
        except Exception as e:
            print(f'\nAn Unexpected Error Occurred: {e}')

        input('\nPress Enter to Continue...')

    def _manage_budgets(self):
        """
        Sub-menu for viewing and setting/updating budgets.
        """

        user = AuthManager.get_current_user()

        while True:
            clear_screen(); print_title('Manage Budgets')
            print("First, let's View Budgets for a Specific Month.")

            year_str = get_input('Enter Year (e.g. 2025)', lambda y: y if y.isdigit() and len(y) == 4 else None, "Invalid Year.")
            month_str = get_input('Enter Month (1-12)', lambda m: m if m.isdigit() and 1 <= int(m) <= 12 else None, "Invalid Month.")

            if not year_str or not month_str:
                return

            year, month = int(year_str), int(month_str)
            budgets = self.budget_service.get_budgets_for_period(user.id, year, month)
            headers = ['ID', 'Category', 'Type', 'Amount']
            data = [{
                'id': b['id'],
                'category': b['category_name'],
                'type': b['category_type'],
                'amount': f'{b['amount']:.2f}'
            } for b in budgets]
            print_table(data= data, headers= headers)

            print('\nOptions: [S]et/Update a Budget, [B]ack to Main Menu')
            choice = get_input('> ').lower()

            if choice == 's':
                self._handle_set_budget()
            elif choice == 'b':
                break
            else:
                print('Invalid Option.')
                input('\nPress Enter to Continue...')

# ===================================================================================================================#
    def _run_expense_analysis(self):
        """
        Handles Analysis of Expenses and Provides Charts of Choice to User.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Expense Analysis')
        print('1. Monthly Expense Trend')
        print("2. Expense Breakdown by Category")
        print('3. Budget vs Actual Spending')
        choice = get_input('> ')

        df = self.analytics_service.get_transactions_as_dataframe(user.id)

        if df.empty:
            print('\nNo Transaction Data Available for Analysis.')
            input('Press Enter...')
            return

        if choice == '1':
            trend_df = reports.monthly_expense_trend(df)
            path = charts.plot_monthly_trend(trend_df= trend_df, user_id= user.id)
            print(f'\nChart Saved to: {path}')

        elif choice == '2':
            cat_df = reports.category_breakdown(df)
            path = charts.plot_category_breakdown(cat_df, user.id)
            print(f'\nChart Saved to: {path}')

        elif choice == '3':
            year = int(get_input('Enter Year for Analysis (e.g. 2025)', lambda y: y if y.isdigit() else None))
            month = int(get_input('Enter Month for Analysis (1-12)', lambda m: m if m.isdigit() else None))
            bva_df = reports.budget_vs_actual(user.id, year, month, df)
            path = charts.plot_budget_vs_actual(bva_df, user.id, year, month)
            print(f'\nChart Saved to: {path}')

        input('\nPress Enter to Continue...')

    def _handle_csv_operations(self):
        """
        Handles Exporting Transaction Data to CSV File and Importing Transactions from CSV File.
        """

        user = AuthManager.get_current_user()
        clear_screen(); print_title('Export/Import Transactions')
        print('1. Export All transactions to CSV')
        print('2. Import Transactions from CSV')
        choice = get_input('> ')

        if choice == '1':
            filename = get_input('Enter FileName to Save Transactions into (e.g. export.csv)', validate_not_empty)
            result = self.transaction_service.export_transaction_to_csv(user.id, filename)
            print(f'\n{result}')

        elif choice == '2':
            filename = get_input('Enter FileName to Import (e.g. sample_transactions.csv)', validate_not_empty)
            result = self.transaction_service.import_transactions_from_csv(user.id, filename)
            print(f'\n{result}')

        input('\nPress Enter to Continue...')

# ===================================================================================================================#
    def _admin_manage_users(self):
        """
        Handles Admin's Functionality to List all users and Delete Users.
        """

        admin_user = AuthManager.get_current_user()
        clear_screen(); print_title('Admin: Manage Users')

        users = self.user_service.get_all_users()
        headers = ['Id','Username','Email','Role','Created At']
        data = [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role,
            'created_at': u.created_at.strftime('%Y-%m-%d')
        } for u in users]
        print_table(data= data, headers= headers)

        print('\nOptions: [D]elete User, [B]ack')
        choice = get_input('> ').lower()

        if choice == 'd':
            user_id_str = get_input('Enter User ID to Delete', lambda i: i if i.isdigit() else None)

            if user_id_str:
                try:
                    if self.user_service.delete_user(int(user_id_str), admin_user):
                        print('User Deleted Successfully.')
                    else:
                        print('User Not Found.')
                except ValueError as e:
                    print(f'Error: {e}')

                input('\nPress Enter to Continue...')





if __name__ == '__main__':

    try:
        print('Initializing Database Connection...')
        DatabaseConnection.initialize_pool()
        app = ExpenseTrackerCLI()
        app.run()

    except Exception as e:
        print(f'\nAn Unexpected Error Occurred: {e}')