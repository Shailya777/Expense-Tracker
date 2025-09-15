from typing import List, Optional
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.category import Category

class CategoryRepository:
    """
    Handles all database operations related to the Category model.
    """

    @staticmethod
    def create(category: Category) -> Category:
        """
        Creates a new category in the database.

        :param category: A Category object to be created.

        :return: The created Category object with the new database ID.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    insert into categories (user_id, name, type, parent_id)
                    values (%s, %s, %s, %s)
                    """
                cursor.execute(sql, (category.user_id, category.name, category.type, category.parent_id))
                category.id = cursor.lastrowid
                conn.commit()
                return category


    @staticmethod
    def find_by_user_id(user_id: int) -> List[Category]:
        """
        Finds all categories associated with a specific user.

        :param user_id: The ID of the user.

        :return: List[Category]: A list of Category objects.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = "select * from categories where user_id = %s order by name"
                cursor.execute(sql, (user_id,))
                rows = cursor.fetchall()
                return [Category(**row) for row in rows]



    @staticmethod
    def find_by_id_and_user(category_id: int, user_id: int) -> Optional[Category]:
        """
        Finds a specific category by its ID, ensuring it belongs to the user.

        :param category_id: The ID of the category.
        :param user_id: The ID of the user.

        :return: Optional[Category]: The Category object if found, otherwise None.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary= True) as cursor:
                sql = "select * from categories where id = %s and user_id = %s"
                cursor.execute(sql, (category_id, user_id))
                row = cursor.fetchone()
                return Category(**row) if row else None



    @staticmethod
    def delete(category_id: int, user_id: int) -> bool:
        """
        Deletes a category from the database.

        :param category_id: The ID of the category to delete.
        :param user_id: The ID of the user owning the category.

        :return: bool: True if a row was deleted, False otherwise.
        """
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = "delete from categories where id = %s and user_id = %s"
                cursor.execute(sql, (category_id, user_id))
                conn.commit()
                return cursor.rowcount > 0