from repos.account_repo import AccountRepo
from models.account import Account

class AccountService:

    def __init__(self, config):
        self.repo = AccountRepo(config)

    def get_accounts(self, user_id):
        accs = self.repo.get_user_accounts(user_id)
        return [Account(**a) for a in accs]

    def create_account(self, user_id, account_name, balance, account_type):
        account = Account(None, user_id, account_name, balance, account_type)
        self.repo.add(account)