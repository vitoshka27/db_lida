from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QFormLayout, QSizePolicy, QComboBox, QDateEdit, QScrollArea
import mysql.connector
from config import DB_CONFIG
import os
import re
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QDate
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvgWidgets import QSvgWidget
from ui.query_filters import (
    QueryFilterSorter,
    Script1FilterSorter, Script2FilterSorter, Script3FilterSorter, Script4FilterSorter, Script5FilterSorter,
    Script6FilterSorter, Script7FilterSorter, Script8FilterSorter, Script9FilterSorter, Script10FilterSorter,
    Script11FilterSorter, Script12FilterSorter
)

class UserQueryWidget(QWidget):
    def __init__(self, scripts_dir='scripts/requests', parent=None, back_callback=None):
        super().__init__(parent)
        self.scripts_dir = scripts_dir
        self.scripts = self.load_scripts()
        self.current_script = None
        self.current_filters = []
        self.back_callback = back_callback
        self.filter_panel = None
        self.filter_panel_anim = None
        self.filter_panel_open = False
        # Главный горизонтальный layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Меню запросов слева (без отдельного sidebar)
        self.menu_widget = QWidget()
        self.menu_widget.setFixedWidth(400)
        self.menu_widget.setStyleSheet('background: #181c24; border-right: 2px solid #23272e;')
        menu_layout = QVBoxLayout(self.menu_widget)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        # Кнопка назад (стрелка)
        arrow_svg = '''<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 8L12 16L20 24" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_widget = QSvgWidget()
        svg_widget.load(bytearray(arrow_svg, encoding='utf-8'))
        svg_widget.renderer().render(painter)
        painter.end()
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon(pixmap))
        self.back_btn.setIconSize(pixmap.size())
        self.back_btn.setFixedSize(40, 40)
        self.back_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                border: none;
                margin: 16px 0 0 12px;
            }
            QPushButton:hover {
                background: #e3f0ff;
                border-radius: 8px;
            }
        ''')
        self.back_btn.clicked.connect(self.on_back)
        menu_layout.addWidget(self.back_btn, alignment=Qt.AlignLeft)
        # Заголовок меню
        title = QLabel('Пользовательские запросы')
        title.setStyleSheet('font-size: 19px; color: #7bb0ff; font-weight: bold; padding: 12px 0 18px 24px;')
        menu_layout.addWidget(title)
        self.menu_buttons = []
        for idx, script in enumerate(self.scripts):
            btn = QPushButton(f"{idx+1}. {script['title']}")
            btn.setCheckable(True)
            btn.setStyleSheet('''
                QPushButton {
                    background: transparent;
                    color: #e0e4ea;
                    font-size: 16px;
                    text-align: left;
                    padding: 10px 0 10px 32px;
                    border: none;
                }
                QPushButton:checked {
                    background: #23272e;
                    color: #7bb0ff;
                    border-left: 4px solid #4f8cff;
                }
                QPushButton:hover {
                    background: #23272e;
                    color: #7bb0ff;
                }
            ''')
            btn.clicked.connect(lambda checked, i=idx: self.on_script_change(i))
            menu_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        menu_layout.addStretch(1)
        main_layout.addWidget(self.menu_widget)
        # Правая часть — фильтры, кнопка, таблица
        right = QVBoxLayout()
        right.setContentsMargins(32, 32, 32, 32)
        right.setSpacing(18)
        # --- Кнопки фильтрации и сортировки ---
        top_btns = QHBoxLayout()
        self.sort_btn = QPushButton('')
        self.sort_btn.setFixedHeight(36)
        self.sort_btn.setStyleSheet('font-size: 16px; border-radius: 8px; background: #23272e; color: #7bb0ff; font-weight: bold;')
        self.sort_btn.clicked.connect(self.open_sort_menu)
        self.sort_dir_btn = QPushButton('⮟')
        self.sort_dir_btn.setFixedHeight(36)
        self.sort_dir_btn.setFixedWidth(36)
        self.sort_dir_btn.setStyleSheet('font-size: 18px; border-radius: 8px; background: #23272e; color: #7bb0ff; font-weight: bold;')
        self.sort_dir_btn.clicked.connect(self.toggle_sort_direction)
        self.filter_btn = QPushButton('Фильтры')
        self.filter_btn.setFixedHeight(36)
        self.filter_btn.setStyleSheet('font-size: 16px; border-radius: 8px; background: #23272e; color: #7bb0ff; font-weight: bold;')
        self.filter_btn.clicked.connect(self.toggle_filter_panel)
        top_btns.addWidget(self.sort_btn)
        top_btns.addWidget(self.sort_dir_btn)
        top_btns.addWidget(self.filter_btn)
        top_btns.addStretch(1)
        right.addLayout(top_btns)
        # --- END ---
        self.result_label = QLabel(self)
        right.addWidget(self.result_label)
        self.result_table = QTableWidget(self)
        self.result_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right.addWidget(self.result_table)
        self.result_table.verticalHeader().setDefaultSectionSize(38)
        self.result_table.setStyleSheet('''
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
        main_layout.addLayout(right)
        # --- Состояния фильтра и сортировки ---
        self.active_filters = {}
        self.sort_column = None
        self.sort_asc = True
        # Инициализация
        if self.scripts:
            self.on_script_change(0)

    def on_back(self):
        if self.back_callback:
            self.back_callback()

    def load_scripts(self):
        scripts = []
        # Маппинг: имя файла -> красивое название
        script_titles = {
            'script1.sql':  'Пункты приёма заказов (1)',
            'script2.sql':  'Заказы на фотоработы за период (2)',
            'script3.sql':  'Число простых и срочных заказов (3)',
            'script4.sql':  'Выручка по видам работ (4)',
            'script5.sql':  'Количество отпечатанных фотографий (5)',
            'script6.sql':  'Количество проявленных плёнок (6)',
            'script7.sql':  'Поставщики и их поставки за период (7)',
            'script8.sql':  'Клиенты по объёму заказов и скидкам (8)',
            'script9.sql':  'Выручка от фототоваров за период (9)',
            'script10.sql': 'Самые популярные товары и бренды (10)',
            'script11.sql': 'Объёмы продаж товаров за период (11)',
            'script12.sql': 'Список рабочих мест по профилю (12)',
        }
        # Сортируем по номеру в скобках
        def script_sort_key(fname):
            title = script_titles.get(fname, fname)
            import re
            m = re.search(r'\((\d+)\)', title)
            return int(m.group(1)) if m else 999
        for fname in sorted(os.listdir(self.scripts_dir), key=script_sort_key):
            if fname.endswith('.sql'):
                path = os.path.join(self.scripts_dir, fname)
                with open(path, encoding='utf-8') as f:
                    sql = f.read()
                # Название по маппингу или имени файла
                title = script_titles.get(fname, fname)
                # Фильтры — строки вида -- AND ...
                filters = []
                for line in sql.splitlines():
                    line = line.strip()
                    if line.startswith('-- AND') or line.startswith('--AND'):
                        filters.append(line[2:].strip())
                scripts.append({'title': title, 'filename': fname, 'sql': sql, 'filters': filters})
        return scripts

    def on_script_change(self, idx):
        self.current_script = self.scripts[idx]
        # Меню: выделяем активную кнопку
        for i, btn in enumerate(self.menu_buttons):
            btn.setChecked(i == idx)
        # Очищаем старые фильтры
        self.active_filters = {}
        self.result_label.setText('')
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)
        # Сброс сортировки при смене скрипта
        self.sort_column = None
        self.sort_asc = True
        # Пересоздаём фильтр-панель под новый скрипт
        if self.filter_panel:
            self.filter_panel.deleteLater()
            self.filter_panel = None
        self.create_filter_panel()
        self.execute_query()

    def build_query(self):
        # Определяем номер скрипта по имени файла
        script_name = self.current_script['filename']
        script_num = None
        m = re.match(r'script(\d+)\\.sql', script_name)
        if not m:
            m = re.match(r'script(\d+)\.sql', script_name)
        if m:
            script_num = int(m.group(1))
        # Выбираем нужный класс
        filter_sorter_cls = {
            1: Script1FilterSorter,
            2: Script2FilterSorter,
            3: Script3FilterSorter,
            4: Script4FilterSorter,
            5: Script5FilterSorter,
            6: Script6FilterSorter,
            7: Script7FilterSorter,
            8: Script8FilterSorter,
            9: Script9FilterSorter,
            10: Script10FilterSorter,
            11: Script11FilterSorter,
            12: Script12FilterSorter,
        }.get(script_num, QueryFilterSorter)
        sorter = filter_sorter_cls(
            self.current_script['sql'],
            self.active_filters,
            self.sort_column,
            self.sort_asc
        )
        return sorter.build_query()

    def execute_query(self):
        query = self.build_query()
        print("[execute_query] Выполняю запрос:", query)
        if not query:
            self.result_label.setText('Выберите запрос')
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(query)
            # --- FORCE FULL TABLE RESET ---
            self.result_table.clear()
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                print(f"[execute_query] Получено строк: {len(rows)}, колонки: {columns}")
                self.result_table.setRowCount(len(rows))
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                for i, row in enumerate(rows):
                    for j, val in enumerate(row):
                        self.result_table.setItem(i, j, QTableWidgetItem(str(val)))
                self.result_table.resizeColumnsToContents()
                if columns:
                    if self.sort_column is None:
                        self.sort_column = columns[0]
                    self.sort_btn.setText(self.sort_column)
                self.result_label.setText(f'Результатов: {len(rows)}')
            else:
                conn.commit()
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
                self.result_label.setText('Запрос выполнен успешно (без вывода)')
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[execute_query] Ошибка: {e}")
            self.result_label.setText(f'Ошибка: {e}')
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
        # --- FORCED UI REFRESH ---
        self.result_table.repaint()
        self.result_table.viewport().update()
        print('[execute_query] Таблица UI обновлена после сортировки/запроса')

    def toggle_filter_panel(self):
        if not self.filter_panel:
            self.create_filter_panel()
        if self.filter_panel_open:
            self.animate_filter_panel(opening=False)
        else:
            self.animate_filter_panel(opening=True)

    def create_filter_panel(self):
        from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QDateEdit, QScrollArea, QWidget
        from PySide6.QtCore import QDate, Qt
        self.filter_panel = QWidget(self)
        self.filter_panel.setFixedWidth(340)
        self.filter_panel.setStyleSheet('''
            QWidget {
                background: #fff;
                border-top-left-radius: 24px;
                border-bottom-left-radius: 24px;
                border: 2px solid #e0e4ea;
                border-right: none;
            }
        ''')
        self.filter_panel.move(self.width(), 0)
        self.filter_panel.setGeometry(self.width(), 0, 340, self.height())
        self.filter_panel.setParent(self)
        self.filter_panel.raise_()

        # --- SCROLL AREA ---
        scroll_area = QScrollArea(self.filter_panel)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet('''
            QScrollArea, QScrollArea > QWidget, QScrollArea > QAbstractScrollArea, QScrollArea > QAbstractScrollArea > QWidget, QScrollArea > QAbstractScrollArea > QViewport, QScrollArea > QViewport {
                background: transparent;
                border: none;
            }
        ''')
        scroll_content = QWidget()
        scroll_content.setStyleSheet('background: transparent;')
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(18)
        scroll_area.setWidget(scroll_content)
        # --- Layout для всей панели ---
        panel_layout = QVBoxLayout(self.filter_panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(0)
        panel_layout.addWidget(scroll_area)

        title = QLabel('Фильтры')
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #23272e; margin-bottom: 18px; border: none; background: none;')
        layout.addWidget(title)
        self.filter_panel_widgets = {}
        label_map = {
            'type': 'Тип точки',
            'name': 'Название',
            'point_name': 'Название точки',
            'branch_id': 'Филиал',
            'kiosk_id': 'Киоск',
            'category_id': 'Категория',
            'position': 'Должность',
            'order_type': 'Тип заказа',
            'is_urgent': 'Срочный',
            'date_from': 'Дата с',
            'date_to': 'Дата по',
            'is_profi': 'Профи-клиент',
            'qty_from': 'Мин. количество',
            'qty_to': 'Макс. количество',
            'vol_from': 'Мин. объем',
            'vol_to': 'Макс. объем',
        }
        # --- Уникальные фильтры для каждого скрипта ---
        script_filters_map = {
            1: ['type', 'branch_id', 'kiosk_id'],
            2: ['type', 'branch_id', 'kiosk_id', 'date_from', 'date_to'],
            3: ['branch_id', 'kiosk_id', 'order_type', 'is_urgent', 'date_from', 'date_to'],
            4: ['branch_id', 'kiosk_id', 'order_type', 'is_urgent', 'date_from', 'date_to'],
            5: ['branch_id', 'kiosk_id', 'is_urgent', 'date_from', 'date_to'],
            6: ['branch_id', 'kiosk_id', 'is_urgent', 'date_from', 'date_to'],
            7: ['category_id', 'date_from', 'date_to', 'qty_from', 'qty_to'],
            8: ['branch_id', 'is_profi', 'vol_from', 'vol_to'],
            9: ['branch_id', 'kiosk_id', 'date_from', 'date_to'],
            10: ['branch_id'],
            11: ['branch_id', 'date_from', 'date_to'],
            12: ['position'],
        }
        script_name = self.current_script['filename']
        script_num = None
        m = re.match(r'script(\d+)\.sql', script_name)
        if not m:
            m = re.match(r'script(\d+).sql', script_name)
        if m:
            script_num = int(m.group(1))
        filter_keys = script_filters_map.get(script_num, [])
        for key in filter_keys:
            label = label_map.get(key, key.replace('_id', '').replace('_', ' ').capitalize())
            if key == 'type':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                cb.addItem('Филиал', 'Филиал')
                cb.addItem('Киоск', 'Киоск')
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif key == 'branch_id':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                from services.entity_services import BranchService
                for b in BranchService().get_all():
                    cb.addItem(getattr(b, 'name', str(b)), getattr(b, 'id', ''))
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif key == 'kiosk_id':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                from services.entity_services import KioskService
                for k in KioskService().get_all():
                    cb.addItem(getattr(k, 'kiosk_name', str(k)), getattr(k, 'id', ''))
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif key == 'category_id':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                try:
                    from services.entity_services import ProductCategoryService
                    for c in ProductCategoryService().get_all():
                        cb.addItem(getattr(c, 'name', str(c)), getattr(c, 'id', ''))
                except Exception:
                    pass
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif key == 'position':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                try:
                    from services.entity_services import WorkplaceService
                    positions = set(w.position for w in WorkplaceService().get_all())
                    for pos in sorted(positions):
                        cb.addItem(pos, pos)
                except Exception:
                    cb.addItem('Администратор', 'Администратор')
                    cb.addItem('Фотограф', 'Фотограф')
                    cb.addItem('Реставратор', 'Реставратор')
                    cb.addItem('Оператор киоска', 'Оператор киоска')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif key == 'order_type':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                cb.addItem('Проявка', 'film')
                cb.addItem('Печать', 'print')
                cb.addItem('Проявка + Печать', 'both')
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif key == 'is_urgent':
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                cb.addItem('Да', '1')
                cb.addItem('Нет', '0')
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            elif 'date' in key:
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                date_edit = QLineEdit()
                date_edit.setPlaceholderText('yyyy-MM-dd')
                date_edit.setInputMask('0000-00-00;_')
                date_edit.setStyleSheet('color: #23272e; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; font-size: 18px;')
                layout.addWidget(date_edit)
                self.filter_panel_widgets[key] = date_edit
            elif key in ('is_profi',):
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                cb = QComboBox()
                cb.addItem('Не выбрано', '')
                cb.addItem('Да', '1')
                cb.addItem('Нет', '0')
                cb.setStyleSheet('font-size: 18px; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; color: #23272e;')
                layout.addWidget(cb)
                self.filter_panel_widgets[key] = cb
            else:
                lbl = QLabel(label)
                lbl.setStyleSheet('font-size: 17px; color: #23272e; font-weight: 600; margin-bottom: 4px; border: none; background: none;')
                layout.addWidget(lbl)
                le = QLineEdit()
                le.setStyleSheet('color: #23272e; background: #f5f7fa; border-radius: 16px; padding: 10px 18px; border: 2px solid #e0e4ea; font-size: 18px;')
                layout.addWidget(le)
                self.filter_panel_widgets[key] = le
        btn_apply = QPushButton('Применить')
        btn_apply.setStyleSheet('font-size: 22px; background: #4f8cff; color: #fff; border-radius: 18px; padding: 18px 0; font-weight: bold; margin-top: 18px;')
        btn_apply.clicked.connect(self.apply_filter_panel)
        btn_reset = QPushButton('Сбросить фильтры')
        btn_reset.setStyleSheet('font-size: 18px; background: #e0e4ea; color: #23272e; border-radius: 16px; padding: 14px 0; font-weight: bold; margin-top: 10px;')
        btn_reset.clicked.connect(self.reset_filter_panel)
        layout.addWidget(btn_apply)
        layout.addWidget(btn_reset)
        layout.addStretch(1)
        self.filter_panel.show()

    def animate_filter_panel(self, opening=True):
        if not self.filter_panel:
            return
        start_x = self.width() if opening else self.width() - self.filter_panel.width()
        end_x = self.width() - self.filter_panel.width() if opening else self.width()
        self.filter_panel_anim = QPropertyAnimation(self.filter_panel, b'geometry')
        self.filter_panel_anim.setDuration(180)
        self.filter_panel_anim.setStartValue(QRect(start_x, 0, self.filter_panel.width(), self.height()))
        self.filter_panel_anim.setEndValue(QRect(end_x, 0, self.filter_panel.width(), self.height()))
        self.filter_panel_anim.start()
        self.filter_panel_open = opening

    def apply_filter_panel(self):
        print("[apply_filter_panel] Применяю фильтры...")
        for key, widget in self.filter_panel_widgets.items():
            if isinstance(widget, QComboBox):
                val = widget.currentData()
                if val:
                    self.active_filters[key] = val
                else:
                    self.active_filters[key] = ''
            elif 'date' in key:
                val = widget.text().strip()
                # Применяем фильтр только если поле не пустое и формат yyyy-MM-dd
                import re
                if val and re.match(r'^\d{4}-\d{2}-\d{2}$', val):
                    self.active_filters[key] = val
                else:
                    self.active_filters[key] = ''
            elif hasattr(widget, 'text'):
                self.active_filters[key] = widget.text()
            else:
                self.active_filters[key] = ''
        print("[apply_filter_panel] Новые фильтры:", self.active_filters)
        self.animate_filter_panel(opening=False)
        self.execute_query()

    def reset_filter_panel(self):
        print("[reset_filter_panel] Сброс фильтров...")
        for key, widget in self.filter_panel_widgets.items():
            if isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)
            elif 'date' in key:
                widget.clear()
            elif hasattr(widget, 'clear'):
                widget.clear()
            self.active_filters[key] = ''
        print("[reset_filter_panel] После сброса:", self.active_filters)
        self.animate_filter_panel(opening=False)
        self.execute_query()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.filter_panel:
            if self.filter_panel_open:
                self.filter_panel.setGeometry(self.width() - self.filter_panel.width(), 0, self.filter_panel.width(), self.height())
            else:
                self.filter_panel.setGeometry(self.width(), 0, self.filter_panel.width(), self.height())

    def open_filter_dialog(self):
        self.toggle_filter_panel()

    def open_sort_menu(self):
        print("[open_sort_menu] Открываю меню сортировки")
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        columns = []
        if self.result_table.columnCount() > 0:
            columns = [self.result_table.horizontalHeaderItem(i).text() for i in range(self.result_table.columnCount())]
        print("[open_sort_menu] Доступные колонки:", columns)
        for col in columns:
            action = menu.addAction(col)
            action.setCheckable(True)
            action.setChecked(col == self.sort_column)
            action.triggered.connect(lambda checked, c=col: self.set_sort_column(c))
        menu.exec(self.sort_btn.mapToGlobal(self.sort_btn.rect().bottomLeft()))

    def set_sort_column(self, col):
        print(f'[set_sort_column] Было: self.sort_column={self.sort_column}, self.sort_asc={self.sort_asc}')
        if self.sort_column == col:
            # Если выбрана та же колонка, просто меняем направление
            self.sort_asc = not self.sort_asc
            self.sort_dir_btn.setText('⮟' if self.sort_asc else '⮝')
        else:
            self.sort_column = col
            self.sort_btn.setText(col)
            self.sort_asc = True
            self.sort_dir_btn.setText('⮟')
        self.execute_query()
        print(f'[set_sort_column] Стало: self.sort_column={self.sort_column}, self.sort_asc={self.sort_asc}')

    def toggle_sort_direction(self):
        print(f'[toggle_sort_direction] Было: self.sort_column={self.sort_column}, self.sort_asc={self.sort_asc}')
        self.sort_asc = not self.sort_asc
        self.sort_dir_btn.setText('⮟' if self.sort_asc else '⮝')
        self.execute_query()
        print(f'[toggle_sort_direction] Стало: self.sort_column={self.sort_column}, self.sort_asc={self.sort_asc}')
 