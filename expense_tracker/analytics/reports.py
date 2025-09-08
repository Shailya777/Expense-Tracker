import pandas as pd
from repos.transaction_repo import TransactionRepo
from repos.budget_repo import BudgetRepo

class ReportGenerator:

    def __init__(self, config):
        self.transaction_repo = TransactionRepo(config)
        self.budget_repo = BudgetRepo(config)

    def monthly_expense_trend(self, user_id):
        txns = self.transaction_repo.get_by_user(user_id)
        df = pd.DataFrame(txns)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        monthly = df[df['transaction_type'] == 'expense'].groupby(df['transaction_date'].dt.month)['amount'].sum()
        return monthly

    def category_breakdown(self, user_id, month = None):
        txns = self.transaction_repo.get_by_user(user_id)
        df = pd.DataFrame(txns)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        expense_df = df[df['transaction_type'] == 'expense']

        if month:
            expense_df = expense_df[expense_df['transaction_date'].dt.month == month]

        breakdown = expense_df.groupby('category')['amount'].sum()
        return breakdown

    def budget_vs_actual(self, user_id, month):
        budgets = self.budget_repo.get_by_user(user_id)
        txns = self.transaction_repo.get_by_user(user_id)

        txn_df = pd.DataFrame(txns)
        txn_df['transaction_date'] = pd.to_datetime(txn_df['transaction_date'])

        actual = txn_df[(txn_df['transaction_date'].dt.month == month) & (txn_df['transaction_type'] == 'expense')].groupby('category')['amount'].sum()

        budget_df = pd.DataFrame(budgets)
        budget_df = budget_df[budget_df['month'] == month]

        result = pd.merge(budget_df, actual, left_on= 'category', right_index= True, how= "left")
        result['amount_actual'] = result['amount_y'].fillna(0)

        return result[['category, amount_x', 'amount_actual']].rename(columns = {'amount_x' : 'budget'})