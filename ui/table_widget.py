from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QPushButton, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QLabel, QSpinBox
from PySide6.QtGui import QColor
from ui.record_form import RecordForm

COLUMN_TRANSLATIONS = {
    'MainOffice': {
        'address': 'Адрес',
        'phone': 'Телефон',
        'manager_name': 'Менеджер',
        'workplace_count_for_branch': 'Раб. мест (филиал)',
        'workplace_count_for_kiosk': 'Раб. мест (киоск)',
    },
    'Branch': {
        'office_id': 'ID офиса',
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
        self.table.setStyleSheet('''
            QTableWidget {
                background: #fff;
                border-radius: 18px;
                border: 2px solid #e0e4ea;
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                selection-background-color: #e3f0ff;
                selection-color: #23272e;
                gridline-color: #e0e4ea;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f8cff, stop:1 #6ec6ff);
                color: #fff;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-top-left-radius: 18px;
                border-top-right-radius: 18px;
                padding: 8px 0;
            }
            QTableWidget::item {
                color: #23272e;
                background: #fff;
                border-bottom: 1.5px solid #e0e4ea;
                padding: 6px 8px;
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
                rows, total = self.service.get_page(page, page_size, filters=filters)
                self.total_pages = max(1, (total + page_size - 1) // page_size)
                self.page_label.setText(f"Страница {self.current_page} из {self.total_pages} (всего: {total})")
                if rows:
                    model = type(rows[0])
                    all_columns = list(model.__table__.columns.keys())
                    hidden_cols = {'id', '_sa_instance_state'}
                    if self.table_name == 'Branch':
                        hidden_cols.add('office_id')
                    columns = [col for col in all_columns if col not in hidden_cols]
                    self.columns = all_columns
                    self.visible_columns = columns
                    table_key = self.table_name.strip('`')
                    col_trans = COLUMN_TRANSLATIONS.get(table_key, {})
                    header_labels = [col_trans.get(col, col) for col in columns]
                    self.table.setRowCount(len(rows))
                    self.table.setColumnCount(len(columns))
                    self.table.setHorizontalHeaderLabels(header_labels)
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
                            self.table.setItem(i, j, QTableWidgetItem(str(val)))
                    self.table.resizeColumnsToContents()
                else:
                    self.table.setRowCount(0)
                    self.table.setColumnCount(0)
                return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def add_record(self):
        if not self.service:
            return
        columns = getattr(self, 'columns', None)
        if not columns:
            self.load_data()
            columns = getattr(self, 'columns', None)
        if self.table_name == 'Branch':
            insert_columns = [col for i, col in enumerate(columns) if i != 0 and col != 'office_id']
        else:
            insert_columns = [col for i, col in enumerate(columns) if not (i == 0 and (col.lower() == 'id' or col.endswith('_id')))]
        form = RecordForm(insert_columns, parent=self)
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
        values = [self.table.item(row, col).text() if self.table.item(row, col) else '' for col in range(self.table.columnCount())]
        pk_value = self.get_pk_value(row)
        if self.table_name == 'Branch':
            edit_columns = [col for i, col in enumerate(columns) if i != 0 and col != 'office_id']
        else:
            edit_columns = columns[1:]
        form = RecordForm(edit_columns, values, parent=self)
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
        pk_value = self.get_pk_value(row)
        visible_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
        visible_str = ', '.join(f'{col}: {val}' for col, val in zip(self.visible_columns, visible_data))
        reply = QMessageBox.question(self, "Подтверждение", f"Удалить запись ({visible_str})?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.service.delete(pk_value)
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {e}")

    def get_pk_value(self, row):
        # Предполагаем, что первый столбец — это PK (id)
        item = self.table.item(row, 0)
        if item:
            return item.text()
        return None

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