from typing import Dict, Any
import re

class QueryFilterSorter:
    """
    Базовый класс для фильтрации и сортировки SQL-запросов.
    """
    def __init__(self, sql: str, filters: Dict[str, Any], sort_column: str = None, sort_asc: bool = True):
        self.sql = sql
        self.filters = filters
        self.sort_column = sort_column
        self.sort_asc = sort_asc

    def build_query(self) -> str:
        """
        Возвращает финальный SQL с учётом фильтров и сортировки.
        Должен быть переопределён в наследниках для уникальной логики.
        """
        sql = self.sql
        # Применяем фильтры (по умолчанию — как в старой логике)
        for key, value in self.filters.items():
            if value:
                sql = re.sub(rf"-- (AND [^\n]*\{{{key}\}}[^\n]*)", lambda m: m.group(1).replace(f'{{{key}}}', str(value)), sql)
        # Применяем сортировку (по умолчанию — заменяем ORDER BY)
        if self.sort_column:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY `{self.sort_column}` {order};'
        return sql

    def _remove_last_order_by(self, sql: str) -> str:
        pattern = re.compile(r'ORDER BY[\s\S]*?(;|$)', re.IGNORECASE)
        matches = list(pattern.finditer(sql))
        if matches:
            m = matches[-1]
            sql = sql[:m.start()] + sql[m.end():]
            sql = re.sub(r',\s*$', '', sql[:m.start()]) + sql[m.start():]
        return sql

# Пример для первого скрипта (script1.sql)
class Script1FilterSorter(QueryFilterSorter):
    def build_query(self) -> str:
        sql = self.sql
        # Фильтр по типу точки
        if self.filters.get('type'):
            sql = re.sub(r"-- AND p\.point_type = \{type\}", f"AND p.point_type = '{self.filters['type']}'", sql)
        else:
            sql = re.sub(r'(^|\n)\s*AND p\.point_type = \'[^\']*\'', r"\1-- AND p.point_type = '{type}'", sql)
        # Фильтр по branch_id/kiosk_id (CTE)
        if self.filters.get('branch_id'):
            sql = re.sub(r'-- WHERE b\.id = [0-9]+', f'WHERE b.id = {self.filters["branch_id"]}', sql)
        if self.filters.get('kiosk_id'):
            sql = re.sub(r'-- WHERE k\.id = [0-9]+', f'WHERE k.id = {self.filters["kiosk_id"]}', sql)
        # Сортировка по умолчанию (как в оригинале)
        if self.sort_column:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY `{self.sort_column}` {order};'
        return sql

class Script2FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'ФИО клиента': 'cl.full_name',
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Цена без скидки': 'o.price',
        'Цена со скидкой': 'o.total_price',
        'Дата заказа': 'o.order_date',
        'Количество заказов': None,
    }
    def build_query(self) -> str:
        sql = self.sql
        # --- Уникальная логика фильтрации ---
        type_val = self.filters.get('type')
        branch_id = self.filters.get('branch_id')
        kiosk_id = self.filters.get('kiosk_id')
        # Приоритет: конкретный филиал/киоск > тип точки
        if branch_id and not kiosk_id:
            sql = re.sub(r"-- AND \(o.branch_id IS NOT NULL AND o.kiosk_id IS NULL\)", f"AND (o.branch_id = {branch_id} AND o.kiosk_id IS NULL)", sql)
        elif kiosk_id:
            sql = re.sub(r"-- AND o.kiosk_id IS NOT NULL", f"AND o.kiosk_id = {kiosk_id}", sql)
        elif type_val == 'Филиал':
            sql = re.sub(r"-- AND \(o.branch_id IS NOT NULL AND o.kiosk_id IS NULL\)", f"AND (o.branch_id IS NOT NULL AND o.kiosk_id IS NULL)", sql)
        elif type_val == 'Киоск':
            sql = re.sub(r"-- AND o.kiosk_id IS NOT NULL", f"AND o.kiosk_id IS NOT NULL", sql)
        # Дата
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND o.order_date BETWEEN '[^']*' AND '[^']*'", f"AND o.order_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script3FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'ФИО клиента': 'cl.full_name',
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Тип заказа': 'o.order_type',
        'Срочный': 'o.is_urgent',
        'Цена без скидки': 'o.price',
        'Цена со скидкой': 'o.total_price',
        'Дата заказа': 'o.order_date',
        'Количество заказов': None,
    }
    def build_query(self) -> str:
        sql = self.sql
        # Только эти фильтры реально есть в скрипте:
        if self.filters.get('branch_id') and not self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND \(o.branch_id IS NOT NULL AND o.kiosk_id IS NULL\)", f"AND (o.branch_id IS NOT NULL AND o.kiosk_id IS NULL)", sql)
        if self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND o.kiosk_id IS NOT NULL", f"AND o.kiosk_id IS NOT NULL", sql)
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND o.order_date BETWEEN '[^']*' AND '[^']*'", f"AND o.order_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        if self.filters.get('order_type'):
            sql = re.sub(r"-- AND o.order_type = '[^']*'", f"AND o.order_type = '{self.filters['order_type']}'", sql)
        if self.filters.get('is_urgent'):
            sql = re.sub(r"-- AND o.is_urgent = '[^']*'", f"AND o.is_urgent = '{self.filters['is_urgent']}'", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script4FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Тип заказа': 'o.order_type',
        'Срочный': 'o.is_urgent',
        'Выручка': '`Выручка`',
        'Общая выручка': '`Общая выручка`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND o.order_date BETWEEN '[^']*' AND '[^']*'", f"AND o.order_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        if self.filters.get('branch_id') and not self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND \(o.branch_id IS NOT NULL AND o.kiosk_id IS NULL\)", f"AND (o.branch_id IS NOT NULL AND o.kiosk_id IS NULL)", sql)
        if self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND o.kiosk_id = [0-9]+", f"AND o.kiosk_id = {self.filters['kiosk_id']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script5FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Срочный': 'o.is_urgent',
        'Всего фотографий': '`Всего фотографий`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('is_urgent'):
            sql = re.sub(r"-- AND o.is_urgent = [0-9]+", f"AND o.is_urgent = {self.filters['is_urgent']}", sql)
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND o.order_date BETWEEN '[^']*' AND '[^']*'", f"AND o.order_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        if self.filters.get('branch_id') and not self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND \(o.branch_id = [0-9]+ AND o.kiosk_id IS NULL\)", f"AND (o.branch_id = {self.filters['branch_id']} AND o.kiosk_id IS NULL)", sql)
        if self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND o.kiosk_id = [0-9]+", f"AND o.kiosk_id = {self.filters['kiosk_id']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script6FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Срочный': 'o.is_urgent',
        'Всего пленок': '`Всего пленок`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('is_urgent'):
            sql = re.sub(r"-- AND o.is_urgent = [0-9]+", f"AND o.is_urgent = {self.filters['is_urgent']}", sql)
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND o.order_date BETWEEN '[^']*' AND '[^']*'", f"AND o.order_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        if self.filters.get('branch_id') and not self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND \(o.branch_id = [0-9]+ AND o.kiosk_id IS NULL\)", f"AND (o.branch_id = {self.filters['branch_id']} AND o.kiosk_id IS NULL)", sql)
        if self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND o.kiosk_id = [0-9]+", f"AND o.kiosk_id = {self.filters['kiosk_id']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script7FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Поставщик': 's.name',
        'Номер телефона': 's.phone_number',
        'Категории': '`Категории`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('category_id'):
            sql = re.sub(r"-- AND sp.category_id = [0-9]+", f"AND sp.category_id = {self.filters['category_id']}", sql)
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND su.supply_date BETWEEN '[^']*' AND '[^']*'", f"AND su.supply_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        if self.filters.get('qty_from') and self.filters.get('qty_to'):
            sql = re.sub(r"-- AND su.quantity BETWEEN '[^']*' AND '[^']*'", f"AND su.quantity BETWEEN {self.filters['qty_from']} AND {self.filters['qty_to']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script8FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'ФИО': 'c.full_name',
        'Телефон': 'c.phone',
        'E-mail': 'c.email',
        'Всего фотографий': '`Всего фотографий`',
        'Всего пленок': '`Всего пленок`',
        'Объем заказов': '`Объем заказов`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('branch_id'):
            sql = re.sub(r"-- AND o.branch_id = [0-9]+", f"AND o.branch_id = {self.filters['branch_id']}", sql)
        if self.filters.get('is_profi'):
            sql = re.sub(r"-- AND \(c.is_profi_client = [0-9]+ or dc.client_id IS NOT NULL\)", f"AND (c.is_profi_client = {self.filters['is_profi']} or dc.client_id IS NOT NULL)", sql)
        if self.filters.get('vol_from') and self.filters.get('vol_to'):
            sql = re.sub(r"-- HAVING `Объем заказов` BETWEEN [0-9]+ AND [0-9]+", f"HAVING `Объем заказов` BETWEEN {self.filters['vol_from']} AND {self.filters['vol_to']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script9FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Выручка': '`Выручка`',
        'Общая выручка': '`Общая выручка`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('branch_id') and not self.filters.get('kiosk_id'):
            sql = re.sub(r"-- AND \(s.branch_id = [0-9]+ AND s.kiosk_id IS NULL\)", f"AND (s.branch_id = {self.filters['branch_id']} AND s.kiosk_id IS NULL)", sql)
        if self.filters.get('kiosk_id') and not self.filters.get('branch_id'):
            sql = re.sub(r"-- AND \(s.kiosk_id IS NOT NULL AND s.branch_id IS NULL\)", f"AND (s.kiosk_id IS NOT NULL AND s.branch_id IS NULL)", sql)
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND s.sale_date BETWEEN '[^']*' AND '[^']*'", f"AND s.sale_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script10FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Товар': 'p.name',
        'Фирма': 'p.brand',
        'Всего продано': '`Всего продано`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('branch_id'):
            sql = re.sub(r"-- AND s.branch_id = [0-9]+", f"AND s.branch_id = {self.filters['branch_id']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script11FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Товар': 'p.name',
        'Фирма': 'p.brand',
        'Всего продано': '`Всего продано`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('date_from') and self.filters.get('date_to'):
            sql = re.sub(r"-- AND s.sale_date BETWEEN '[^']*' AND '[^']*'", f"AND s.sale_date BETWEEN '{self.filters['date_from']}' AND '{self.filters['date_to']}'", sql)
        if self.filters.get('branch_id'):
            sql = re.sub(r"-- AND s.branch_id = [0-9]+", f"AND s.branch_id = {self.filters['branch_id']}", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql

class Script12FilterSorter(QueryFilterSorter):
    COLUMN_MAP = {
        'Филиал': 'b.name',
        'Киоск': 'k.kiosk_name',
        'Должность': 'w.position',
        'Обязанности': '`Обязанности`',
    }
    def build_query(self) -> str:
        sql = self.sql
        if self.filters.get('position'):
            sql = re.sub(r"-- AND w.position = '[^']*'", f"AND w.position = '{self.filters['position']}'", sql)
        sort_field = None
        if self.sort_column:
            sort_field = self.COLUMN_MAP.get(self.sort_column, None)
        if sort_field:
            sql = self._remove_last_order_by(sql)
            order = 'ASC' if self.sort_asc else 'DESC'
            sql = sql.strip().rstrip(';')
            if not sql.endswith('\n'):
                sql += '\n'
            sql += f'ORDER BY {sort_field} {order};'
        return sql 