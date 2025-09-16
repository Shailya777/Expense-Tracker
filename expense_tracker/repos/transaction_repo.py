from typing import List, Optional
from datetime import datetime
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.transaction import Transaction, ExpenseTransaction, IncomeTransaction

class TransactionRepository:
    """
    Handles all database operations related to Transaction models.
    """

    TRANSACTION_TYPE_MAP = {
        'expense' : ExpenseTransaction,
        'income' : IncomeTransaction
    }

    @staticmethod
    def create(transaction: Transaction):
        """
        Creates a new transaction by calling a stored procedure.
        The procedure handles inserting the transaction and updating the account balance.

        :param transaction:  The transaction object to create.
        :return: Transaction: The created transaction object (ID will not be populated by this method).
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                args = (
                    transaction.user_id,
                    transaction.account_id,
                    transaction.category_id,
                    transaction.merchant_id,
                    transaction.amount,
                    transaction.transaction_type,
                    transaction.transaction_date,
                    transaction.description
                )

                cursor.callproc('sp_post_transaction', args)
                conn.commit()

                return transaction


    @staticmethod
    def find_all_by_user(user_id: int) -> List[Transaction]:
        """
        Finds all transactions for a given user, joining with related tables.

        :param user_id: The ID of the user.
        :return: List[Transaction]: A list of all transaction objects for the user.
        """

        transactions= []
        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = """
                    select t.*, c.name as category_name, a.name as account_name, m.name as merchant_name
                    from transactions t
                    join categories c
                    on (t.category_id = c.id)
                    join accounts a
                    on (t.account_id = a.id)
                    join merchants m
                    on (t.merchant_id = m.id)
                    where t.user_id = %s
                    order by t.transaction_date desc
                    """
                cursor.execute(sql, (user_id,))
                rows = cursor.fetchall()

                for row in rows:
                    transaction_class = TransactionRepository.TRANSACTION_TYPE_MAP.get(row['transaction_type'])

                    if transaction_class:
                        trans_obj = transaction_class(
                            id = row['id'],
                            user_id = row['user_id'],
                            account_id= row['account_id'],
                            category_id= row['category_id'],
                            merchant_id= row['merchant_id'],
                            amount= row['amount'],
                            transaction_date= row['transaction_date'],
                            description= row['description']
                        )

                        setattr(trans_obj, 'category_name', row['category_name'])
                        setattr(trans_obj, 'account_name', row['account_name'])
                        setattr(trans_obj, 'merchant_name', row['merchant_name'])
                        transactions.append(trans_obj)



        return transactions


    @staticmethod
    def delete(transaction_id: int, user_id: int):
        """
        Deletes a transaction. The associated trigger will update the account balance.

        :param transaction_id: The ID of the transaction to delete.
        :param user_id: The ID of the user who owns the transaction.

        :return:  bool: True if a row was deleted, False otherwise.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "delete from transactions where id = %s and user_id = %s"
                cursor.execute(sql, (transaction_id, user_id))
                conn.commit()
                return cursor.rowcount > 0


    @staticmethod
    def find_by_id_and_user(transaction_id: int, user_id: int) -> Optional[dict]:
        """
        Finds a single transaction by its ID, ensuring it belongs to the user.

        :param transaction_id:  The ID of the transaction.
        :param user_id: The ID of the user.

        :return: Optional[dict]: A dictionary representing the transaction if found, otherwise None.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary = True) as cursor:
                sql = "select * from transactions where id = %s and user_id = %s"
                cursor.execute(sql, (transaction_id, user_id))
                return cursor.fetchone()


    @staticmethod
    def update(transaction: Transaction) -> bool:
        """
        Updates an existing transaction in the database.

        :param transaction: The transaction object with updated data.

        :return: bool: True if the update was successful, False otherwise.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    update transactions
                    set account_id = %s,
                    category_id = %s,
                    amount = %s,
                    transaction_date = %s,
                    description = %s
                    where id = %s and user_id = %s
                    """

                params = (
                    transaction.account_id,
                    transaction.category_id,
                    transaction.amount,
                    transaction.transaction_date,
                    transaction.description,
                    transaction.id,
                    transaction.user_id
                )

                cursor.execute(sql, params)
                conn.commit()
                return cursor.rowcount > 0