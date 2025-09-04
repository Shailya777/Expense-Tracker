from expense_tracker.core.config import load_db_config
from expense_tracker.core.db_conn import get_db_connection

def db_conn_test():

    config_details = load_db_config()
    db_conn = get_db_connection(config_details)
    print(f'Connection Successful: {db_conn.is_connected()}')
    db_conn.close()


if __name__ == '__main__':
    db_conn_test()
