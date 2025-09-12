from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Budget:
    """
    Represents a budget for a specific category and time period.
    Corresponds to the 'budgets' table.
    """

    user_id : int
    category_id : int
    amount : Decimal
    year : int
    month : int
    id : int | None = None