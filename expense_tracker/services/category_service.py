from typing import List, Optional
from expense_tracker.models.category import Category
from expense_tracker.repos.category_repo import CategoryRepository
from expense_tracker.core.exceptions import ValidationError

class CategoryService:
    """
    Provides business logic for managing transaction categories.
    """

    @staticmethod
    def create_category(user_id: int, name: str, cat_type: str, parent_id: Optional[int] = None) -> Category:
        """
         Creates a new category for a user.

        :param user_id: The ID of the user.
        :param name: The name of the category.
        :param cat_type: The type of category ('income' or 'expense').
        :param parent_id: The ID of the parent category, if any.

        :return: Category: The created category object.
        """

        if cat_type not in ['income', 'expense']:
            raise ValidationError(f'Invalid Category Type: {cat_type}')

        # Preventing Duplicate Category Names for The Same User:
        existing_categories = CategoryRepository.find_by_user_id(user_id)
        if any(c.name.lower() == name.lower() for c in existing_categories):
            raise ValidationError(f'Category With Name {name} Already Exists.')

        category = Category(user_id= user_id, name= name, type= cat_type, parent_id= parent_id)
        return CategoryRepository.create(category)


    @staticmethod
    def get_user_categories(user_id: int) -> List[Category]:
        """
        Retrieves all categories for a specific user.

        :param user_id: The ID of the user.

        :return: A list of the user's category objects.
        """

        return CategoryRepository.find_by_user_id(user_id)


    @staticmethod
    def delete_category(category_id: int, user_id: int) -> bool:
        """
        Deletes a user's category.

        :param category_id: The ID of the category to delete.
        :param user_id: The ID of the user who owns the category.

        :return: bool: True if deletion was successful, False otherwise.
        """

        return CategoryRepository.delete(category_id, user_id)