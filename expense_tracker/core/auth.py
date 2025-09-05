import bcrypt
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.core.exceptions import AuthError

class AuthManager:

    # Gets DB CONNECTION Objects from db_conn file:
    def __init__(self, db_config):
        self.conn = get_db_connection(db_config)

    # Takes Password, Turns it into Bytes and Turns it into Hashed Password:
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # New User Registration:
    def register(self):
        email = input('Enter Email: ').strip()
        password = input('Enter Password: ').strip()
        hashed_pass = self.hash_password(password)

        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "insert into users (email, password_hash, role) values (%s, %s, 'user')",
                (email, hashed_pass.decode('utf-8'))
            )
            self.conn.commit()
            print('User Registration Successful')

        except Exception as e:
            self.conn.rollback()
            print(f'Registration Failed: {e}')


    # User Login:
    def login(self):
        email = input('Enter Email: ').strip()
        password = input('Enter Password: ').strip()
        cursor = self.conn.cursor(dictionary= True)
        cursor.execute("select * from users where email = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            raise AuthError('User Not Found.')
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            raise AuthError('Incorrect Password.')

        return user
