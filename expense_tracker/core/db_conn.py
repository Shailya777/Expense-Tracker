import mysql.connector
from mysql.connector import pooling
from .config import settings

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
            return cls._pool.get_connection()
        except mysql.connector.Error as err:
            print(f'Error Getting Connection From Pool: {err}')
            raise


def get_db_connection():
    """
    Provides a global access point to a database connection.
    :return: DatabaseConnection Object.
    """
    return DatabaseConnection.get_connection()