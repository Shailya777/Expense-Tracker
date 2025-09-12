from datetime import datetime
from decimal import Decimal
from .base import Transaction

class ExpenseTransaction(Transaction):
    """
    Represents an expense transaction.
    """

    def __init__(self, id: int | None, user_id: int, account_id: int, category_id: int,
                 amount: Decimal, transaction_date: datetime,
                 merchant_id: int | None = None, description: str | None = None):
        super().__init__(id, user_id, account_id, category_id, amount,
                         transaction_date, 'expense', merchant_id, description)

    def get_transaction_type(self):
        return self.transaction_type
        
class IncomeTransaction(Transaction):
    """
    Represents an income transaction.
    """

    def __init__(self, id: int | None, user_id: int, account_id: int, category_id: int,
                 amount: Decimal, transaction_date: datetime,
                 merchant_id: int | None = None, description: str | None = None):
        super().__init__(id, user_id, account_id, category_id, amount,
                         transaction_date, 'income', merchant_id, description)

    def get_transaction_type(self):
        return self.transaction_type