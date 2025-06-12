DELIMITER //
CREATE FUNCTION get_order_volume(p_order_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE photos INT DEFAULT 0;
  DECLARE films INT DEFAULT 0;

  SELECT IFNULL(SUM(pp.total_photos), 0)
  INTO photos
  FROM PhotoPrint pp
  WHERE pp.order_id = p_order_id;

  SELECT IFNULL(SUM(fd.num_films), 0)
  INTO films
  FROM FilmDevelopment fd
  WHERE fd.order_id = p_order_id;

  RETURN photos + films;
END;
//

DELIMITER ;
