from services.base_service import BaseService
from models_orm import (
    Employee, Workplace, Branch, Kiosk, Client, DiscountCard, ProfiDiscount, Supplier, ProductCategory, SupplierSpecialization, Product, Supply, Distribution, Order, FilmDevelopment, PhotoPrint, PrintDetail, Sale, ServiceType, ServiceOrder, MainOffice, Role, Permission, RolePermission, UserRole
)
from sqlalchemy.orm import joinedload
from orm_db import SessionLocal

class EmployeeService(BaseService):
    def __init__(self):
        super().__init__(Employee)

    def get_page(self, page=1, page_size=20, filters=None):
        session = SessionLocal()
        query = session.query(self.model_cls)
        query = query.options(joinedload(Employee.workplace).joinedload(Workplace.branch))
        query = query.options(joinedload(Employee.workplace).joinedload(Workplace.kiosk))
        if filters:
            for k, v in filters.items():
                query = query.filter(getattr(self.model_cls, k) == v)
        total = query.count()
        result = query.offset((page-1)*page_size).limit(page_size).all()
        session.close()
        return result, total

class WorkplaceService(BaseService):
    def __init__(self):
        super().__init__(Workplace)

class BranchService(BaseService):
    def __init__(self):
        super().__init__(Branch)

class KioskService(BaseService):
    def __init__(self):
        super().__init__(Kiosk)

class ClientService(BaseService):
    def __init__(self):
        super().__init__(Client)

class DiscountCardService(BaseService):
    def __init__(self):
        super().__init__(DiscountCard)

class ProfiDiscountService(BaseService):
    def __init__(self):
        super().__init__(ProfiDiscount)

class SupplierService(BaseService):
    def __init__(self):
        super().__init__(Supplier)

class ProductCategoryService(BaseService):
    def __init__(self):
        super().__init__(ProductCategory)

class SupplierSpecializationService(BaseService):
    def __init__(self):
        super().__init__(SupplierSpecialization)

class ProductService(BaseService):
    def __init__(self):
        super().__init__(Product)

class SupplyService(BaseService):
    def __init__(self):
        super().__init__(Supply)

class DistributionService(BaseService):
    def __init__(self):
        super().__init__(Distribution)

class OrderService(BaseService):
    def __init__(self):
        super().__init__(Order)

class FilmDevelopmentService(BaseService):
    def __init__(self):
        super().__init__(FilmDevelopment)

class PhotoPrintService(BaseService):
    def __init__(self):
        super().__init__(PhotoPrint)

class PrintDetailService(BaseService):
    def __init__(self):
        super().__init__(PrintDetail)

class SaleService(BaseService):
    def __init__(self):
        super().__init__(Sale)

class ServiceTypeService(BaseService):
    def __init__(self):
        super().__init__(ServiceType)

class ServiceOrderService(BaseService):
    def __init__(self):
        super().__init__(ServiceOrder)

class MainOfficeService(BaseService):
    def __init__(self):
        super().__init__(MainOffice) 

class RoleService(BaseService):
    def __init__(self):
        super().__init__(Role)

class PermissionService(BaseService):
    def __init__(self):
        super().__init__(Permission)

class RolePermissionService(BaseService):
    def __init__(self):
        super().__init__(RolePermission)

class UserRoleService(BaseService):
    def __init__(self):
        super().__init__(UserRole)