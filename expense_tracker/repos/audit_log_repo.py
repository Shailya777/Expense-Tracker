from typing import List
from expense_tracker.core.db_conn import get_db_connection
from expense_tracker.models.audit_log import AuditLog

class AuditLogRepository:
    """
    Handles all database operations for the AuditLog model.
    """

    @staticmethod
    def create(log: AuditLog) -> None:
        """
        Creates a new audit log entry in the database.

        :param log: log (AuditLog): The AuditLog object to be created.
        """

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                sql = """
                    insert into audit_log (user_id, action, details)
                    values (%s, %s, %s)
                    """
                cursor.execute(sql, (log.user_id, log.action, log.details))
                conn.commit()


    @staticmethod
    def find_all() -> List[dict]:
        """
        Retrieves all audit logs, joining with the users table to get usernames.

        :return: List[dict]: A list of dictionaries representing the log entries.
        """

        with get_db_connection() as conn:
            with conn.cursor(dictionary = True) as cursor:
                sql = """
                    select a.id, a.timestamp, a.action, a.details, u,username
                    from audit_log a
                    left join users u
                    on (a.user_id = u.id)
                    order by a.timestamp desc
                    """

                cursor.execute(sql)
                return cursor.fetchall()
