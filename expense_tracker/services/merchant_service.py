from typing import List
from expense_tracker.models.merchant import Merchant
from expense_tracker.repos.merchant_repo import MerchantRepository

class MerchantService:
    """
    Provides business logic for managing merchants.
    """

    @staticmethod
    def get_user_merchants(user_id: int) -> List[Merchant]:
        """
        Retrieves all merchants for a specific user.

        :param user_id: The ID of the user.

        :return: List[Merchant]: A list of the user's merchant objects.
        """

        return MerchantRepository.find_by_user_id(user_id)

    @staticmethod
    def get_or_create_merchant(user_id: int, name: str) -> Merchant:
        """
        Gets a merchant by name, creating it if it doesn't exist.

        :param user_id: The ID of the user.
        :param name: The name of the merchant.

        :return: Merchant: The found or newly created Merchant object.
        """

        return MerchantRepository.find_or_create(user_id, name)