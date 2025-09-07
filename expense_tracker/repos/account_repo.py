from core.db_conn import get_db_connection

class AccountRepo:

    def __init__(self, db_config):
        self.conn = get_db_connection(db_config)

    def get_user_accounts(self, user_id):
        cursor = self.conn.cursor(dictionary= True)
        cursor.execute("""
            select account_id, account_name, balance,
            account_type
            from accounts
            where user_id = %s""",
                       (user_id,))
        return cursor.fetchall()

    def add(self, account):
        cursor = self.conn.cursor()
        cursor.execute("""
            insert into accounts (user_id, account_name, balance, account_type)
            values (%s, %s, %s, %s)""",
                       (account.user_id, account.account_name, account.balance, account.account_type))
        self.conn.commit()

    def delete(self, account_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            delete from accounts
            where account_id = %s""", (account_id,))
        self.conn.commit()