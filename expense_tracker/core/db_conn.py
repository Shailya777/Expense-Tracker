import mysql.connector
from mysql.connector import Error

# Get Database Connection Details from Configuration file and create Database Connection.

def get_db_connection(db_config):

    try:
        conn = mysql.connector.connect(
            host = db_config.get('DB_HOST'),
            user = db_config.get('DB_USER'),
            password = db_config.get('DB_PASS'),
            database = db_config.get('DB_NAME'),
            auth_plugin = 'mysql_native_password'
        )

        if conn.is_connected():
            return conn
        else:
            raise ConnectionError('Failed to Connect to Database.')

    except Error as e:
        raise ConnectionError(f'Database Connection Error: {e}')