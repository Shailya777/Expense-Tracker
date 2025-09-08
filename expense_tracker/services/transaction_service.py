from repos.transaction_repo import TransactionRepo
from models.transaction import ExpenseTransaction, IncomeTransaction

class TransactionService:

    def __init__(self, config):
        self.repo = TransactionRepo(config)

    def list_transactions(self, user_id):
        return self.repo.get_by_user(user_id)

    def add_transaction(self, txn_data):
        if txn_data['transaction_type'] == 'expense':
            txn = ExpenseTransaction(**txn_data)
        else:
            txn = IncomeTransaction(**txn_data)

        self.repo.add(txn)