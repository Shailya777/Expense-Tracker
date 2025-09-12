from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    """
    Represents a user of the application.
    Corresponds to the 'users' table in the database.
    """

    username : str
    email : str
    password_hash : str
    role : str = 'user'
    id : int | None = None
    created_at : datetime = field(default_factory= datetime.now)