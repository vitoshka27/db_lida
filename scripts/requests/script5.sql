SELECT 
  b.name AS `Филиал`,
  k.kiosk_name as `Киоск`,
  CASE
        WHEN o.is_urgent THEN 'Да'
        ELSE 'Нет'
    END AS `Срочный`,
  SUM(pp.total_photos) AS `Всего фотографий`
FROM PhotoPrint pp
JOIN `Order` o ON pp.order_id = o.id
LEFT JOIN Branch b ON o.branch_id = b.id
LEFT JOIN Kiosk k ON o.kiosk_id = k.id
WHERE 1=1
	-- AND o.is_urgent = 1
	-- AND o.order_date BETWEEN '2023-05-01' AND '2027-05-10'
	-- AND (o.branch_id = 2 AND o.kiosk_id IS NULL)
    -- AND o.kiosk_id = 1
GROUP BY b.name, k.kiosk_name, o.is_urgent
ORDER BY b.name, k.kiosk_name, o.is_urgent;
