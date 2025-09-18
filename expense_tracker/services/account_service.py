from typing import List, Optional, Type
from decimal import Decimal
from expense_tracker.models.account import Account, CashAccount, BankAccount, CreditCardAccount
from expense_tracker.repos.account_repo import AccountRepository

class AccountService:
    """
    Provides business logic for managing user financial accounts.
    """

    ACCOUNT_TYPE_MAP = {
        'CashAccount' : CashAccount,
        'BankAccount' : BankAccount,
        'CreditCardAccount' : CreditCardAccount
    }

    @staticmethod
    def create_account(user_id: int, name: str, account_type: str, balance: Decimal = Decimal('0.0')):
        """
        Creates a new financial account for a user.

        :param user_id: The ID of the user owning the account.
        :param name: The name of the account (e.g., "Checking Account").
        :param account_type: The type of account ('CashAccount', 'BankAccount', etc.).
        :param balance: The initial balance. Defaults to 0.0.

        :raises
            ValueError: If the account type is invalid.

        :return: The created account object.
        """

        account_class = AccountService.ACCOUNT_TYPE_MAP.get(account_type)

        if not account_class:
            raise ValueError(f'Invalid Account Type: {account_type}')

        account = account_class(id= None, user_id= user_id, name= name, balance= balance)

        return AccountRepository.create(account)


    @staticmethod
    def get_user_accounts(user_id: int):
        """
        Retrieves all financial accounts for a specific user.

        :param user_id: The ID of the user.

        :return: List[Account]: A list of the user's account objects.
        """

        return AccountRepository.find_by_user_id(user_id)

    @staticmethod
    def delete_account(account_id: int, user_id: int):
        """
        Deletes a user's financial account.

        :param account_id: The ID of the account to delete.
        :param user_id: The ID of the user who owns the account.

        :return: bool: True if deletion was successful, False otherwise.
        """

        return AccountRepository.delete(account_id, user_id)

    @staticmethod
    def update_account_name(account_id: int, user_id: int, new_name: str) -> bool:
        """
        Updates the name of an existing account.

        :param account_id: The ID of the account to update.
        :param user_id: The ID of the user who owns the account.
        :param new_name: The new name for the account.

        :return: bool: True if the update was successful, False otherwise.
        """

        account = AccountRepository.find_by_id_and_user(account_id, user_id)

        if not account:
            return False

        account.name = new_name
        AccountRepository.update(account)
        return True
