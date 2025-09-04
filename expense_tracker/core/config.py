# Gets DataBase Connection details From ENVIRONMENT FILE into Dictionary:

import os

def load_db_config(env_path = None):

    # If no path is provided, Go back up 2 Directories from current file and find .env file in Root Directory:
    if env_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_path = os.path.join(base_dir, '.env')

    db_config = {}

    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()

                if line and not line.startswith('#'):
                    if '=' in line:
                        key, val = line.split('=', 1)
                        db_config[key.strip()] = val.strip()

    else:
        raise FileNotFoundError(f'Database Configuration file {env_path} not found.')

    return db_config