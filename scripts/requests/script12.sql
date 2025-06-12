SELECT
	b.name  AS `Филиал`,
    k.kiosk_name AS `Киоск`,
    w.position AS `Должность`,
    w.duties AS `Обязанности`
FROM Workplace w
LEFT JOIN Branch b ON w.branch_id = b.id
LEFT JOIN Kiosk  k ON w.kiosk_id  = k.id
WHERE 1 = 1
	-- AND w.position = 'Администратор'
ORDER BY
	`Киоск`,
	`Филиал`,
    `Должность`