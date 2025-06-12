from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QLabel, QSpinBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from ui.record_form import RecordForm
from services.entity_services import *

COLUMN_TRANSLATIONS = {
    'MainOffice': {
        'address': 'Адрес',
        'phone': 'Телефон',
        'manager_name': 'Менеджер',
        'workplace_count_for_branch': 'Раб. мест (филиал)',
        'workplace_count_for_kiosk': 'Раб. мест (киоск)',
    },
    'Branch': {
        'name': 'Название',
        'address': 'Адрес',
    },
    'Kiosk': {
        'branch_id': 'Название филиала',
        'kiosk_name': 'Название киоска',
        'address': 'Адрес',
    },
    'Client': {
        'full_name': 'ФИО',
        'phone': 'Телефон',
        'email': 'E-mail',
        'is_profi_client': 'Профи-клиент',
    },
    'DiscountCard': {
        'client_id': 'ФИО клиента',
        'issue_date': 'Дата выдачи',
        'discount_rate': 'Скидка',
    },
    'ProfiDiscount': {
        'client_id': 'ФИО клиента',
        'branch_id': 'Название филиала',
        'min_orders': 'Мин. заказов',
        'discount_rate': 'Скидка',
        'valid_from': 'Действует с',
        'valid_to': 'Действует до',
    },
    'Supplier': {
        'name': 'Название',
        'phone_number': 'Телефон',
    },
    'ProductCategory': {
        'name': 'Категория',
    },
    'SupplierSpecialization': {
        'supplier_id': 'Поставщик',
        'category_id': 'Категория',
    },
    'Product': {
        'name': 'Название',
        'category_id': 'Категория',
        'brand': 'Бренд',
        'unit_price': 'Цена за ед.',
    },
    'Supply': {
        'id': 'Номер поставки',
        'supplier_id': 'Поставщик',
        'product_id': 'Товар',
        'supply_date': 'Дата поставки',
        'quantity': 'Кол-во',
        'total_cost': 'Сумма',
    },
    'Distribution': {
        'supply_id': 'Номер поставки',
        'to_branch_id': 'Филиал',
        'to_kiosk_id': 'Киоск',
        'quantity': 'Кол-во',
        'dist_date': 'Дата',
    },
    'Order': {
        'id': 'Номер заказа',
        'client_id': 'ФИО клиента',
        'branch_id': 'Филиал',
        'kiosk_id': 'Киоск',
        'order_type': 'Тип заказа',
        'is_urgent': 'Срочно',
        'price': 'Цена',
        'total_price': 'Итого',
        'order_date': 'Дата заказа',
    },
    'FilmDevelopment': {
        'order_id': 'Номер заказа',
        'num_films': 'Кол-во пленок',
        'price_per_film': 'Цена за пленку',
    },
    'PhotoPrint': {
        'order_id': 'Номер заказа',
        'total_photos': 'Кол-во фото',
        'format': 'Формат',
        'paper_type': 'Тип бумаги',
    },
    'PrintDetail': {
        'order_id': 'Номер заказа',
        'frame_number': 'Кадр',
        'copies_count': 'Кол-во копий',
    },
    'Sale': {
        'client_id': 'ФИО клиента',
        'branch_id': 'Филиал',
        'kiosk_id': 'Киоск',
        'product_id': 'Товар',
        'quantity': 'Кол-во',
    },
    'ServiceType': {
        'description': 'Описание',
    },
    'ServiceOrder': {
        'client_id': 'ФИО клиента',
        'branch_id': 'Филиал',
        'service_code': 'Услуга',
        'price': 'Цена',
        'details': 'Детали',
    },
    'Workplace': {
        'branch_id': 'Филиал',
        'kiosk_id': 'Киоск',
        'position': 'Должность',
        'duties': 'Обязанности',
    },
    'Employee': {
        'full_name': 'ФИО',
        'hire_date': 'Дата найма',
        'phone': 'Телефон',
        'login': 'Логин',
        'password_hash': 'Пароль (хэш)',
        'workplace_id': 'Место работы',
    },
    'RolePermission': {
        'role_id': 'Роль',
        'permission_id': 'Право',
    },
    'UserRole': {
        'employee_id': 'Сотрудник',
        'role_id': 'Роль',
    },
    'Role': {
        'name': 'Роль',
        'description': 'Описание',
    },
    'Permission': {
        'name': 'Право',
        'description': 'Описание',
    },
}

print("TableWidget module loaded")

class TableWidget(QWidget):
    def __init__(self, table_name, user_info=None, service=None):
        print(f"TableWidget for {table_name} created")
        super().__init__()
        self.table_name = table_name
        self.user_info = user_info or {}
        self.service = service  # сервис для работы с данными
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(self)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.setStyleSheet('''
            QTableWidget {
                background: #fff;
                border-radius: 18px;
                border: 2px solid #e0e4ea;
                font-size: 19px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                selection-background-color: #e3f0ff;
                selection-color: #23272e;
                gridline-color: #e0e4ea;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f8cff, stop:1 #6ec6ff);
                color: #fff;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
                padding: 12px 0;
            }
            QTableWidget::item {
                color: #23272e;
                background: #fff;
                border-bottom: 1.5px solid #e0e4ea;
                padding: 10px 16px;
                font-size: 19px;
            }
            QTableWidget::item:selected {
                background: #e3f0ff;
                color: #23272e;
            }
        ''')
        self.layout.addWidget(self.table)
        # Пагинация
        self.pagination_layout = QHBoxLayout()
        self.prev_btn = QPushButton('Назад')
        self.next_btn = QPushButton('Вперёд')
        self.page_label = QLabel()
        self.page_size_spin = QSpinBox()
        self.page_size_spin.setRange(5, 100)
        self.page_size_spin.setValue(20)
        self.pagination_layout.addWidget(self.prev_btn)
        self.pagination_layout.addWidget(self.next_btn)
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(QLabel('На странице:'))
        self.pagination_layout.addWidget(self.page_size_spin)
        self.layout.addLayout(self.pagination_layout)
        self.current_page = 1
        self.total_pages = 1
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.page_size_spin.valueChanged.connect(self.change_page_size)
        self.button_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        for btn in (self.btn_add, self.btn_edit, self.btn_delete):
            btn.setStyleSheet('''
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f8cff, stop:1 #6ec6ff);
                    color: #fff;
                    border-radius: 10px;
                    font-size: 15px;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    padding: 8px 24px;
                    margin: 8px 8px 8px 0;
                    border: none;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6ec6ff, stop:1 #4f8cff);
                    color: #fff;
                }
            ''')
        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_edit)
        self.button_layout.addWidget(self.btn_delete)
        self.layout.addLayout(self.button_layout)
        self.btn_add.clicked.connect(self.add_record)
        self.btn_edit.clicked.connect(self.edit_record)
        self.btn_delete.clicked.connect(self.delete_record)
        self.setup_permissions()
        self.load_data()

    def setup_permissions(self):
        permissions = set(self.user_info.get('permissions', []))
        # Добавление
        if not (('edit_all' in permissions) or ('edit_own_branch' in permissions) or ('edit_own_kiosk' in permissions)):
            self.btn_add.hide()
        # Редактирование
        if not (('edit_all' in permissions) or ('edit_own_branch' in permissions) or ('edit_own_kiosk' in permissions)):
            self.btn_edit.hide()
        # Удаление
        if not (('delete_all' in permissions) or ('edit_own_branch' in permissions) or ('edit_own_kiosk' in permissions)):
            self.btn_delete.hide()

    def load_data(self):
        try:
            page_size = self.page_size_spin.value()
            page = self.current_page
            permissions = set(self.user_info.get('permissions', []))
            branch_id = self.user_info.get('branch_id')
            kiosk_id = self.user_info.get('kiosk_id')
            filters = {}
            if self.service:
                # Фильтрация по правам
                if 'view_all' not in permissions:
                    if 'view_own_branch' in permissions and branch_id:
                        filters['branch_id'] = branch_id
                    elif 'view_own_kiosk' in permissions and kiosk_id:
                        filters['kiosk_id'] = kiosk_id
                # --- Исправление: поддержка сервисов без get_page ---
                if hasattr(self.service, 'get_page'):
                    rows, total = self.service.get_page(page, page_size, filters=filters)
                else:
                    all_rows = self.service.get_all(filters=filters)
                    total = len(all_rows)
                    start = (page - 1) * page_size
                    end = start + page_size
                    rows = all_rows[start:end]
                self.total_pages = max(1, (total + page_size - 1) // page_size)
                self.page_label.setText(f"Страница {self.current_page} из {self.total_pages} (всего: {total})")
                if rows:
                    model = type(rows[0])
                    all_columns = list(model.__table__.columns.keys())
                    pk_cols = [col.name for col in model.__table__.primary_key.columns]
                    hidden_cols = {'_sa_instance_state'}
                    if self.table_name == 'Branch':
                        hidden_cols.add('office_id')
                    # --- Корректная логика: columns = все поля, visible_columns = только нужные ---
                    columns = [col for col in all_columns if col not in hidden_cols]
                    self.columns = columns
                    if self.table_name in ('Order', '`Order`', 'Supply', '`Supply`'):
                        self.visible_columns = columns[:]
                    else:
                        self.visible_columns = [col for col in columns if col != 'id']
                    # --- END ---
                    table_key = self.table_name.strip('`')
                    col_trans = COLUMN_TRANSLATIONS.get(table_key, {})
                    header_labels = [col_trans.get(col, col) for col in columns]
                    self.table.setRowCount(len(rows))
                    self.table.setColumnCount(len(columns))
                    self.table.setHorizontalHeaderLabels(header_labels)
                    # Скрываем id если не нужен
                    if 'id' in columns and 'id' not in self.visible_columns:
                        idx = columns.index('id')
                        self.table.setColumnHidden(idx, True)
                    # Карта: внешний ключ -> (имя relationship, поле для отображения)
                    fk_display = {
                        'client_id':    ('client', 'full_name'),
                        'branch_id':    ('branch', 'name'),
                        'kiosk_id':     ('kiosk', 'kiosk_name'),
                        'product_id':   ('product', 'name'),
                        'supplier_id':  ('supplier', 'name'),
                        'category_id':  ('category', 'name'),
                        'service_code': ('service', 'description'),
                        'workplace_id': ('workplace', 'position'),
                        # Для Distribution — показываем имя филиала/киоска
                        'to_branch_id': ('branch', 'name'),
                        'to_kiosk_id':  ('kiosk', 'kiosk_name'),
                        'role_id': ('role', 'name'),
                        'permission_id': ('permission', 'name'),
                        'employee_id': ('employee', 'full_name'),
                    }
                    order_type_map = {'film': 'Проявка плёнки', 'print': 'Печать фото', 'both': 'Печать и проявка'}
                    for i, obj in enumerate(rows):
                        for j, col in enumerate(columns):
                            val = getattr(obj, col, '')
                            # Если это внешний ключ и есть relationship, показываем связанное значение
                            if col == 'workplace_id' and self.table_name == 'Employee':
                                workplace = getattr(obj, 'workplace', None)
                                if workplace:
                                    if getattr(workplace, 'branch_id', None):
                                        branch = getattr(workplace, 'branch', None)
                                        branch_name = getattr(branch, 'name', '') if branch else ''
                                        val = f"Филиал {branch_name} - {getattr(workplace, 'position', '')}"
                                    elif getattr(workplace, 'kiosk_id', None):
                                        kiosk = getattr(workplace, 'kiosk', None)
                                        kiosk_name = getattr(kiosk, 'kiosk_name', '') if kiosk else ''
                                        val = f"Киоск {kiosk_name} - {getattr(workplace, 'position', '')}"
                                    else:
                                        val = getattr(workplace, 'position', '')
                            elif col in fk_display:
                                rel, rel_field = fk_display[col]
                                rel_obj = getattr(obj, rel, None)
                                if rel_obj is not None:
                                    val = getattr(rel_obj, rel_field, val)
                            # Для order_type — перевод
                            if self.table_name == '`Order`' and col == 'order_type':
                                val = order_type_map.get(val, val)
                            # Для is_urgent — Да/Нет
                            if col == 'is_urgent' or (self.table_name == 'Client' and col == 'is_profi_client'):
                                val = 'Да' if val in (1, True, '1', 'TRUE', 'True') else 'Нет'
                            # null/None -> ''
                            if val is None or str(val).lower() == 'none':
                                val = ''
                            item = QTableWidgetItem(str(val))
                            # Если это PK — делаем ячейку read-only и сохраняем id в UserRole
                            if model and hasattr(model, '__table__'):
                                pk_cols = [c.name for c in model.__table__.primary_key.columns]
                                if col in pk_cols:
                                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                                    # Сохраняем id (или tuple PK) в UserRole
                                    if len(pk_cols) == 1:
                                        item.setData(Qt.UserRole, getattr(obj, col, None))
                                    else:
                                        # Для составного ключа сохраняем tuple
                                        item.setData(Qt.UserRole, tuple(getattr(obj, pk, None) for pk in pk_cols))
                            self.table.setItem(i, j, item)
                    self.table.resizeColumnsToContents()
                else:
                    self.table.setRowCount(0)
                    self.table.setColumnCount(0)
                return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def get_pk_value(self, row):
        # Для составных ключей возвращаем кортеж значений всех PK-колонок в правильном порядке и типе
        model = None
        if hasattr(self, 'columns') and self.table.rowCount() > 0:
            item = self.table.item(row, 0)
            if item:
                model = type(self.service.get_all()[0]) if hasattr(self.service, 'get_all') and self.service.get_all() else None
        if model and hasattr(model, '__table__'):
            pk_cols = [col.name for col in model.__table__.primary_key.columns]
            values = []
            for pk_col in pk_cols:
                if pk_col in self.columns:
                    idx = self.columns.index(pk_col)
                    item = self.table.item(row, idx)
                    val = item.text() if item else None
                    # Приведение к типу из модели
                    col_type = str(model.__table__.columns[pk_col].type)
                    try:
                        if val is not None:
                            if 'INTEGER' in col_type or 'INT' in col_type:
                                val = int(val)
                            elif 'FLOAT' in col_type or 'REAL' in col_type:
                                val = float(val)
                    except Exception:
                        QMessageBox.critical(self, "Ошибка", f"Некорректное значение ключа: {val} (ожидался тип {col_type})")
                        return None
                    values.append(val)
            if len(values) == 1:
                return values[0]
            return tuple(values)
        # Fallback: первый столбец
        item = self.table.item(row, 0)
        if item:
            return item.text()
        return None

    def get_fk_options(self, columns):
        # Карта: внешний ключ -> (имя сервиса, поле для отображения)
        fk_map = {
            'client_id':    ('Client', 'full_name'),
            'branch_id':    ('Branch', 'name'),
            'kiosk_id':     ('Kiosk', 'kiosk_name'),
            'product_id':   ('Product', 'name'),
            'supplier_id':  ('Supplier', 'name'),
            'category_id':  ('ProductCategory', 'name'),
            'service_code': ('ServiceType', 'description'),
            'workplace_id': ('Workplace', 'position'),
            'to_branch_id': ('Branch', 'name'),
            'to_kiosk_id':  ('Kiosk', 'kiosk_name'),
            'role_id': ('Role', 'name'),
            'permission_id': ('Permission', 'name'),
            'employee_id': ('Employee', 'full_name'),
        }
        fk_options = {}
        for col in columns:
            if col == 'workplace_id' and getattr(self, 'table_name', None) in ('Employee',):
                # Особое отображение для Employee.workplace_id
                service = WorkplaceService()
                items = service.get_all()
                options = []
                for w in items:
                    if getattr(w, 'branch_id', None):
                        branch = w.branch
                        branch_name = getattr(branch, 'name', '') if branch else ''
                        display = f"Филиал {branch_name} - {getattr(w, 'position', '')}"
                    elif getattr(w, 'kiosk_id', None):
                        kiosk = w.kiosk
                        kiosk_name = getattr(kiosk, 'kiosk_name', '') if kiosk else ''
                        display = f"Киоск {kiosk_name} - {getattr(w, 'position', '')}"
                    else:
                        display = getattr(w, 'position', '')
                    options.append((w.id, display))
                fk_options[col] = options
                continue
            if col in fk_map:
                service_name, display_field = fk_map[col]
                service = globals().get(f'{service_name}Service')
                if service is None:
                    continue
                service_obj = service()
                items = service_obj.get_all()
                options = [(getattr(item, 'id', getattr(item, col, None)), getattr(item, display_field, str(item))) for item in items]
                fk_options[col] = options
        return fk_options

    def add_record(self):
        if not self.service:
            return
        columns = getattr(self, 'columns', None)
        if not columns:
            self.load_data()
            columns = getattr(self, 'columns', None)
        model = None
        if hasattr(self.service, 'get_all') and self.service.get_all():
            model = type(self.service.get_all()[0])
        pk_columns = []
        if model and hasattr(model, '__table__'):
            pk_columns = [col.name for col in model.__table__.primary_key.columns]
        if self.table_name == 'Branch':
            insert_columns = [col for i, col in enumerate(columns) if i != 0 and col != 'office_id']
        elif self.table_name in ('UserRole', 'RolePermission', 'Sale', 'ServiceOrder', 'PrintDetail', 'ProfiDiscount', 'SupplierSpecialization'):
            insert_columns = columns  # для составных PK не скрываем PK
        else:
            insert_columns = [col for i, col in enumerate(columns) if not (i == 0 and (col.lower() == 'id' or col.endswith('_id')))]
        fk_options = self.get_fk_options(insert_columns)
        form = RecordForm(insert_columns, parent=self, pk_columns=pk_columns, fk_options=fk_options)
        # --- Добавляю переводимые лейблы ---
        table_key = self.table_name.strip('`')
        col_trans = COLUMN_TRANSLATIONS.get(table_key, {})
        for i, col in enumerate(insert_columns):
            label = col_trans.get(col, col)
            form.layout.labelForField(form.inputs[col]).setText(label)
        # --- END ---
        result = form.exec()
        if result == QDialog.Accepted:
            data = form.get_data()
            try:
                self.service.create(**dict(zip(insert_columns, data)))
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка добавления: {e}")

    def edit_record(self):
        if not self.service:
            return
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите строку для редактирования")
            return
        columns = getattr(self, 'columns', None)
        if not columns:
            self.load_data()
            columns = getattr(self, 'columns', None)
        model = None
        if hasattr(self.service, 'get_all') and self.service.get_all():
            model = type(self.service.get_all()[0])
        pk_columns = []
        if model and hasattr(model, '__table__'):
            pk_columns = [col.name for col in model.__table__.primary_key.columns]
        if self.table_name == 'Branch':
            edit_columns = [col for i, col in enumerate(columns) if i != 0 and col != 'office_id']
        elif self.table_name in ('UserRole', 'RolePermission', 'Sale', 'ServiceOrder', 'PrintDetail', 'ProfiDiscount', 'SupplierSpecialization'):
            edit_columns = columns  # для составных PK не скрываем PK
        else:
            edit_columns = columns[1:]
        fk_options = self.get_fk_options(edit_columns)
        # Получаем PK из UserRole
        pk_value = None
        if pk_columns:
            idx = self.columns.index(pk_columns[0])
            item = self.table.item(row, idx)
            if item:
                pk_value = item.data(Qt.UserRole)
        # Получаем ORM-объект по PK
        obj = None
        if pk_value is not None:
            if isinstance(pk_value, tuple):
                # Составной ключ
                filter_kwargs = dict(zip(pk_columns, pk_value))
                obj = self.service.get_all(filters=filter_kwargs)
                if obj:
                    obj = obj[0]
            else:
                obj = self.service.get_by_id(pk_value)
        # Формируем значения для формы строго по edit_columns
        values = []
        labels = []
        table_key = self.table_name.strip('`')
        col_trans = COLUMN_TRANSLATIONS.get(table_key, {})
        for col in edit_columns:
            if col in fk_options and obj is not None:
                val = getattr(obj, col, '')
                values.append(val)
            elif col in self.columns:
                idx = self.columns.index(col)
                item = self.table.item(row, idx)
                values.append(item.text() if item else '')
            else:
                values.append('')
            labels.append(col_trans.get(col, col))
        form = RecordForm(edit_columns, values, parent=self, pk_columns=pk_columns, fk_options=fk_options)
        # Устанавливаем красивые лейблы
        for i, label in enumerate(labels):
            form.layout.labelForField(form.inputs[edit_columns[i]]).setText(label)
        result = form.exec()
        if result == QDialog.Accepted:
            new_data = form.get_data()
            try:
                self.service.update(pk_value, **dict(zip(edit_columns, new_data)))
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования: {e}")

    def delete_record(self):
        if not self.service:
            return
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите строку для удаления")
            return
        # Получаем PK из UserRole (аналогично edit_record)
        columns = getattr(self, 'columns', None)
        if not columns:
            self.load_data()
            columns = getattr(self, 'columns', None)
        model = None
        if hasattr(self.service, 'get_all') and self.service.get_all():
            model = type(self.service.get_all()[0])
        pk_columns = []
        if model and hasattr(model, '__table__'):
            pk_columns = [col.name for col in model.__table__.primary_key.columns]
        pk_value = None
        if pk_columns:
            idx = self.columns.index(pk_columns[0])
            item = self.table.item(row, idx)
            if item:
                pk_value = item.data(Qt.UserRole)
        # Формируем строку только по видимым колонкам (не PK) с красивыми заголовками
        visible_strs = []
        table_key = self.table_name.strip('`')
        col_trans = COLUMN_TRANSLATIONS.get(table_key, {})
        for col in self.visible_columns:
            idx = self.columns.index(col)
            header = col_trans.get(col, col)
            val = self.table.item(row, idx).text() if self.table.item(row, idx) else ''
            visible_strs.append(f'{header}: {val}')
        visible_str = ', '.join(visible_strs)
        reply = QMessageBox.question(self, "Подтверждение", f"Удалить запись ({visible_str})?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.service.delete(pk_value)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_data()

    def change_page_size(self):
        self.current_page = 1
        self.load_data()

    def get_display_value(self, row, column):
        value = self.table.item(row, column).text()
        if self.table_name == 'Employee' and column == 'workplace_id':
            workplace = self.service.session.query(Workplace).get(value)
            if workplace:
                if getattr(workplace, 'branch_id', None):
                    branch = self.service.session.query(Branch).get(workplace.branch_id)
                    branch_name = getattr(branch, 'name', '') if branch else ''
                    return f"Филиал {branch_name} - {getattr(workplace, 'position', '')}"
                elif getattr(workplace, 'kiosk_id', None):
                    kiosk = self.service.session.query(Kiosk).get(workplace.kiosk_id)
                    kiosk_name = getattr(kiosk, 'name', '') if kiosk else ''
                    return f"Киоск {kiosk_name} - {getattr(workplace, 'position', '')}"
                else:
                    return getattr(workplace, 'position', '')
            return ''
        return value