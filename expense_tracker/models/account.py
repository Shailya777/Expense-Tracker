from decimal import Decimal
from .base import Account

class CashAccount(Account):
    """
    Represents a cash account.
    """

    def __init__(self, id: int | None, user_id: int, name: str, balance: Decimal):
        super().__init__(id, user_id, name, balance, account_type= 'CashAccount')

    def get_account_type(self):
        return self.account_type

class BankAccount(Account):
    """
    Represents a bank account.
    """

    def __init__(self, id: int | None, user_id: int, name: str, balance: Decimal):
        super().__init__(id, user_id, name, balance, account_type= 'BankAccount')

    def get_account_type(self):
        return self.account_type

class CreditCardAccount(Account):
    """
    Represents a Credit Card Account.
    """

    def __init__(self, id: int | None, user_id: int, name: str, balance: Decimal):
        super().__init__(id, user_id, name, balance, account_type= 'CreditCardAccount')

    def get_account_type(self):
        return  self.account_type