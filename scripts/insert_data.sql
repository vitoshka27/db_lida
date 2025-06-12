-- MainOffice
INSERT INTO MainOffice(address,phone,manager_name,workplace_count_for_branch,workplace_count_for_kiosk) VALUES
('ул. Ленина, д.1','+380441111111','Иванов И.И.',10,5),
('пр. Победы, д.5','+380442222222','Петров П.П.',8,4),
('ул. Шевченко, д.10','+380443333333','Сидоров С.С.',12,6),
('бул. Дружбы, д.3','+380444444444','Кузнецов А.А.',9,3),
('ул. Свободы, д.7','+380445555555','Михайлов М.М.',11,5),
('пр. Героев, д.2','+380446666666','Ильина И.И.',7,2),
('ул. Приднепровская, д.15','+380447777777','Андреев А.А.',13,7),
('ул. Бандеры, д.33','+380448888888','Васильев В.В.',10,4);

-- Branch
INSERT INTO Branch(office_id,name,address) VALUES
(1,'Центральный','ул. Ленина, д.3'),
(1,'Восточный','ул. Восточная, д.15'),
(2,'Западный','пр. Победы, д.8'),
(2,'Северный','ул. Северная, д.20'),
(3,'Южный','ул. Южная, д.5'),
(3,'Подольский','ул. Подольская, д.12'),
(4,'Оболонь','пр. Оболонский, д.4'),
(5,'Троещина','ул. Троещинская, д.30');

-- Kiosk
INSERT INTO Kiosk(branch_id,kiosk_name,address) VALUES
(1,'Parkside Photo','ТРЦ Gulliver, 3 этаж'),
(1,'FotoExpress','ТРЦ Arena City, 1 этаж'),
(2,'ColorFrame','ТРЦ Ocean Plaza, 2 этаж'),
(2,'Print&Go','ТРЦ Dream Town, 1 этаж'),
(3,'ФотоМиг','ТРЦ SkyMall, 4 этаж'),
(4,'ZoomPoint','ТРЦ Lavina Mall, 2 этаж'),
(5, 'SnapShot','ТРЦ Respublika, 3 этаж'),
(6,'Фото24','ТРЦ Retroville, 1 этаж');

-- Client
INSERT INTO `Client`(full_name,phone,email,is_profi_client) VALUES
('Иванов И.И.','+380501111111','ivanov@example.com',FALSE),
('Петров П.П.','+380502222222','petrov@example.com',TRUE),
('Сидорова С.С.','+380503333333','sidorova@example.com',FALSE),
('Кузнецов А.А.','+380504444444','kuznetsov@example.com',TRUE),
('Михайлов М.М.','+380505555555','mihailov@example.com',FALSE),
('Ильина И.И.','+380506666666','ilina@example.com',TRUE),
('Андреев А.А.','+380507777777','andreev@example.com',FALSE),
('Васильев В.В.','+380508888888','vasilev@example.com',TRUE);

-- DiscountCard
INSERT INTO DiscountCard(client_id,issue_date,discount_rate) VALUES
(1,'2025-01-10',0.05),
(2,'2025-02-12',0.10),
(3,'2025-03-15',0.03),
(4,'2025-04-01',0.08),
(5,'2025-04-20',0.06),
(6,'2025-05-01',0.12),
(7,'2025-05-05',0.04),
(8,'2025-05-10',0.07);

-- ProfiDiscount
INSERT INTO ProfiDiscount(client_id,branch_id,min_orders,discount_rate,valid_from,valid_to) VALUES
(2,1,5,0.05,'2025-01-01','2025-12-31'),
(2,1,10,0.10,'2025-01-01',NULL),
(4,2,3,0.04,'2025-02-01','2025-10-31'),
(4,2,7,0.08,'2025-02-01',NULL),
(6,3,4,0.06,'2025-03-01','2025-12-31'),
(6,3,8,0.10,'2025-03-01',NULL),
(8,4,2,0.03,'2025-04-01','2025-09-30'),
(8,4,6,0.07,'2025-04-01',NULL);

-- Supplier
INSERT INTO Supplier(name,specialization,phone_number) VALUES
('PhotoSupply Ltd.','бумага, химреактивы','+380441234567'),
('CamMasters','аппараты, объективы','+380445678901'),
('FilmWorld','пленки','+380447890123'),
('AlbumArt','альбомы','+380449012345'),
('PaperPro','бумага','+380441098765'),
('ChemLab','химреактивы','+380442109876'),
('FotoAcc','аксессуары','+380443210987'),
('PrintFast','пленка, бумага','+380444321098');

-- Product
INSERT INTO Product(name,category,brand,unit_price) VALUES
('Kodak Gold','film','Kodak',200.00),
('Fujifilm Superia','film','Fujifilm',180.00),
('Canon EOS 80D','camera','Canon',7000.00),
('Nikon D3500','camera','Nikon',6500.00),
('Фотоальбом Classic','album','Hama',350.00),
('Фотоальбом Modern','album','Brauberg',400.00),
('Чехол для камеры','accessory','CamCase',250.00),
('Фотобумага Glossy','paper','Agfa',60.00);

-- Supply
INSERT INTO Supply(supplier_id,product_id,supply_date,quantity,total_cost) VALUES
(1,1,'2025-03-01',100,20000.00),
(2,2,'2025-03-05',10,50000.00),
(3,3,'2025-04-01',5,35000.00),
(4,4,'2025-04-15',20,7000.00),
(5,5,'2025-05-01',15,5250.00),
(6,6,'2025-05-10',50,3000.00),
(7,7,'2025-05-15',25,6250.00),
(8,8,'2025-05-18',200,12000.00);

-- Distribution
INSERT INTO Distribution(supply_id,to_branch_id,to_kiosk_id,quantity,dist_date) VALUES
(1,1,NULL,50,'2025-03-10'),
(1,NULL,1,50,'2025-03-11'),
(2,2,NULL,10,'2025-03-12'),
(3,3,NULL,5,'2025-04-02'),
(4,NULL,3,20,'2025-04-16'),
(5,5,NULL,15,'2025-05-02'),
(6,NULL,4,50,'2025-05-11'),
(7,6,NULL,25,'2025-05-16');

INSERT INTO `Order` (client_id, branch_id, kiosk_id, order_type, is_urgent, price, total_price, order_date) VALUES
(1, 1, NULL, 'film', FALSE, 100.00, 100.00, '2025-05-01'),
(2, 1, 1, 'print', TRUE, 50.00, 70.00, '2025-05-02'),
(3, 2, 3, 'both', FALSE, 120.00, 120.00, '2025-05-05'),
(4, 2, NULL, 'print', FALSE, 80.00, 80.00, '2025-05-07'),
(5, 3, 5, 'film', TRUE, 110.00, 130.00, '2025-05-08'),
(6, 4, 6, 'both', FALSE, 90.00, 90.00, '2025-05-09'),
(7, 4, NULL, 'print', TRUE, 60.00, 80.00, '2025-05-10'),
(8, 5, 7, 'film', FALSE, 100.00, 100.00, '2025-05-12'),


-- FilmDevelopment
INSERT INTO FilmDevelopment(order_id,num_films,price_per_film) VALUES
(1,3,100.00),
(3,2,120.00),
(5,5,90.00),
(6,4,110.00);

-- PhotoPrint
INSERT INTO PhotoPrint(order_id,total_photos,format,paper_type) VALUES
(1,50,'10x15','glossy'),
(2,150,'10x15','matte'),
(4,80,'13x18','lustre'),
(7,120,'10x15','semi-gloss');

-- PrintDetail
INSERT INTO PrintDetail(order_id,frame_number,copies_count) VALUES
(1,1,10),(1,2,15),
(2,1,50),(2,2,100),
(4,1,30),(4,2,50),
(7,1,60),(7,2,60);

-- Sale
INSERT INTO Sale(client_id,branch_id,kiosk_id,product_id,quantity,unt_price) VALUES
(1,1,NULL,1,2,200.00),
(2,1,1,3,1,7000.00),
(3,2,NULL,2,3,180.00),
(4,2,3,4,5,6500.00),
(5,3,NULL,5,1,350.00),
(6,3,5,6,2,110.00),
(7,4,NULL,7,4,250.00),
(8,5,7,8,10,60.00);

-- ServiceType
INSERT INTO ServiceType(service_code,description) VALUES
(1,'Фото на документы'),
(2,'Реставрация'),
(3,'Прокат аппаратов'),
(4,'Художественное фото'),
(5,'Проф. фотограф'),
(6,'Сканирование'),
(7,'Оформление в рамку'),
(8,'Ретро-фото');

-- ServiceOrder
INSERT INTO ServiceOrder(client_id,branch_id,service_code,price,details) VALUES
(1,1,'1',120.00,'паспорт'),
(2,2,'2',450.00,'старое фото'),
(3,3,'3',600.00,'на выходные'),
(4,4,'4',1500.00,'семейное'),
(5,5,'5',3000.00,'свадебная съемка'),
(6,1,'6',80.00,'слайд'),
(7,2,'7',200.00,'рамка 20x30'),
(8,3,'8',500.00,'старый стиль');
