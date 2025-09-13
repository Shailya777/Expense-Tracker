from decimal import Decimal
from typing import List
from expense_tracker.models.budget import Budget
from expense_tracker.repos.budget_repo import BudgetRepository

class BudgetService:
    """
    Provides business logic for managing budgets.
    """

    @staticmethod
    def set_budget(user_id: int, category_id: int, amount: Decimal, year: int, month: int) -> Budget:
        """
        Sets or updates a budget for a specific category and period.

        :param user_id: The ID of the user.
        :param category_id: The ID of the category for the budget.
        :param amount: The budget amount.
        :param year: The budget year.
        :param month: The budget month (1-12).

        :raises
            ValueError: If the amount is not positive.

        :return: Budget: The budget object that was set.
        """

        if amount <= 0:
            raise ValueError('Budget Amount Must Be Positive.')

        budget = Budget(
            user_id= user_id,
            category_id= category_id,
            amount= amount,
            year= year,
            month= month
        )

        return BudgetRepository.upsert(budget)


    @staticmethod
    def get_budgets_for_period(user_id: int, year: int, month: int) -> List[dict]:
        """
        Retrieves budgets for a user for a specific period.

        :param user_id: The user's ID.
        :param year: The year to retrieve budgets for.
        :param month: The month to retrieve budgets for.

        :return: List[dict]: A list of dictionaries with budget and category information.
        """

        return BudgetRepository.find_by_user_and_period(user_id, year, month)


    @staticmethod
    def delete_budget(budget_id: int, user_id: int) -> bool:
        """
        Deletes a specific budget.

        :param budget_id: The ID of the budget to delete.
        :param user_id: The ID of the user who owns the budget.

        :return: bool: True if deletion was successful, False otherwise.
        """

        return BudgetRepository.delete(budget_id, user_id)