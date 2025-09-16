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
        new_amount_str = get_input(f'Amount (Current: {trans.amount})')
        new_desc = get_input(f'Description (Current: {trans.description})')

        new_data = {
            'amount': validate_amount(new_amount_str) or trans.amount,
            'description': new_desc or trans.description
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