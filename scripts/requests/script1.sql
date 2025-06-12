WITH points AS (
  SELECT
    b.name              AS point_name,
    b.address           AS point_address,
    'Филиал'            AS point_type
  FROM Branch b
 -- WHERE b.id = 3

  UNION ALL

  SELECT
    k.kiosk_name        AS point_name,
    k.address           AS point_address,
    'Киоск'             AS point_type
  FROM Kiosk k
   -- WHERE k.id = 1
)

SELECT
  p.point_name `Название точки`,
  p.point_address as `Адрес`,
  p.point_type `Тип точки`,
  COUNT(*) OVER() AS `Всего точек`
FROM points p
WHERE 1 = 1
-- AND p.point_type = {type}
ORDER BY
  p.point_type,
  p.point_name;
