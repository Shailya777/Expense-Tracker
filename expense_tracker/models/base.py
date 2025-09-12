from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal

class BaseModel(ABC):
    """An abstract base class for all model objects."""

    def __init__(self, id: int | None = None):
        self.id = id

class Account(BaseModel, ABC):
    """
    Abstract base class for all account types.
    Represents a source of funds, like a bank account or cash.
    """
    def __init__(self, id: int | None, user_id: int, name: str, balance: Decimal, account_type: str):
        super().__init__(id)
        self.user_id = user_id
        self.name = name
        self.balance = balance
        self.account_type = account_type

    @abstractmethod
    def get_account_type(self):
        """
        Returns the specific type of the account.
        """
        pass

class Transaction(BaseModel, ABC):
    """
    Abstract base class for all transaction types.
    Represents a single financial event, either an expense or income.
    """
    def __init__(self, id: int | None, user_id: int, account_id: int, category_id: int,
                 amount: Decimal, transaction_date: datetime, transaction_type: str,
                 merchant_id: int | None, description: str | None = None):
        super().__init__(id)
        self.user_id = user_id
        self.account_id = account_id
        self.category_id = category_id
        self.merchant_id = merchant_id
        self.amount = amount
        self.transaction_date = transaction_date
        self.transaction_type = transaction_type
        self.description = description

    @abstractmethod
    def get_transaction_type(self):
        """
        Returns the specific type of the transaction.
        """
        pass