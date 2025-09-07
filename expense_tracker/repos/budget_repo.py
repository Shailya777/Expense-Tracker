from core.db_conn import get_db_connection

class BudgetRepo:

    def __init__(self, db_config):
        self.conn = get_db_connection(db_config)

    def upsert(self, budget):
        cursor = self.conn.cursor()
        cursor.callproc("sp_upsert_budget", (
            budget.user_id, budget.category_id, budget.amount,
            budget.budget_month, budget.budget_year
        ))
        self.conn.commit()

    def get_by_user(self, user_id):
        cursor = self.conn.cursor(dictionary= True)
        cursor.execute("""
            select b.budget_id, b.amount, b.budget_month,
            b.budget_year, c.category_name as category
            from budgets b
            join categories c on (b.category_id = c.category_id)
            where b.user_id = %s""", (user_id, ))
        return cursor.fetchall()