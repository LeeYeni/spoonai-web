from src.database.mysql import get_mysql_db
from src.entity.user import User

class UserRepository:
    @staticmethod
    def save(ip_address: str) -> int:
        with get_mysql_db() as db:
            user = UserRepository.get_by_ip_address(db, ip_address)

            if user:
                return user.id
            
            new_user = User(ip_address=ip_address)

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return new_user.id

    @staticmethod
    def get_by_ip_address(db, ip_address: str) -> User:
        return db.query(User).filter(User.ip_address==ip_address).first()