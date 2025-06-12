SELECT DISTINCT 
	c.full_name, 
    c.phone, 
    c.email,
	SUM(pp.total_photos) AS `Всего фотографий`,
    SUM(fd.num_films) AS `Всего пленок`,
	SUM(get_order_volume(o.id)) AS `Объем заказов`
FROM Client c
JOIN `Order` o ON c.id = o.client_id
LEFT JOIN DiscountCard dc ON c.id = dc.client_id
LEFT JOIN PhotoPrint pp ON o.id = pp.order_id
LEFT JOIN FilmDevelopment fd ON o.id = fd.order_id
WHERE 1=1
	-- AND o.branch_id = 2
    -- AND (c.is_profi_client = 1 or dc.client_id IS NOT NULL)
GROUP BY c.full_name, c.phone, c.email
-- HAVING `Объем заказов` BETWEEN 100 AND 160
ORDER BY c.full_name, `Всего фотографий` DESC;