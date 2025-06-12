SELECT
    b.name AS `Филиал`,
	k.kiosk_name AS `Киоск`,
    SUM(s.quantity * p.unit_price) AS `Выручка`,
    SUM(SUM(s.quantity * p.unit_price)) OVER () AS `Общая выручка`
FROM Sale s
LEFT JOIN Branch b ON s.branch_id = b.id
LEFT JOIN Kiosk k ON s.kiosk_id = k.id
JOIN Product p ON s.product_id = p.id
WHERE 1=1
	-- AND (s.branch_id = 1 AND s.kiosk_id IS NULL)
    -- AND (s.kiosk_id IS NOT NULL AND s.branch_id IS NULL)
    -- AND s.sale_date BETWEEN '2025-05-01' AND '2025-07-01'
GROUP BY
	b.name,
    k.kiosk_name