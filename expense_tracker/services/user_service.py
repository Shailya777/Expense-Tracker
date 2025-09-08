from repos.user_repo import UserRepo
from models.user import User

class UserService:

    def __init__(self, config):
        self.repo = UserRepo(config)

    def view_profile(self, user_id):
        user_data = self.repo.get_by_id(user_id)
        return User(**user_data) if user_data else None

    def list_users(self):
        return self.repo.get_all()

    def delete_user(self, user_id, is_admin):
        if is_admin:
            self.repo.delete(user_id)
            return True
        return False