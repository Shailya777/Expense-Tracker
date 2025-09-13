from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Type
from expense_tracker.models.transaction import Transaction, ExpenseTransaction, IncomeTransaction
from expense_tracker.repos.transaction_repo import TransactionRepository

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