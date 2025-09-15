from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Type
from expense_tracker.models.transaction import Transaction, ExpenseTransaction, IncomeTransaction
from expense_tracker.repos.transaction_repo import TransactionRepository
import pandas as pd

class TransactionService:
    """
    Provides business logic for handling financial transactions.
    """

    TRANSACTION_TYPE_MAP = {
        'expense' : ExpenseTransaction,
        'income' : IncomeTransaction
    }

    @staticmethod
    def add_transaction(
            user_id: int,
            account_id: int,
            category_id: int,
            amount: Decimal,
            transaction_type: str,
            transaction_date: datetime,
            merchant_id: Optional[int] = None,
            description: Optional[str] = None
    ):
        """
        Adds a new income or expense transaction.

        :param user_id: ID of the user performing the transaction.
        :param account_id: ID of the account affected.
        :param category_id: ID of the transaction category.
        :param amount: The transaction amount.
        :param transaction_type: 'income' or 'expense'.
        :param transaction_date: The date and time of the transaction.
        :param merchant_id: ID of the merchant. Defaults to None.
        :param description: A brief description. Defaults to None.

        :raises
            ValueError: If amount is not positive or transaction type is invalid.

        :return: Transaction: The created transaction object.
        """

        if amount <= 0:
            raise ValueError('Transaction Amount Must Be Positive.')

        transaction_class = TransactionService.TRANSACTION_TYPE_MAP.get(transaction_type)

        if not transaction_class:
            raise ValueError(f'Invalid Transaction Type: {transaction_type}')

        transaction = transaction_class(
            id = None,
            user_id = user_id,
            account_id = account_id,
            category_id= category_id,
            amount= amount,
            transaction_date= transaction_date,
            merchant_id= merchant_id,
            description= description
        )

        return TransactionRepository.create(transaction)

    @staticmethod
    def get_user_transaction(user_id: int) -> List[Transaction]:
        """
        Retrieves all transactions for a specific user.

        :param user_id: The ID of the user.

        :return: List[Transaction]: A list of the user's transaction objects.
        """

        return TransactionRepository.find_all_by_user(user_id)

    @staticmethod
    def delete_transaction(transaction_id: int, user_id: int) -> bool:
        """
        Deletes a transaction.
        The balance update is handled by a database trigger.

        :param transaction_id: The ID of the transaction to delete.
        :param user_id: The ID of the user who owns the transaction.

        :return: bool: True if deletion was successful, False otherwise.
        """

        return TransactionRepository.delete(transaction_id, user_id)



    @staticmethod
    def export_transaction_to_csv(user_id: int, file_path: str) -> str:
        """
        Exports a user's transactions to a CSV file.

        :param user_id: The ID of the user.
        :param file_path: The path to save the CSV file to.

        :return: str: A confirmation message with the file path.
        """

        transactions = TransactionRepository.find_all_by_user(user_id)

        if not transactions:
            return 'No Transactions to Export.'

        data = [{
            'date': t.transaction_date.strftime('%Y-%m-%d'),
            'type': t.transaction_type,
            'amount': t.amount,
            'category': getattr(t, 'category_name', 'N/A'),
            'account': getattr(t, 'account_name', 'N/A'),
            'merchant': getattr(t, 'merchant_name', 'N/A'),
            'description': t.description
        }  for t in transactions ]

        df = pd.DataFrame(data)
        df.to_csv(file_path, index= False)
        return f'Successfully Exported {len(df)} Transactions to {file_path}'



    @staticmethod
    def import_transactions_from_csv(user_id: int, file_path: str) -> str:
        """
        Imports transactions from a CSV file.

        :param user_id: The ID of the user.
        :param file_path: The path of the CSV file to import.

        :return: str: A summary of the import process.
        """

        try:
            df = pd.read_csv(file_path)
            required_columns = ['date', 'type', 'amount', 'category', 'account']

            if not all(col in df.columns for col in required_columns):
                raise ValueError(f'CSV Must Contain The Following Columns: {required_columns}')

            # Pre Fetching Users Accounts and Categories:
            from expense_tracker.repos.account_repo import AccountRepository
            from expense_tracker.repos.category_repo import CategoryRepository

            accounts = {acc.name.lower(): acc.id for acc in AccountRepository.find_by_user_id(user_id)}
            categories = {cat.name.lower(): cat.id for cat in CategoryRepository.find_by_user_id(user_id)}

            imported_count = 0

            for index, row in df.iterrows():
                account_id = accounts.get(row['account'].lower())
                category_id = categories.get(row['category'].lower())

                if not account_id or not category_id:
                    print(f'Skipping Row {index + 1}: Could Not Find Account {row['account']} or Category {row['category']}.')
                    continue

                TransactionService.add_transaction(
                    user_id= user_id,
                    account_id= account_id,
                    category_id= category_id,
                    amount= Decimal(row['amount']),
                    transaction_type= row['type'],
                    transaction_date= datetime.strptime(row['date'], '%Y-%m-%d'),
                    description= row.get('description', '')
                )
                imported_count += 1

            return f'Successfully Imported {imported_count} of {len(df)} Transactions.'

        except FileNotFoundError:
            return f'Error: File Not Found at {file_path}.'

        except Exception as e:
            return f'An Error occurred During Import: {e}'