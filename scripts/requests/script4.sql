SELECT
    b.name AS `Филиал`,
    k.kiosk_name AS `Киоск`,
    CASE 
        WHEN o.order_type = 'film'  THEN 'Проявка'
        WHEN o.order_type = 'print' THEN 'Печать'
        ELSE 'Проявка + Печать'
    END AS `Тип заказа`,
    CASE
        WHEN o.is_urgent THEN 'Да'
        ELSE 'Нет'
    END AS `Срочный`,
    SUM(o.total_price) AS `Выручка`,
    SUM(SUM(o.total_price)) OVER () AS `Общая выручка`
FROM `Order` o
JOIN Branch b   ON o.branch_id = b.id
LEFT JOIN Kiosk k ON o.kiosk_id = k.id
WHERE 1=1
    -- AND o.order_date BETWEEN '2025-05-01' AND '2025-05-31'
    -- AND (o.branch_id IS NOT NULL AND o.kiosk_id IS NULL)
    -- AND o.kiosk_id = 7
GROUP BY
    b.name,
    k.kiosk_name,
    o.order_type,
    o.is_urgent
ORDER BY
    o.order_type,
    o.is_urgent;