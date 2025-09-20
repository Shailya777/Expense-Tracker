import bcrypt
from typing import Optional, List
from expense_tracker.models.user import User
from expense_tracker.repos.user_repo import UserRepository
from expense_tracker.services.audit_log_service import AuditLogService

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
            AuditLogService.log('Login_Success', user_id= user.id, details= f'User {user.username} logged in.')
            return user

        user_id = user.id if user else None
        AuditLogService.log('Login_Failure', user_id= user.id, details= f'Failed Login Attempt for Email: {email}')
        return None


    @staticmethod
    def get_all_users() -> List[User]:
        """
        Retrieves a list of all users. (For Admin use)

        :return: A list of all user objects.
        """

        return UserRepository.find_all()

    @staticmethod
    def delete_user(user_id_to_delete: int, admin_user: User) -> bool:
        """
        Deletes a user. (For Admin use)

        :param user_id_to_delete: The ID of the user to be deleted.
        :param admin_user: The admin user performing the action.

        :raises: ValueError: If the admin tries to delete themselves.

        :return: bool: True if deletion was successful.
        """

        if user_id_to_delete == admin_user.id:
            raise ValueError('Admin Users Can Not Delete Their Own Account.')

        AuditLogService.log(
            'Admin_Delete_User',
            user_id= admin_user.id,
            details= f'Admin {admin_user.username} Deleted User with ID {user_id_to_delete}'
        )
        return UserRepository.delete(user_id= user_id_to_delete)

