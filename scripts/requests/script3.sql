SELECT
	cl.full_name as `ФИО клиента`,
	b.name as `Филиал`,
    k.kiosk_name as `Киоск`,
    CASE
		WHEN o.order_type = 'film'  THEN 'Проявка'
		WHEN o.order_type = 'print' THEN 'Печать'
		ELSE 'Проявка + Печать'
	END AS `Тип заказа`,
	CASE 
		WHEN o.is_urgent THEN 'Да'
		ELSE 'Нет'
	END AS `Срочный`,
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
    -- AND o.order_type = 'both'
    -- AND o.is_urgent = '1'
ORDER BY
	o.order_date;