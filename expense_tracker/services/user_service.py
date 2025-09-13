import bcrypt
from typing import Optional
from expense_tracker.models.user import User
from expense_tracker.repos.user_repo import UserRepository

class UserService:
    """
    Provides business logic for user-related operations like registration and login.
    """

    @staticmethod
    def register(username: str, email: str, password: str):
        """
        Registers a new user.

        :param username: The desired username.
        :param email: The user's email address.
        :param password: The user's password in plain-text.

        :raises
            ValueError: If the username or email is already taken.

        :return:  User: The newly created user object.
        """

        if UserRepository.find_by_username(username):
            raise ValueError(f'Username {username} is already taken.')

        if UserRepository.find_by_email(email):
            raise ValueError(f'Email {email} is already registered.')

        # Hashing The Password for Secure Storage:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            username= username,
            email = email,
            password_hash= hashed_password.decode('utf-8')
        )

        return UserRepository.create(user)


    @staticmethod
    def login(email: str, password: str):
        """
        Authenticates a user based on email and password.

        :param email: The user's email.
        :param password: The user's password in plain-text.

        :return: Optional[User]: The authenticated User object if credentials are valid,
                            otherwise None.
        """

        user = UserRepository.find_by_email(email)

        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.password_hash.encode('utf-8')):
            return user
        return None

