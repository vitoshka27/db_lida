from orm_db import SessionLocal
from models_orm import Employee, Workplace
import bcrypt

class AuthService:
    def __init__(self):
        pass

    def authenticate(self, login, password):
        session = SessionLocal()
        user = session.query(Employee).filter(Employee.login == login).first()
        if not user or not user.password_hash or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            session.close()
            return None
        # workplace
        workplace = session.query(Workplace).filter(Workplace.id == user.workplace_id).first()
        user_info = {
            'id': user.id,
            'full_name': user.full_name,
            'hire_date': user.hire_date,
            'phone': user.phone,
            'login': user.login,
            'password_hash': user.password_hash,
            'workplace_id': user.workplace_id,
            'branch_id': workplace.branch_id if workplace else None,
            'kiosk_id': workplace.kiosk_id if workplace else None,
            'position': workplace.position if workplace else None
        }
        session.close()
        return user_info 