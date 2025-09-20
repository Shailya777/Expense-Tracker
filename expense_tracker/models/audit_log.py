from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AuditLog:
    """
    Represents an entry in the audit log.
    Corresponds to the 'audit_log' table.
    """

    action : str
    user_id : Optional[int] = None
    details : Optional[str] = None
    id: Optional[int] = None
    timestamp : Optional[datetime] = None