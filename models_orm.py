from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class MainOffice(Base):
    __tablename__ = 'MainOffice'
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    manager_name = Column(String(100), nullable=False)
    workplace_count_for_branch = Column(Integer, nullable=False)
    workplace_count_for_kiosk = Column(Integer, nullable=False)

class Branch(Base):
    __tablename__ = 'Branch'
    id = Column(Integer, primary_key=True)
    office_id = Column(Integer, ForeignKey('MainOffice.id'))
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    office = relationship('MainOffice')

class Kiosk(Base):
    __tablename__ = 'Kiosk'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey('Branch.id'))
    kiosk_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    branch = relationship('Branch')

class Client(Base):
    __tablename__ = 'Client'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    is_profi_client = Column(Boolean, nullable=False)

class DiscountCard(Base):
    __tablename__ = 'DiscountCard'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('Client.id'))
    issue_date = Column(Date, nullable=False)
    discount_rate = Column(Float, nullable=False)
    client = relationship('Client')

class ProfiDiscount(Base):
    __tablename__ = 'ProfiDiscount'
    client_id = Column(Integer, ForeignKey('Client.id'), primary_key=True)
    branch_id = Column(Integer, ForeignKey('Branch.id'), primary_key=True)
    min_orders = Column(Integer, nullable=False)
    discount_rate = Column(Float, nullable=False)
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date, nullable=False)
    client = relationship('Client')
    branch = relationship('Branch')

class Supplier(Base):
    __tablename__ = 'Supplier'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone_number = Column(String(50), nullable=False)

class ProductCategory(Base):
    __tablename__ = 'ProductCategory'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class SupplierSpecialization(Base):
    __tablename__ = 'SupplierSpecialization'
    supplier_id = Column(Integer, ForeignKey('Supplier.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('ProductCategory.id'), primary_key=True)
    supplier = relationship('Supplier')
    category = relationship('ProductCategory')

class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    category_id = Column(Integer, ForeignKey('ProductCategory.id'))
    brand = Column(String(100))
    unit_price = Column(Float, nullable=False)
    category = relationship('ProductCategory')

class Supply(Base):
    __tablename__ = 'Supply'
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('Supplier.id'))
    product_id = Column(Integer, ForeignKey('Product.id'))
    supply_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_cost = Column(Float, nullable=False)
    supplier = relationship('Supplier')
    product = relationship('Product')

class Distribution(Base):
    __tablename__ = 'Distribution'
    id = Column(Integer, primary_key=True)
    supply_id = Column(Integer, ForeignKey('Supply.id'))
    to_branch_id = Column(Integer, ForeignKey('Branch.id'), nullable=True)
    to_kiosk_id = Column(Integer, ForeignKey('Kiosk.id'), nullable=True)
    quantity = Column(Integer, nullable=False)
    dist_date = Column(Date, nullable=False)
    supply = relationship('Supply')
    branch = relationship('Branch')
    kiosk = relationship('Kiosk')

class Order(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('Client.id'))
    branch_id = Column(Integer, ForeignKey('Branch.id'))
    kiosk_id = Column(Integer, ForeignKey('Kiosk.id'), nullable=True)
    order_type = Column(String(10), nullable=False)
    is_urgent = Column(Boolean, nullable=False)
    price = Column(Float, nullable=False)
    total_price = Column(Float)
    order_date = Column(Date, nullable=False)
    client = relationship('Client')
    branch = relationship('Branch')
    kiosk = relationship('Kiosk')

class FilmDevelopment(Base):
    __tablename__ = 'FilmDevelopment'
    order_id = Column(Integer, ForeignKey('Order.id'), primary_key=True)
    num_films = Column(Integer, nullable=False)
    price_per_film = Column(Float, nullable=False)
    order = relationship('Order')

class PhotoPrint(Base):
    __tablename__ = 'PhotoPrint'
    order_id = Column(Integer, ForeignKey('Order.id'), primary_key=True)
    total_photos = Column(Integer, nullable=False)
    format = Column(String(20), nullable=False)
    paper_type = Column(String(50), nullable=False)
    order = relationship('Order')

class PrintDetail(Base):
    __tablename__ = 'PrintDetail'
    order_id = Column(Integer, ForeignKey('Order.id'), primary_key=True)
    frame_number = Column(Integer, primary_key=True)
    copies_count = Column(Integer, nullable=False)
    order = relationship('Order')

class Sale(Base):
    __tablename__ = 'Sale'
    client_id = Column(Integer, ForeignKey('Client.id'), primary_key=True)
    branch_id = Column(Integer, ForeignKey('Branch.id'), primary_key=True, nullable=True)
    kiosk_id = Column(Integer, ForeignKey('Kiosk.id'), primary_key=True, nullable=True)
    product_id = Column(Integer, ForeignKey('Product.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    client = relationship('Client')
    branch = relationship('Branch')
    kiosk = relationship('Kiosk')
    product = relationship('Product')

class ServiceType(Base):
    __tablename__ = 'ServiceType'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)

class ServiceOrder(Base):
    __tablename__ = 'ServiceOrder'
    client_id = Column(Integer, ForeignKey('Client.id'), primary_key=True)
    branch_id = Column(Integer, ForeignKey('Branch.id'), primary_key=True)
    service_code = Column(Integer, ForeignKey('ServiceType.id'), primary_key=True)
    price = Column(Float, nullable=False)
    details = Column(String(255))
    client = relationship('Client')
    branch = relationship('Branch')
    service = relationship('ServiceType')

class Workplace(Base):
    __tablename__ = 'Workplace'
    id = Column(Integer, primary_key=True)
    branch_id = Column(Integer, ForeignKey('Branch.id'), nullable=True)
    kiosk_id = Column(Integer, ForeignKey('Kiosk.id'), nullable=True)
    position = Column(String(50), nullable=False)
    duties = Column(String(255), nullable=False)
    branch = relationship('Branch')
    kiosk = relationship('Kiosk')

class Employee(Base):
    __tablename__ = 'Employee'
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    hire_date = Column(Date, nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    login = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    workplace_id = Column(Integer, ForeignKey('Workplace.id'), nullable=False, unique=True)
    workplace = relationship('Workplace')

class Role(Base):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))

class Permission(Base):
    __tablename__ = 'Permission'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))

class RolePermission(Base):
    __tablename__ = 'RolePermission'
    role_id = Column(Integer, ForeignKey('Role.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('Permission.id'), primary_key=True)
    role = relationship('Role')
    permission = relationship('Permission')

class UserRole(Base):
    __tablename__ = 'UserRole'
    employee_id = Column(Integer, ForeignKey('Employee.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('Role.id'), primary_key=True)
    employee = relationship('Employee')
    role = relationship('Role') 