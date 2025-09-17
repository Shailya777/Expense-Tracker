from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Category:
    """
    Represents a category for transactions (e.g., 'Groceries', 'Salary').
    Corresponds to the 'categories' table.
    """

    user_id: int
    name : str
    type : str
    id : int | None = None
    parent_id : int | None = None
    created_at: datetime = field(default_factory=datetime.now)