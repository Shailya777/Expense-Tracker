from repos.budget_repo import BudgetRepo
from models.budget import Budget

class BudgetService:

    def __init__(self, config):
        self.repo = BudgetRepo(config)

    def upsert_budget(self, budget_data):
        budget = Budget(**budget_data)
        self.repo.upsert(budget)

    def get_budgets(self, user_id):
        return self.repo.get_by_user(user_id)