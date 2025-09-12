from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.user import User

class UserRepository:
    """
    Handles all database operations related to the User model.
    """

    @staticmethod
    def create(user: User):
        """
        Creates a new user in the database.

        :param user: A User object with username, email, and password_hash.
        :return: User: The created User object with the new database ID.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    insert into users (username, email, password_hash, role)
                    values (%s, %s, %s, %s)
                    """
                cursor.execute(sql, (user.username, user.email, user.password_hash, user.role))
                user.id = cursor.lastrowid
                conn.commit()
                return user

    @staticmethod
    def find_by_email(email: str):
        """
        Finds a user by their email address.

        :param email: The email address to search for.
        :return: Optional[User]: A User object if found, otherwise None.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictonary = True) as cursor:
                sql = "select * from users where email = %s"
                cursor.execute(sql, (email,))
                row = cursor.fetchone()
                if row:
                    return User(**row)
                return None

    @staticmethod
    def find_by_username(username: str):
        """
        Finds a user by their username.

        :param username: The username to search for.
        :return: Optional[User]: A User object if found, otherwise None.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = "select * from users where username= %s"
                cursor.execute(sql, (username,))
                row = cursor.fetchone()
                if row:
                    return User(**row)
                return None

    @staticmethod
    def find_by_id(user_id: int):
        """
        Finds a user by their unique ID.

        :param user_id: The ID of the user.
        :return: Optional[User]: A User object if found, otherwise None.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = "select * from users where id = %s"
                cursor.execute(sql, (user_id,))
                row = cursor.fetchone()
                if row:
                    return User(**row)
                return None