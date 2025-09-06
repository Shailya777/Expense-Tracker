from models.base_model import BaseModel

class Account(BaseModel):

    def __init__(self, account_id, user_id, account_name, balance, account_type):
        self.account_id = account_id
        self.user_id = user_id
        self.account_name = account_name
        self.balance = balance
        self.account_type = account_type

    def to_dict(self):
        return {
            'account_id' : self.account_id,
            'user_id' : self.user_id,
            'account_name' : self.account_name,
            'balance' : self.balance,
            'account_type' : self.account_type
        }

class CashAccount(Account):
    def __init__(self, account_id, user_id, account_name, balance):
        super().__init__(account_id, user_id, account_name, balance, account_type= 'cash')

class BankAccount(Account):
    def __init__(self, account_id, user_id, account_name, balance):
        super().__init__(account_id, user_id, account_name, balance, account_type= 'bank')

class CreditCardAccount(Account):
    def __init__(self, account_id, user_id, account_name, balance):
        super().__init__(account_id, user_id, account_name, balance, account_type= 'creditcard')