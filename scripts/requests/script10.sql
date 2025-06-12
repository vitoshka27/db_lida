SELECT
    p.name AS `Товар`,
    p.brand AS `Фирма`,
    SUM(s.quantity) AS `Всего продано`
FROM Sale s
JOIN Product p ON s.product_id = p.id
WHERE 1=1
   -- AND s.branch_id = 1  
GROUP BY p.name, p.brand
ORDER BY `Всего продано` DESC;
