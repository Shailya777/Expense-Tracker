from core.db_conn import get_db_connection

class UserRepo:

    def __init__(self, db_config):
        self.conn = get_db_connection(db_config)

    def get_by_id(self, user_id):
        cursor = self.conn.cursor(dictionary= True)
        cursor.execute("select user_id, first_name, last_name, email, role from users where user_id = %s", (user_id, ))
        return cursor.fetchone()

    def get_all(self):
        cursor = self.conn.cursor(dictionary= True)
        cursor.execute("select user_id, first_name, last_name, email, role from users")
        return cursor.fetchall()

    def delete(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("delete from users where user_id = %s", (user_id, ))
        self.conn.commit()