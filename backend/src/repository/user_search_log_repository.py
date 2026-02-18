from src.entity.user_search_log import UserSearchLog
from src.database.mysql import get_mysql_db

class UserSearchLogRepository:
    @staticmethod
    def save(user_id: int, query: str) -> None:
        with get_mysql_db() as db:
            new_log = UserSearchLog(
                user_id=user_id,
                query=query
            )

            db.add(new_log)
            db.commit()