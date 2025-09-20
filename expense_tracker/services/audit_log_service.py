from typing import List, Optional
from expense_tracker.models.audit_log import AuditLog
from expense_tracker.repos.audit_log_repo import AuditLogRepository

class AuditLogService:
    """
    Provides a centralized service for logging and retrieving audit trail events.
    """

    @staticmethod
    def log(action: str, user_id: Optional[int] = None, details: Optional[str] = None):
        """
        Logs a specific user or system action.

        :param action: A short description of the action (e.g., "USER_LOGIN_SUCCESS").
        :param user_id: The ID of the user performing the action.
        :param details: Any additional details about the event.
        """

        log_entry = AuditLog(action= action, user_id= user_id, details= details)
        AuditLogRepository.create(log= log_entry)


    @staticmethod
    def get_all_logs() -> List[dict]:
        """
        Retrieves all audit logs for admin viewing.

        :return: List[dict]: A list of all log entries.
        """

        return AuditLogRepository.find_all()