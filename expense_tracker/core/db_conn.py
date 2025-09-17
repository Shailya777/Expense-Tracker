import mysql.connector
from mysql.connector import pooling
from core.config import settings
from mysql.connector.pooling import PooledMySQLConnection

class CursorContext:
    """
    Context manager wrapper for MySQL cursors.
    Ensures cursor is closed automatically when leaving a 'with' block.
    """

    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.cursor.close()
        except Exception as e:
            print(f'Error: {e}')

class ConnectionContext:
    """
    Context manager wrapper for PooledMySQLConnection.
    Allows usage like:

        with DatabaseConnection.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users")

    Automatically closes the connection when the context ends.
    """

    def __init__(self, conn: PooledMySQLConnection):
        self.conn = conn

    def __enter__(self):
        return self # Return Wrapper, Not The Raw Connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn.is_connected():
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
                self.conn.close()
        except Exception as e:
            print(f'Error: {e}')

    def cursor(self, *args, **kwargs):
        """
        Wrap the real cursor in a context manager.
        """
        return CursorContext(self.conn.cursor(*args, **kwargs))

    # Proxy other attributes/methods to the real connection
    def __getattr__(self, item):
        return getattr(self.conn, item)

class DatabaseConnection:
    """
    Manages the database connection pool for the application.
    """

    _pool = None

    @classmethod
    def initialize_pool(cls):
        """
        Initializes the MySQL connection pool.
        """

        if cls._pool is None:
            try:
                db_config = settings.get_db_config()

                db_config['auth_plugin'] = 'mysql_native_password'

                cls._pool = pooling.MySQLConnectionPool(
                        pool_name= 'expense_tracker_pool',
                        pool_size= 5,
                        **db_config
                )
                print('Database Connection Pool Initialized Successfully.')

            except mysql.connector.Error as err:
                print(f'Error Initializing Database Pool: {err}')
                raise

    @classmethod
    def get_connection(cls):
        """
        Retrieves a connection from the pool.
        """
        if cls._pool is None:
            cls.initialize_pool()

        try:
            conn = cls._pool.get_connection()
            return ConnectionContext(conn)
        except mysql.connector.Error as err:
            print(f'Error Getting Connection From Pool: {err}')
            raise


def get_db_connection():
    """
    Provides a global access point to a database connection.
    :return: DatabaseConnection Object.
    """
    return DatabaseConnection.get_connection()