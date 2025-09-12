from typing import List, Optional
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.account import Account, BankAccount, CashAccount, CreditCardAccount

class AccountRepository:
    """
    Handles all database operations related to Account models.
    """

    ACCOUNT_TYPE_MAP = {
        'CashAccount' : CashAccount,
        'BankAccount' : BankAccount,
        'CreditCardAccount' : CreditCardAccount
    }

    @staticmethod
    def create(account: Account):
        """
        Creates a new account in the database.

        :param account: An Account object (e.g., CashAccount) to be created.
        :return: The created Account object with its new ID.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    insert into accounts (user_id, name, account_type, balance)
                    values (%s, %s, %s, %s)
                    """
                cursor.execute(sql, (account.user_id, account.name, account.account_type, account.balance))
                account.id = cursor.lastrowid
                conn.commit()
                return account

    @staticmethod
    def find_by_user_id(user_id: int):
        """
         Finds all accounts associated with a specific user.
        :param user_id: The ID of the user.
        :return: A list of Account objects.
        """

        accounts = []
        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = "select * from accounts where user_id = %s order by name"
                cursor.execute(sql, (user_id,))
                rows = cursor.fetchall()

                for row in rows:
                    account_class = AccountRepository.ACCOUNT_TYPE_MAP.get(row['account_type'])
                    if account_class:
                        accounts.append(account_class(
                            id = row['id'],
                            user_id = row['user_id'],
                            name = row['name'],
                            balance = row['balance']
                        ))

        return accounts

    @staticmethod
    def find_by_id_and_user(account_id: int, user_id: int):
        """
        Finds a specific account by its ID, ensuring it belongs to the user.

        :param account_id: The ID of the account.
        :param user_id: The ID of the user.
        :return: Optional[Account]: The Account object if found, otherwise None.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary = True) as cursor:
                sql = "select * from accounts where id = %s and user_id = %s"
                cursor.execute(sql, (account_id, user_id))
                row = cursor.fetchone()

                if row:
                    account_class = AccountRepository.ACCOUNT_TYPE_MAP.get(row['account_type'])

                    if account_class:
                        return account_class(
                            id = row['id'],
                            user_id = row['user_id'],
                            name = row['name'],
                            balance = row['balance']
                        )
                return None


    @staticmethod
    def update(account: Account):
        """
        Updates an existing account's details.

        :param account: The account object with updated information.
        :return: None
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    update accounts
                    set name = %s, balance = %s
                    where id = %s
                    and user_id = %s"""
                cursor.execute(sql, (account.name, account.balance, account.id, account.user_id))
                conn.commit()

    @staticmethod
    def delete(account_id: int, user_id: int):
        """
        Deletes an account from the database.

        :param account_id: The ID of the account to delete.
        :param user_id: The ID of the user owning the account.

        :return: bool: True if a row was deleted, False otherwise.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "delete from accounts where id = %s and user_id = %s"
                cursor.execute(sql, (account_id, user_id))
                conn.commit()
                return cursor.rowcount > 0