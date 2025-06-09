-- MainOffice
INSERT INTO MainOffice(address,phone,manager_name,workplace_count_for_branch,workplace_count_for_kiosk) VALUES
('ул. Ленина, д.1','+7(962)21-4910','Щербаков Л.И.', 3, 1);

-- Branch
INSERT INTO Branch(office_id,`name`,address) VALUES
(1,'Центральный','ул. Ленина, д.3'),
(1,'Восточный','ул. Восточная, д.15'),
(1,'Западный','пр. Победы, д.8'),
(1,'Северный','ул. Северная, д.20'),
(1,'Южный','ул. Южная, д.5'),
(1,'Подольский','ул. Подольская, д.12'),
(1,'Оболонь','пр. Оболонский, д.4'),
(1,'Троещина','ул. Троещинская, д.30');

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
INSERT INTO `Client`(full_name, phone, email, is_profi_client) VALUES
('Иванов И.И.',    '+7(495)147-4601', 'ivanov@example.com',    FALSE),
('Петров П.П.',    '+7(495)147-4602', 'petrov@example.com',    TRUE),
('Сидорова С.С.',  '+7(495)147-4603', 'sidorova@example.com',  FALSE),
('Кузнецов А.А.',  '+7(495)147-4604', 'kuznetsov@example.com', TRUE),
('Михайлов М.М.',  '+7(495)147-4605', 'mihailov@example.com',  FALSE),
('Ильина И.И.',    '+7(495)147-4606', 'ilina@example.com',     TRUE),
('Андреев А.А.',   '+7(495)147-4607', 'andreev@example.com',   FALSE),
('Васильев В.В.',  '+7(495)147-4608', 'vasilev@example.com',   TRUE);

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
(4,2,3,0.04,'2025-02-01','2025-10-31'),
(6,3,4,0.06,'2025-03-01','2025-12-31'),
(8,4,2,0.03,'2025-04-01','2025-09-30');


-- Supplier
INSERT INTO Supplier (name, phone_number) VALUES
  ('PhotoSupply Ltd.', '+7(495)123-4567'),
  ('CamMasters',     '+7(495)234-5678'),
  ('FilmWorld',      '+7(495)345-6789'),
  ('AlbumArt',       '+7(495)456-7890'),
  ('PaperPro',       '+7(495)567-8901'),
  ('ChemLab',        '+7(495)678-9012'),
  ('FotoAcc',        '+7(495)789-0123'),
  ('PrintFast',      '+7(495)890-1234');

INSERT INTO ProductCategory (name) VALUES
  ('бумага'),
  ('химреактивы'),
  ('аппараты'),
  ('объективы'),
  ('пленки'),
  ('альбомы'),
  ('аксессуары');
  
-- Product
INSERT INTO Product (name, category_id, brand, unit_price) VALUES
  ('Kodak Gold',        5, 'Kodak',    200.00),
  ('Fujifilm Superia',   5, 'Fujifilm', 180.00),
  ('Canon EOS 80D',      3, 'Canon',    7000.00),
  ('Nikon D3500',        3, 'Nikon',    6500.00),
  ('Фотоальбом Classic', 6, 'Hama',     350.00),
  ('Фотоальбом Modern',  6, 'Brauberg', 400.00),
  ('Чехол для камеры',   7, 'CamCase',  250.00),
  ('Фотобумага Glossy',  1, 'Agfa',     60.00);


INSERT INTO SupplierSpecialization (supplier_id, category_id) VALUES
  -- PhotoSupply Ltd. (id = 1): бумага (1) и химреактивы (2)
  (1, 1),
  (1, 2),
  -- CamMasters (id = 2): аппараты (3) и объективы (4)
  (2, 3),
  (2, 4),
  -- FilmWorld (id = 3): пленки (5)
  (3, 5),
  -- AlbumArt (id = 4): альбомы (6)
  (4, 6),
  -- PaperPro (id = 5): бумага (1)
  (5, 1),
  -- ChemLab (id = 6): химреактивы (2)
  (6, 2),
  -- FotoAcc (id = 7): аксессуары (7)
  (7, 7),
  -- PrintFast (id = 8): пленки (5) и бумага (1)
  (8, 5),
  (8, 1);
  
  
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
(1, 1, NULL, 'film', TRUE, 100.00, 100.00, '2025-05-01'),
(2, 1, 1, 'print', FALSE, 50.00, 70.00, '2025-05-02'),
(3, 2, 3, 'both', FALSE, 120.00, 120.00, '2025-05-05'),
(4, 2, NULL, 'both', FALSE, 80.00, 80.00, '2025-05-07'),
(5, 2, 5, 'both', FALSE, 110.00, 130.00, '2025-05-08'),
(6, 4, 6, 'both', FALSE, 90.00, 90.00, '2025-05-09'),
(7, 4, NULL, 'print', TRUE, 60.00, 80.00, '2025-05-10'),
(8, 5, 7, 'film', FALSE, 100.00, 100.00, '2025-05-12');


-- FilmDevelopment
INSERT INTO FilmDevelopment(order_id,num_films,price_per_film) VALUES
(1,3,100.00),
(3,2,120.00),
(5,5,90.00),
(6,4,110.00);

-- PhotoPrint
INSERT INTO PhotoPrint(order_id,total_photos,`format`,paper_type) VALUES
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
INSERT INTO Sale(client_id,branch_id,kiosk_id,product_id,quantity) VALUES
(1,1,NULL,1,2),
(2,NULL,1,3,1),
(3,2,NULL,3,3),
(4,NULL,3,4,5),
(5,3,NULL,5,1),
(6,NULL,5,6,2),
(7,4,NULL,7,4),
(8,NULL,7,8,10);

-- ServiceType
INSERT INTO ServiceType(id,`description`) VALUES
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

INSERT INTO Workplace(branch_id, kiosk_id, position, duties) VALUES
(1, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(1, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(1, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(2, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(2, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(2, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(3, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(3, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(3, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(4, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(4, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(4, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(5, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(5, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(5, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(6, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(6, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(6, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(7, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(7, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(7, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),
(7, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),

(8, NULL, 'Администратор', 'Приём заказов, печать/проявка, работа с клиентами'),
(8, NULL, 'Фотограф',       'Фотосъёмка (документы, художественное, ретро)'),
(8, NULL, 'Реставратор',    'Реставрация фотографий, сканирование, оформление'),

(NULL, 1, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 2, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 3, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 4, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 5, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 6, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 7, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг'),
(NULL, 8, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг');

INSERT INTO Employee (full_name, hire_date, phone, login, password_hash, workplace_id) VALUES
-- Филиал 1
('Михалков Н.И.',    '2025-06-01', '+7(495)101-0001', 'admin1', '$2b$12$MHSeF/o8wJ3GCOsHPpnp1Oe6dG2B1k8o5UxYj5OuAEsjOf60hVa2q',  1),
('Юровская С.А.',    '2025-06-01', '+7(495)101-0002', 'photo1', '$2b$12$rCcp.K..ucN1WDGinocaHeIeEReixwcwgGQrQR0MwRGIThGlixKaG', 2),
('Казырицкий В.Н.',  '2025-06-01', '+7(495)101-0003', 'rest1',  '$2b$12$EzqoW2iimvggQ7G8GoUTCeMmkEPe3OTAuBnSoBhRO.SL36osS8KfK', 3),

-- Филиал 2
('Прокопьев И.С.',   '2025-06-02', '+7(495)102-0001', 'admin2', '$2b$12$xfMANEgZJHsvk2LqE5Xqi.gWSNLqFeLViikpx2SOAY/3ZLAlqxEKu', 4),
('Волков А.С.',      '2025-06-02', '+7(495)102-0002', 'photo2', '$2b$12$fh/1FrIvqEfpEzvF6vQCCeAUyH5lVwTxqyXauCkgaxCKDiqvz5SeG', 5),
('Морозова Е.И.',    '2025-06-02', '+7(495)102-0003', 'rest2',  '$2b$12$pIWCHy8fJ3YDdUDps40pOOQ2aSIL6tFfAGjBxyTU0puzquE7mc6se', 6),

-- Филиал 3
('Соколов Д.В.',     '2025-06-03', '+7(495)103-0001', 'admin3', '$2b$12$DM7CYYLSiZk.9Hcqi94dYeU6VAAr/bn66wk.zT0tPdS7GcuR6tMlm', 7),
('Лебедева Н.С.',    '2025-06-03', '+7(495)103-0002', 'photo3', '$2b$12$34dijXp8wjOVePfGgYhQkO5n2ExRfmq5OxVaWT2AlQVenXM68hz6G', 8),
('Новиков И.А.',     '2025-06-03', '+7(495)103-0003', 'rest3',  '$2b$12$7ebb25PWmsgpckjjQMqefOof5eIOQR2d8fsYVJzmm4wRWCQd1BIHe', 9),

-- Филиал 4
('Павлова А.В.',     '2025-06-04', '+7(495)104-0001', 'admin4', '$2b$12$ei6HdN16/46iqlv0F.bzCOk1YmsACQxTIPlPvLO.EDzko0ZzbIVSq', 10),
('Орлов П.С.',       '2025-06-04', '+7(495)104-0002', 'photo4', '$2b$12$HqE6A6yYkCJhzV6v0g65ReK8Pz5ukQUm5JRIu3WDoTJqcCdysT2au', 11),
('Федорова Е.Н.',    '2025-06-04', '+7(495)104-0003', 'rest4',  '$2b$12$4wpZk2BqqilkJo63lezmJeEpdIWBk5Ci74WlzsnUVKMUhvPx/.LJq', 12),

-- Филиал 5
('Козлов В.Г.',      '2025-06-05', '+7(495)105-0001', 'admin5', '$2b$12$QOXMfj0L0i8JELErNdEDy.CQaxLQcS.u0jTqkEQFS/pS3tk8VlEv6', 13),
('Степанова С.А.',   '2025-06-05', '+7(495)105-0002', 'photo5', '$2b$12$EkDAZCh1NHHepffhh.n1eerANgDdUXHsOloNI9rxsWYgQgDPzsqCm', 14),
('Семёнов Н.Ю.',     '2025-06-05', '+7(495)105-0003', 'rest5',  '$2b$12$c1qlEo1Ie5Ddmdrz2CkcF.ouSMauPab8Y4x0GAS.uLbJnJYQrlIz2', 15),

-- Филиал 6
('Егоров О.Л.',      '2025-06-06', '+7(495)106-0001', 'admin6', '$2b$12$5Yzknku7aWnsUngvR8Xnne9PIME9AY4CEv6MJZx.9vToTuUtXrFzm', 16),
('Никитина И.П.',    '2025-06-06', '+7(495)106-0002', 'photo6', '$2b$12$KkveJLP0gFsWy6rQ27BkiuMEatC6kyr6laOAoj5rEhX0JWBa.eTF.', 17),
('Виноградов М.Е.',  '2025-06-06', '+7(495)106-0003', 'rest6',  '$2b$12$O.mdxVffpcEa7881lY1fU.RayoE6lPO2S2WoDwE83Tpdx1XIiyw4a', 18),

-- Филиал 7
('Белова Т.И.',      '2025-06-07', '+7(495)107-0001', 'admin7', '$2b$12$Ug1ow5DvxdpFwXeeAoOgN.ypAX4mpcdN6b2zNY9/YMpX88X61jTmK', 19),
('Захаров Д.М.',     '2025-06-07', '+7(495)107-0002', 'photo7', '$2b$12$n5Y8XH29Pu1MJn4QWvP5yu/phgM2kP1/eLCaEbQa3LChqdRRLU1Ze', 20),
('Крылова Ю.А.',     '2025-06-07', '+7(495)107-0003', 'rest7',  '$2b$12$ul/4By5MNKCbRhbOkbi38uTt0yYrjXIb7reNC8edOAuE/p6e1JDSe', 21),

-- Филиал 8
('Лебедев К.А.',     '2025-06-08', '+7(495)108-0001', 'admin8', '$2b$12$rvZyHQzrsjEvycMsuiegDO3eph29xcXRckiPymJ5CTEhvT6uBMVFK', 22),
('Волкова М.Е.',     '2025-06-08', '+7(495)108-0002', 'photo8', '$2b$12$5zc/6ViOEco3jW7WmIWTuu38kHat9.AuV/IVlqaP8q2li6WIWN9bq', 23),
('Орехов А.Р.',      '2025-06-08', '+7(495)108-0003', 'rest8',  '$2b$12$rKST6/vU.2o.7rw2EjYQkOeHAdlTlJRcV8xjGrqyaj1P3/nj2WtX2', 24),

-- Киоски
('Киселева О.Г.',    '2025-06-09', '+7(495)101-0004', 'kiosk1', '$2b$12$SFfC3OK9k4dvJ2wVZan6yuTFvTYK37PX1SS/KpK5CxM30mDsuP/da', 25),
('Соколов В.Н.',     '2025-06-09', '+7(495)101-0005', 'kiosk2', '$2b$12$vf9GyRMl2UJPyGFxw0lkOuqdfFOvlUZE9ZuO.m5zjW/XBSaVCdgJi', 26),
('Максимова Е.Б.',   '2025-06-09', '+7(495)102-0004', 'kiosk3', '$2b$12$FMyYJw4.OrHTaAjdBZ9F5uWViDbEMJv7wsKCSa82qy3CIIy3YGchC', 27),
('Новиков И.А.',     '2025-06-09', '+7(495)102-0005', 'kiosk4', '$2b$12$ZrdOP0QRYOLp.ZnsXqHQneqf0LfU.SP7kg8jqczA9IoKGKRIGis.K', 28),
('Павлова Л.М.',     '2025-06-09', '+7(495)103-0004', 'kiosk5', '$2b$12$sARJDevQ.cQspt8sn8qPk.DVvVwMfy0M/SOEVD0KwUIsCantStGwe', 29),
('Викторов Р.Г.',    '2025-06-09', '+7(495)104-0004', 'kiosk6', '$2b$12$y3w5Hz5a5CDnQRoBSypdLuo2tUeuyVzjai3imr06IGNAYmPmZu.A.', 30),
('Попов Н.В.',       '2025-06-09', '+7(495)105-0004', 'kiosk7', '$2b$12$rw2POi0xcuruHczuC1gcU.j4OqQNbVsh44rncZ30tVhsSZ/APEa3y', 31),
('Козлов Д.Е.',      '2025-06-09', '+7(495)106-0004', 'kiosk8', '$2b$12$7/WiInA1mKp4hxMZkCWzQeLNNwJqH0QVaxokYqFqx8TujqHlRX7bm', 32);

INSERT INTO Role (name, description) VALUES
('Администратор', 'Полный доступ ко всем функциям и данным'),
('Фотограф', 'Доступ только к заказам, клиентам и печати/проявке по своему филиалу'),
('Реставратор', 'Доступ только к заказам, клиентам и реставрации по своему филиалу'),
('Оператор киоска', 'Доступ к заказам, продажам и клиентам по своему киоску');

INSERT INTO Permission (name, description) VALUES
('view_all', 'Просмотр всех данных'),
('edit_all', 'Редактирование всех данных'),
('delete_all', 'Удаление всех данных'),
('view_own_branch', 'Просмотр данных только по своему филиалу'),
('view_own_kiosk', 'Просмотр данных только по своему киоску'),
('edit_own_branch', 'Редактирование данных по своему филиалу'),
('edit_own_kiosk', 'Редактирование данных по своему киоску'),
('raw_sql', 'Выполнение сырых SQL-запросов'),
('manage_roles', 'Управление ролями и правами');

-- Администратор: все права
INSERT INTO RolePermission (role_id, permission_id)
SELECT 1, id FROM Permission;

-- Фотограф: только просмотр по своему филиалу
INSERT INTO RolePermission (role_id, permission_id) VALUES
(2, 4), -- view_own_branch
(2, 6); -- edit_own_branch

-- Реставратор: только просмотр по своему филиалу
INSERT INTO RolePermission (role_id, permission_id) VALUES
(3, 4), -- view_own_branch
(3, 6); -- edit_own_branch

-- Оператор киоска: только по своему киоску
INSERT INTO RolePermission (role_id, permission_id) VALUES
(4, 5), -- view_own_kiosk
(4, 7); -- edit_own_kiosk