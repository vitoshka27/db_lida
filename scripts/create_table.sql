CREATE TABLE MainOffice (
  id INT AUTO_INCREMENT PRIMARY KEY,
  address VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  manager_name VARCHAR(100),
  workplace_count_for_branch INT NOT NULL,
  workplace_count_for_kiosk INT NOT NULL
);

CREATE TABLE Branch (
  id INT AUTO_INCREMENT PRIMARY KEY,
  office_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  address VARCHAR(255) NOT NULL,
  FOREIGN KEY (office_id) REFERENCES MainOffice(id)
);

CREATE TABLE Kiosk (
  id INT AUTO_INCREMENT PRIMARY KEY,
  branch_id INT NOT NULL,
  kiosk_name VARCHAR(100),
  address VARCHAR(255) NOT NULL,
  FOREIGN KEY (branch_id) REFERENCES Branch(id)
);

CREATE TABLE `Client` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name VARCHAR(30) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(100) NOT NULL,
  unique(phone),
  unique(email),
  is_profi_client BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE DiscountCard (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  issue_date DATE NOT NULL,
  discount_rate DECIMAL(4,2) NOT NULL DEFAULT 0.00,
  CONSTRAINT uq_Client UNIQUE(client_id),
  FOREIGN KEY (client_id) REFERENCES Client(id)
);

CREATE TABLE ProfiDiscount (
  client_id INT NOT NULL,
  branch_id INT NOT NULL,
  min_orders INT NOT NULL,
  discount_rate DECIMAL(4,2) NOT NULL,
  valid_from DATE NOT NULL,
  valid_to DATE,
  CHECK (valid_to >= valid_from),
  PRIMARY KEY (client_id, branch_id),
  FOREIGN KEY (client_id) REFERENCES Client(id),
  FOREIGN KEY (branch_id) REFERENCES Branch(id)
);

CREATE TABLE Supplier (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  phone_number VARCHAR(20) NOT NULL
);

CREATE TABLE ProductCategory (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE SupplierSpecialization (
  supplier_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (supplier_id, category_id),
  CONSTRAINT fk_SuppSpec_supplier
    FOREIGN KEY (supplier_id) REFERENCES Supplier(id),
  CONSTRAINT fk_SuppSpec_category
    FOREIGN KEY (category_id) REFERENCES ProductCategory(id)
);


CREATE TABLE Product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  category_id INT NOT NULL,
  brand VARCHAR(100),
  unit_price DECIMAL(10,2) NOT NULL,
  CONSTRAINT fk_Product_category FOREIGN KEY (category_id) REFERENCES ProductCategory(id)
);

CREATE TABLE Supply (
  id INT AUTO_INCREMENT PRIMARY KEY,
  supplier_id INT NOT NULL,
  product_id INT NOT NULL,
  supply_date DATE NOT NULL,
  quantity INT NOT NULL,
  total_cost DECIMAL(12,2) NOT NULL,
  FOREIGN KEY (supplier_id) REFERENCES Supplier(id),
  FOREIGN KEY (product_id) REFERENCES Product(id)
);

CREATE TABLE Distribution (
  id INT AUTO_INCREMENT PRIMARY KEY,
  supply_id INT NOT NULL,
  to_branch_id INT,
  to_kiosk_id INT,
  quantity INT NOT NULL,
  dist_date DATE NOT NULL,
  FOREIGN KEY (supply_id) REFERENCES Supply(id),
  FOREIGN KEY (to_branch_id) REFERENCES Branch(id),
  FOREIGN KEY (to_kiosk_id) REFERENCES Kiosk(id),
  CHECK (
  (to_branch_id IS NOT NULL AND to_kiosk_id IS NULL) OR
  (to_branch_id IS NULL AND to_kiosk_id IS NOT NULL)
)
);

CREATE TABLE `Order` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  branch_id INT NOT NULL,
  kiosk_id INT,
  order_type ENUM('film','print','both') NOT NULL DEFAULT 'both',
  is_urgent BOOLEAN NOT NULL DEFAULT FALSE,
  price DECIMAL(12,2) NOT NULL,
  total_price DECIMAL(12,2),
  order_date DATE NOT NULL,
  FOREIGN KEY (client_id) REFERENCES Client(id),
  FOREIGN KEY (branch_id) REFERENCES Branch(id),
  FOREIGN KEY (kiosk_id) REFERENCES Kiosk(id)
);

CREATE TABLE FilmDevelopment (
  order_id INT PRIMARY KEY,
  num_films INT NOT NULL DEFAULT 1,
  price_per_film DECIMAL(8,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES `Order`(id)
);

CREATE TABLE PhotoPrint (
  order_id INT PRIMARY KEY,
  total_photos INT NOT NULL,
  format VARCHAR(50) NOT NULL,
  paper_type VARCHAR(50) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES `Order`(id)
);



CREATE TABLE PrintDetail (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  frame_number INT NOT NULL,
  copies_count INT NOT NULL DEFAULT 1,
  FOREIGN KEY (order_id) REFERENCES PhotoPrint(order_id)
);

CREATE TABLE Sale (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sale_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  client_id INT NOT NULL,
  branch_id INT,
  kiosk_id INT,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  FOREIGN KEY (client_id) REFERENCES Client(id),
  FOREIGN KEY (branch_id) REFERENCES Branch(id),
  FOREIGN KEY (kiosk_id) REFERENCES Kiosk(id),
  FOREIGN KEY (product_id) REFERENCES Product(id),
  CHECK (
    (branch_id IS NOT NULL AND kiosk_id IS NULL)
    OR (branch_id IS NULL AND kiosk_id IS NOT NULL)
  )
);

CREATE TABLE ServiceType (
  id INT AUTO_INCREMENT PRIMARY KEY,
  description VARCHAR(100) NOT NULL
);

CREATE TABLE ServiceOrder (
  id INT AUTO_INCREMENT PRIMARY KEY,
  client_id INT NOT NULL,
  branch_id INT NOT NULL,
  service_code INT NOT NULL,
  order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  price DECIMAL(10,2) NOT NULL,
  details TEXT DEFAULT NULL,
  FOREIGN KEY (client_id) REFERENCES Client(id),
  FOREIGN KEY (branch_id) REFERENCES Branch(id),
  FOREIGN KEY (service_code) REFERENCES ServiceType(id)
);

CREATE TABLE Workplace (
  id INT AUTO_INCREMENT PRIMARY KEY,
  branch_id INT NULL,
  kiosk_id  INT NULL,
  position VARCHAR(50) NOT NULL,
  duties   VARCHAR(255) NOT NULL,
  FOREIGN KEY (branch_id) REFERENCES Branch(id),
  FOREIGN KEY (kiosk_id)  REFERENCES Kiosk(id),
  CHECK (
  (branch_id IS NOT NULL AND kiosk_id IS NULL) OR
  (branch_id IS NULL AND kiosk_id IS NOT NULL))  
);

CREATE TABLE Employee (
  id INT AUTO_INCREMENT PRIMARY KEY,
  full_name     VARCHAR(150) NOT NULL,
  hire_date     DATE          NOT NULL,
  phone         VARCHAR(20) NOT NULL,
  login         VARCHAR(100)  NOT NULL,
  password_hash VARCHAR(255)  NOT NULL,
  workplace_id  INT           NOT NULL,
  UNIQUE(login),
  UNIQUE(workplace_id),
  UNIQUE(phone),
  FOREIGN KEY (workplace_id) REFERENCES Workplace(id)
);

-- Таблица ролей
CREATE TABLE Role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- Таблица прав 
CREATE TABLE Permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- Таблица связей ролей и прав 
CREATE TABLE RolePermission (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Role(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permission(id) ON DELETE CASCADE
);

-- Таблица связей пользователей и ролей 
CREATE TABLE UserRole (
    employee_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (employee_id, role_id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Role(id) ON DELETE CASCADE
);
