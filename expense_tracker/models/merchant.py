from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Merchant:
    """
    Represents a merchant or vendor.
    Corresponds to the 'merchants' table.
    """

    name : str
    user_id : int | None = None
    id : int | None = None
    created_at : datetime = field(default_factory= datetime.now)