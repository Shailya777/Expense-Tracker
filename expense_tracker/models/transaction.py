from models.base_model import BaseModel

class Transaction(BaseModel):

    def __init__(self, transaction_id, account_id, category_id, merchant_id, amount, transaction_date, transaction_desc , transaction_type):
        self.transaction_id = transaction_id,
        self.account_id = account_id
        self.category_id = category_id,
        self.merchant_id = merchant_id,
        self.amount = amount,
        self.transaction_date = transaction_date,
        self.transactions_desc = transaction_desc,
        self.transaction_type = transaction_type
        
    def to_dict(self):
        return {
        'transaction_id' : self.transaction_id,
        'account_id' : self.account_id,
        'category_id' : self.category_id,
        'merchant_id' : self.merchant_id,
        'amount' : self.amount,
        'transaction_date' : self.transaction_date,
        'transactions_desc' : self.transactions_desc,
        'transaction_type' : self.transaction_type
        }

class ExpenseTransaction(Transaction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, transaction_type= 'expense', **kwargs)
        
class IncomeTransaction(Transaction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, transaction_type= 'income', **kwargs)