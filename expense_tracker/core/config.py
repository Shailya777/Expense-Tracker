# Gets DataBase Connection details From ENVIRONMENT FILE into Dictionary:

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """
    Handles application configuration by loading settings from environment variables.
    """

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')

    @staticmethod
    def get_db_config():
        """
        Returns the database configuration as a dictionary.

        :return: DB configuration
        """

        config = {
            'host' : Config.DB_HOST,
            'port' : Config.DB_PORT,
            'user' : Config.DB_USER,
            'password' : Config.DB_PASSWORD,
            'database' : Config.DB_NAME,
        }

        if not all(config.values()):
            raise ValueError('One or More Database Environment Variables are Not Set.')

        return config


# Instantiating The Configuration To Be Imported By Other Modules
settings = Config()