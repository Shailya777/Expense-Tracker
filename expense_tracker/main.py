# ==================================================== Imports ====================================================#

import sys
from datetime import datetime
from decimal import Decimal

# Importing Services:
from services.user_service import UserService
from services.account_service import AccountService
from services.transaction_service import TransactionService
from services.budget_service import BudgetService
from services.category_service import CategoryService
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
        self.analytics_service = AnalyticsService()


    def run(self):

        while True:
            if not AuthManager.is_authenticated():
                self._startup_menu()
            else:
                self._main_menu()


    def _startup_menu(self):

        clear_screen()
        print_title('Welcome to Expense Tracker!!')
        print('1. Register')
        print('2. Login')
        print('3. Exit')

        choice = get_input('> ', error_message= 'Please Enter a Number.')

        if choice == '1': self._handle_registration()
        elif choice == '2': self._handle_login()
        elif choice == '3':
            print('Goodbye! Have a Nice Day!!')
            sys.exit(0)


    def _main_menu(self):

        user = AuthManager.get_current_user()
        clear_screen()
        print_title(f'Main Menu (Logged in as: {user.username})')
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


    def _handle_registration(self):

        clear_screen()
        print_title('Register New User')

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

        clear_screen()
        print_title('User Login')

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


    def _manage_accounts(self):
        user = AuthManager.get_current_user()
        clear_screen(); print_title('Manage Accounts')

        accounts = self.account_service.get_user_accounts(user.id)
        headers = ['ID','Name','Type','Balance']
        data = [{'id': acc.id,
                 'name': acc.name,
                 'type': acc.account_type,
                 'balance': f"{acc.balance:.2f}"}
                for acc in accounts]
        print_table(data= data, headers= headers)
        input('\nPress Enter to Continue...')


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
            name = get_input('Category Name', validate_not_empty)
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


    def _manage_transactions(self):
        pass

    def _manage_budgets(self):
        pass

    def _run_expense_analysis(self):
        pass

    def _handle_csv_operations(self):
        pass

    def _admin_manage_users(self):
        pass


if __name__ == '__main__':

    try:
        print('Initializing Database Connection...')
        DatabaseConnection.initialize_pool()
        app = ExpenseTrackerCLI()
        app.run()

    except Exception as e:
        print(f'\nAn Unexpected Error Occurred: {e}')