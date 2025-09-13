from typing import List
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.budget import Budget

class BudgetRepository:
    """
    Handles all database operations for the Budget model.
    """

    @staticmethod
    def upsert(budget: Budget):
        """
         Inserts a new budget or updates an existing one using a stored procedure.

        :param budget:  The budget object to create or update.
        :return:  The budget object.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                args = (budget.user_id, budget.category_id, budget.amount, budget.year, budget.month)
                cursor.callproc('sp_upsert_budget', args)
                conn.commit()
                return budget


    @staticmethod
    def find_by_user_and_period(user_id: int, year: int, month: int) -> List[dict]:
        """
        Finds all budgets for a user for a specific period, joining with categories.

        :param user_id: The user's ID.
        :param year: The year of the budget period.
        :param month: The month of the budget period.

        :return: List[dict]: A list of dictionaries, each containing budget and category info.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = """
                    select b.id, b.amount, b.month, b.year, 
                    c.name as category_name, c.type as category_type
                    from budgets b
                    join categories c
                    on (b.category_id = c.id)
                    where b.user_id = %s and b.year = %s and b.month = %s
                    order by c.name
                    """
                cursor.execute(sql, (user_id, year, month))
                return cursor.fetchall()


    @staticmethod
    def delete(budget_id: int, user_id: int):
        """
        Deletes a budget from the database.

        :param budget_id: The ID of the budget to delete.
        :param user_id: The ID of the user who owns the budget.

        :return: bool: True if a row was deleted, False otherwise.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "delete from budgets where id = %s and user_id = %s"
                cursor.execute(sql, (budget_id, user_id))
                conn.commit()
                return cursor.rowcount > 0