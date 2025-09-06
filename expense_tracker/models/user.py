from models.base_model import BaseModel

class User(BaseModel):

    def __init__(self, user_id, email, password_hash, user_role, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.password_has = password_hash
        self.user_role = user_role
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            'user_id' : self.user_id,
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'email' : self.email,
            'user_role' : self.user_role
        }