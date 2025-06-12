from orm_db import SessionLocal
from models_orm import Role, Permission, UserRole, RolePermission
from services.base_service import BaseService

class RoleService(BaseService):
    def __init__(self):
        super().__init__(Role)

    def get_user_roles(self, employee_id):
        session = SessionLocal()
        roles = session.query(Role).join(UserRole, UserRole.role_id == Role.id).filter(UserRole.employee_id == employee_id).all()
        session.close()
        return roles

    def get_role_permissions(self, role_id):
        session = SessionLocal()
        permissions = session.query(Permission).join(RolePermission, RolePermission.permission_id == Permission.id).filter(RolePermission.role_id == role_id).all()
        session.close()
        return permissions

    def get_all_roles(self):
        session = SessionLocal()
        roles = session.query(Role).all()
        session.close()
        return roles

    def assign_role_to_user(self, employee_id, role_id):
        session = SessionLocal()
        user_role = UserRole(employee_id=employee_id, role_id=role_id)
        session.add(user_role)
        session.commit()
        session.close()

    def remove_role_from_user(self, employee_id, role_id):
        session = SessionLocal()
        user_role = session.query(UserRole).filter_by(employee_id=employee_id, role_id=role_id).first()
        if user_role:
            session.delete(user_role)
            session.commit()
        session.close()

    def get_all(self, filters=None):
        session = SessionLocal()
        query = session.query(Role)
        if filters:
            for k, v in filters.items():
                query = query.filter(getattr(Role, k) == v)
        roles = query.all()
        session.close()
        return roles 