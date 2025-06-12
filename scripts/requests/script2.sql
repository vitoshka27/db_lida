SELECT
	cl.full_name as `ФИО клиента`,
	b.name as `Филиал`,
    k.kiosk_name as `Киоск`,
	o.price as `Цена без скидки`,
    o.total_price as `Цена со скидкой`,
    o.order_date as `Дата заказа`,
	COUNT(*) OVER() AS `Количество заказов`
FROM `Order` o
JOIN Client cl ON o.client_id = cl.id
JOIN Branch b ON o.branch_id = b.id
LEFT JOIN Kiosk k ON o.kiosk_id = k.id
WHERE 1=1
	-- AND (o.branch_id IS NOT NULL AND o.kiosk_id IS NULL)
    -- AND o.kiosk_id IS NOT NULL
    -- AND o.order_date BETWEEN '2025-05-05' AND '2025-05-09'
ORDER BY
	o.order_date;