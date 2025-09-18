from typing import List, Optional
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.merchant import Merchant

class MerchantRepository:
    """
     Handles all database operations related to the Merchant model.
    """

    @staticmethod
    def find_by_user_id(user_id: int) -> List[Merchant]:
        """
        Finds all merchants associated with a specific user.

        :param user_id: user_id (int): The ID of the user.

        :return: List[Merchant]: A list of Merchant objects.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary = True) as cursor:
                sql = "select * from merchants where user_id = %s order by name"
                cursor.execute(sql, (user_id,))
                rows = cursor.fetchall()
                return [Merchant(**row) for row in rows]


    @staticmethod
    def find_or_create(user_id: int, name: str) -> Merchant:
        """
        Finds a merchant by name for a user, or creates it if it doesn't exist.
        This prevents creating duplicate merchants.

        :param user_id: The ID of the user.
        :param name: The name of the merchant.

        :return: Merchant: The existing or newly created Merchant object.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                # Trying to find The Merchant:
                sql_find = "select * from merchants where user_id = %s and name = %s"
                cursor.execute(sql_find, (user_id, name))
                row = cursor.fetchone()
                if row:
                    return Merchant(**row)

                # If Not Found, Create it:
                sql_create = "insert into merchants (user_id, name) values (%s, %s)"
                cursor.execute(sql_create, (user_id, name))
                new_id = cursor.lastrowid
                conn.commit()
                return Merchant(id = new_id, user_id= user_id, name= name)