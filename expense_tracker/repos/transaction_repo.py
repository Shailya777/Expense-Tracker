from core.db_conn import get_db_connection

class TransactionRepo:

    def __init__(self, db_config):
        self.conn = get_db_connection(db_config)

    def get_by_user(self, user_id):
        cursor = self.conn.cursor(dictionary= True)
        cursor.execute("""
            select t.transaction_id, t.amount, t.transaction_date,
            t.transaction_desc, c.category_name as category,
             m.merchant_name as merchant, a.account_name as account,
             t.transaction_type
             from transactions t
             join categories c on (t.category_id = c.category_id)
             join merchants m on (t.merchant_id = m.merchant_id)
             join accounts a on (t.account_id = a.account_id)
             where a.user_id = %s
             order by t.transaction_date desc""", (user_id,))
        return cursor.fetchall()

    def add(self, txn):
        cursor = self.conn.cursor()
        cursor.callproc("sp_post_transaction",
                        (txn.account_id, txn.category_id, txn.merchant_id,
                         txn.amount, txn.transaction_date, txn.transaction_desc, txn.transaction_type))
        self.conn.commit()

    def delete(self, txn_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            delete from transaction
            where transaction_id = %s""", (txn_id,))
        self.conn.commit()