from typing import Optional
from expense_tracker.models.user import User

class AuthManager:
    """
    Manages the authentication state of the application.

    This class uses static methods and a class-level attribute to hold the
    state of the currently logged-in user, making it globally accessible
    after login.
    """

    _current_user :Optional[User] = None

    @staticmethod
    def login(user: User) -> None:
        """
        Logs a user in by setting the current user session.

        :param user:  The user object of the successfully authenticated user.

        """

        AuthManager._current_user = user


    @staticmethod
    def logout() -> None:
        """
        Logs the current user out by clearing the session.
        """

        AuthManager._current_user = None


    @staticmethod
    def get_current_user() -> Optional[User]:
        """
        Retrieves the currently logged-in user.

        :return: The User object if a user is logged in, otherwise None.
        """

        return AuthManager._current_user


    @staticmethod
    def is_authenticated() -> bool:
        """
        Checks if there is a user currently logged in.

        :return: bool: True if a user is logged in, False otherwise.
        """

        return AuthManager._current_user is not None


    @staticmethod
    def is_admin() -> bool:
        """
        Checks if the currently logged-in user is an administrator.

        :return: bool: True if the current user has the 'admin' role, False otherwise.
        """

        user = AuthManager.get_current_user()
        return user is not None and user.role == 'admin'