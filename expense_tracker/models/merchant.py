from dataclasses import dataclass

@dataclass
class Merchant:
    """
    Represents a merchant or vendor.
    Corresponds to the 'merchants' table.
    """

    name : str
    user_id : int | None = None
    id : int | None = None