SELECT 
	s.name as `Поставщик`,
	s.phone_number as `Номер телефона`,
	GROUP_CONCAT(pc.name SEPARATOR ', ') AS `Категории`
from Supplier s
JOIN SupplierSpecialization sp on s.id = sp.supplier_id
JOIN ProductCategory pc ON sp.category_id = pc.id
JOIN Supply su ON s.id = su.supplier_id
where 1=1
	-- AND sp.category_id = 1
    -- AND su.supply_date BETWEEN '2025-03-01' AND '2025-03-05'
    -- AND su.quantity BETWEEN '50' AND '200'
GROUP BY
    s.name,
    s.phone_number
ORDER BY
	s.name;