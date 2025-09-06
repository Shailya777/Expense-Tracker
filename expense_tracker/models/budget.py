from models.base_model import BaseModel

class Budget(BaseModel):

    def __init__(self, budget_id, user_id, category_id, amount, budget_month, budget_year):
        self.budget_id = budget_id,
        self.user_id = user_id,
        self.category_id = category_id,
        self.amount = amount,
        self.budget_month = budget_month
        self.budget_year = budget_year

    def to_dict(self):
        return {
            'budget_id' : self.budget_id,
            'user_id' : self.user_id,
            'category_id' : self.category_id,
            'amount' : self.amount,
            'budget_month' : self.budget_month,
            'budget_year' : self.budget_year
        }