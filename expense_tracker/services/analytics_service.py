import pandas as pd
from typing import List
from expense_tracker.models.transaction import Transaction
from expense_tracker.repos.transaction_repo import TransactionRepository

class AnalyticsService:
    """
    Provides services for data analysis and reporting.
    This service acts as a bridge to the main analytics logic.
    """

    @staticmethod
    def get_transactions_as_dataframe(user_id: int) -> pd.DataFrame:
        """
        Fetches all of a user's transactions and converts them into a pandas DataFrame.

        :param user_id: The ID of the user.

        :return: pd.DataFrame: A DataFrame containing transaction data, or an empty
                          DataFrame if no transactions are found.
        """

        transactions: List[Transaction] = TransactionRepository.find_all_by_user(user_id)

        if not transactions:
            return pd.DataFrame()

        # Convert List of Objects to List of Dictionaries for Dataframe Creation:
        data = []

        for t in transactions:
            data.append({
                'id': t.id,
                'amount': t.amount,
                'transaction_type': t.transaction_type,
                'transaction_date': t.transaction_date,
                'description': t.description,
                'account_id': t.account_id,
                'account_name': getattr(t, 'account_name', None),
                'category_id': t.category_id,
                'category_name': getattr(t, 'category_name', None),
                'merchant_id': t.merchant_id,
                'merchant_name': getattr(t, 'merchant_name', None)
            })

        df = pd.DataFrame(data)

        # Ensuring Correct Data Types for Analysis:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['amount'] = pd.to_numeric(df['amount'])

        return df