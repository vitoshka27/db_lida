import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QComboBox, QStackedWidget, QWidget, QLabel, QVBoxLayout, QMessageBox, QDialog, QScrollArea, QDockWidget, QPushButton, QSizePolicy, QHBoxLayout, QFormLayout, QSpacerItem
)
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter
from PySide6.QtCore import Qt, QByteArray, QSize
from ui.table_widget import TableWidget
from ui.login_dialog import LoginScreen
import bcrypt
from ui.raw_sql_widget import RawSQLWidget
from ui.user_query_widget import UserQueryWidget
from services.entity_services import *
from services.role_service import RoleService
from services.auth_service import AuthService
from PySide6.QtSvgWidgets import QSvgWidget

print("main.py started")

TABLES = [
    ('MainOffice', 'Главный офис', '🏢'),
    ('Branch', 'Филиалы', '🏬'),
    ('Kiosk', 'Киоски', '🛒'),
    ('Client', 'Клиенты', '👤'),
    ('DiscountCard', 'Дисконтные карты', '💳'),
    ('ProfiDiscount', 'Профи-скидки', '⭐'),
    ('Supplier', 'Поставщики', '🚚'),
    ('ProductCategory', 'Категории товаров', '📦'),
    ('SupplierSpecialization', 'Специализация поставщиков', '🔗'),
    ('Product', 'Товары', '📷'),
    ('Supply', 'Поставки', '📦'),
    ('Distribution', 'Распределение', '🔄'),
    ('`Order`', 'Заказы', '📝'),
    ('FilmDevelopment', 'Проявка пленки', '🎞️'),
    ('PhotoPrint', 'Печать фото', '🖨️'),
    ('PrintDetail', 'Детали печати', '🔢'),
    ('Sale', 'Продажи', '💰'),
    ('ServiceType', 'Виды услуг', '🛠️'),
    ('ServiceOrder', 'Заказы на услуги', '🧾'),
    ('Workplace', 'Рабочие места', '👔'),
    ('Employee', 'Работники', '🧑‍💼'),
    ('Role', 'Роли', '🛡️'),
    ('Permission', 'Права', '🔑'),
    ('RolePermission', 'Права ролей', '🔗'),
    ('UserRole', 'Роли сотрудников', '👥'),
]

ROLE_TABLES = {
    'Администратор': [t[0] for t in TABLES],
    'Фотограф': ['`Order`', 'Client', 'PhotoPrint', 'FilmDevelopment'],
    'Реставратор': ['`Order`', 'Client', 'PhotoPrint', 'FilmDevelopment'],
    'Оператор киоска': ['`Order`', 'Sale', 'Client', 'PhotoPrint', 'FilmDevelopment']
}

COLUMN_TRANSLATIONS = {
    'full_name': 'ФИО',
    'hire_date': 'Дата найма',
    'phone': 'Телефон',
    'workplace_id': 'Рабочее место',
    'branch_id': 'Филиал',
    'kiosk_id': 'Киоск',
    'position': 'Должность',
    'duties': 'Обязанности',
    'Role': {
        'id': 'ID',
        'name': 'Название роли',
        'description': 'Описание',
    },
    'Permission': {
        'id': 'ID',
        'name': 'Название права',
        'description': 'Описание',
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

class ProfileScreen(QWidget):
    def __init__(self, user_info, parent=None, services=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #23272e, stop:1 #23272e);
            }
        ''')
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        # Верхняя панель с иконкой назад (SVG)
        top_bar = QHBoxLayout()
        arrow_svg = '''<svg width=\"32\" height=\"32\" viewBox=\"0 0 32 32\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><path d=\"M20 8L12 16L20 24\" stroke=\"white\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>'''
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_widget = QSvgWidget()
        svg_widget.load(QByteArray(arrow_svg.encode()))
        svg_widget.renderer().render(painter)
        painter.end()
        self.back_btn = QPushButton()
        self.back_btn.setIcon(QIcon(pixmap))
        self.back_btn.setIconSize(QSize(32, 32))
        self.back_btn.setFixedSize(40, 40)
        self.back_btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                border: none;
                margin: 0 8px 0 0;
            }
            QPushButton:hover {
                background: #e3f0ff;
                border-radius: 8px;
            }
        ''')
        top_bar.addWidget(self.back_btn)
        top_bar.addStretch(1)
        main_layout.addLayout(top_bar)
        # Заголовок
        title = QLabel("Профиль")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #4f8cff; letter-spacing: 1px; margin-bottom: 10px;')
        main_layout.addWidget(title)
        # Скроллируемая область на весь экран
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet('background: transparent;')
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        content_layout.setContentsMargins(60, 20, 60, 20)
        content_layout.setSpacing(18)
        # Формируем данные
        profile_data = []
        has_workplace_position = False
        for k, v in user_info.items():
            if k in ("id", "password_hash", "permissions", "login") or v is None:
                continue
            if k == "workplace_id" and services:
                workplace = services['Workplace'].get_by_id(v)
                if workplace:
                    profile_data.append((COLUMN_TRANSLATIONS.get('position', 'Должность'), getattr(workplace, 'position', '—')))
                    profile_data.append((COLUMN_TRANSLATIONS.get('duties', 'Обязанности'), getattr(workplace, 'duties', '—')))
                    has_workplace_position = True
                continue
            if k == "branch_id" and services:
                branch = services['Branch'].get_by_id(v)
                if branch:
                    profile_data.append((COLUMN_TRANSLATIONS.get('branch_id', 'Филиал'), getattr(branch, 'name', '—')))
                continue
            if k == "kiosk_id" and services:
                kiosk = services['Kiosk'].get_by_id(v)
                if kiosk:
                    profile_data.append((COLUMN_TRANSLATIONS.get('kiosk_id', 'Киоск'), getattr(kiosk, 'name', '—')))
                continue
            if k == "position" and has_workplace_position:
                continue
            label = COLUMN_TRANSLATIONS.get(k, k)
            profile_data.append((label, v))
        # Выводим данные: label сверху, value снизу, без карточки
        for label, value in profile_data:
            l = QLabel(label)
            l.setStyleSheet('font-size: 15px; color: #b6d0ff; margin-bottom: 2px;')
            v = QLabel(str(value))
            v.setStyleSheet('font-size: 19px; color: #fff; background: #23272e; border-radius: 7px; padding: 8px 18px;')
            content_layout.addWidget(l)
            content_layout.addWidget(v)
        content_layout.addStretch(1)
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.services = {
            'MainOffice': MainOfficeService(),
            'Branch': BranchService(),
            'Kiosk': KioskService(),
            'Client': ClientService(),
            'DiscountCard': DiscountCardService(),
            'ProfiDiscount': ProfiDiscountService(),
            'Supplier': SupplierService(),
            'ProductCategory': ProductCategoryService(),
            'SupplierSpecialization': SupplierSpecializationService(),
            'Product': ProductService(),
            'Supply': SupplyService(),
            'Distribution': DistributionService(),
            '`Order`': OrderService(),
            'FilmDevelopment': FilmDevelopmentService(),
            'PhotoPrint': PhotoPrintService(),
            'PrintDetail': PrintDetailService(),
            'Sale': SaleService(),
            'ServiceType': ServiceTypeService(),
            'ServiceOrder': ServiceOrderService(),
            'Workplace': WorkplaceService(),
            'Employee': EmployeeService(),
            'Role': RoleService(),
            'Permission': PermissionService(),
            'RolePermission': RolePermissionService(),
            'UserRole': UserRoleService(),
        }
        self.setWindowTitle("Фотоцентр")
        self.setGeometry(100, 100, 1200, 700)
        self.stacked = QStackedWidget()
        self.login_screen = LoginScreen()
        self.stacked.addWidget(self.login_screen)
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_layout.addWidget(self.stacked)
        self.setCentralWidget(self.central_widget)
        self.login_screen.login_success.connect(self.handle_login)
        self.user_info = None
        self.profile_screen = None
        self.main_ui_widget = None
        self.sql_widget = None
        self.raw_sql_widget = None
        self.user_query_widget = None

    def handle_login(self, username, password):
        try:
            auth_service = AuthService()
            user = auth_service.authenticate(username, password)
            if not user:
                self.login_screen.error_label.setText('Неверный логин или пароль')
                return
            role_service = RoleService()
            roles = role_service.get_user_roles(user['id'])
            permissions = set()
            for role in roles:
                perms = role_service.get_role_permissions(role.id)
                for p in perms:
                    permissions.add(p.name)
            user['permissions'] = list(permissions)
            self.user_info = user
            self.show_main_ui()
        except Exception as e:
            self.login_screen.error_label.setText(f'Ошибка: {e}')

    def show_main_ui(self):
        if self.main_ui_widget:
            self.stacked.removeWidget(self.main_ui_widget)
        self.main_ui_widget = QWidget()
        # Главный вертикальный layout
        main_layout = QVBoxLayout(self.main_ui_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Верхняя панель на всю ширину
        self.top_widget = QWidget()
        top_layout = QHBoxLayout(self.top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("Фотоцентр")
        title.setObjectName('mainTitle')
        title.setStyleSheet("padding: 18px 0 18px 24px; color: #fff; font-weight: bold; font-size: 32px; letter-spacing: 1px;")
        top_layout.addWidget(title)
        role = self.user_info.get('position', '—')
        role_label = QLabel(role)
        role_label.setStyleSheet("color: #e0e4ea; font-size: 18px; font-family: 'Segoe UI', 'Arial', sans-serif; font-style: italic; margin-left: 18px; margin-top: 18px;")
        top_layout.addWidget(role_label)
        top_layout.addStretch(1)
        self.raw_sql_widget = None
        self.user_query_widget = None
        if self.user_info.get('position', '').lower() == 'администратор' or self.user_info.get('login', '').startswith('admin'):
            self.raw_sql_widget = RawSQLWidget()
            self.sql_btn = QPushButton("📝 SQL")
            self.sql_btn.setStyleSheet('''
                QPushButton {
                    color: #111;
                    background: #fff;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    padding: 8px 18px;
                    margin: 8px 8px 8px 0;
                    border: 2px solid #4f8cff;
                }
                QPushButton:hover {
                    background: #e3f0ff;
                }
            ''')
            self.sql_btn.clicked.connect(self.show_sql)
            top_layout.addWidget(self.sql_btn)
            # Кнопка пользовательских запросов
            self.user_query_widget = UserQueryWidget(back_callback=self.back_from_user_queries)
            self.user_query_btn = QPushButton("📊 Пользовательские запросы")
            self.user_query_btn.setStyleSheet('''
                QPushButton {
                    color: #111;
                    background: #fff;
                    border-radius: 10px;
                    font-size: 16px;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    padding: 8px 18px;
                    margin: 8px 8px 8px 0;
                    border: 2px solid #4f8cff;
                }
                QPushButton:hover {
                    background: #e3f0ff;
                }
            ''')
            self.user_query_btn.clicked.connect(self.show_user_queries)
            top_layout.addWidget(self.user_query_btn)
        # Кнопка профиля — иконка (generic user, не совпадает с меню сотрудников)
        user_svg = '''<svg width=\"32\" height=\"32\" viewBox=\"0 0 32 32\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"16\" cy=\"12\" r=\"6\" stroke=\"white\" stroke-width=\"2.5\"/><path d=\"M6 26c0-4 4.5-6 10-6s10 2 10 6\" stroke=\"white\" stroke-width=\"2.5\" stroke-linecap=\"round\"/></svg>'''
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_widget = QSvgWidget()
        svg_widget.load(QByteArray(user_svg.encode()))
        svg_widget.renderer().render(painter)
        painter.end()
        self.profile_btn = QPushButton()
        self.profile_btn.setIcon(QIcon(pixmap))
        self.profile_btn.setIconSize(QSize(32, 32))
        self.profile_btn.setStyleSheet('''
            QPushButton {
                background: #4f8cff;
                border-radius: 10px;
                padding: 8px;
                margin: 8px 18px 8px 0;
                border: none;
            }
            QPushButton:hover {
                background: #6ec6ff;
            }
        ''')
        self.profile_btn.clicked.connect(self.show_profile)
        top_layout.addWidget(self.profile_btn)
        self.top_widget.setFixedHeight(80)
        main_layout.addWidget(self.top_widget)
        # Центральная область — QStackedWidget для TableWidget, SQL и профиля
        self.central_stack = QStackedWidget()
        self.table_widgets = {}
        for table_key in TABLES:
            service = self.services.get(table_key[0])
            widget = TableWidget(table_key[0], self.user_info, service=service)
            self.table_widgets[table_key[0]] = widget
            self.central_stack.addWidget(widget)
        if self.raw_sql_widget:
            self.central_stack.addWidget(self.raw_sql_widget)
        main_layout.addWidget(self.central_stack)
        self.stacked.addWidget(self.main_ui_widget)
        self.stacked.setCurrentWidget(self.main_ui_widget)
        self.central_stack.setCurrentIndex(0)
        # Меню слева как dock
        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout(self.menu_widget)
        menu_layout.setContentsMargins(0, 24, 0, 24)
        menu_layout.setSpacing(6)
        self.menu_buttons = {}
        for idx, table in enumerate(TABLES):
            key, name, icon = table
            btn = QPushButton(f"{icon}  {name}")
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(44)
            btn.setStyleSheet('''
                QPushButton {
                    color: #fff;
                    background: transparent;
                    border: none;
                    border-radius: 12px;
                    font-size: 20px;
                    font-family: 'Segoe UI', 'Arial', sans-serif;
                    padding: 8px 32px 8px 28px;
                    text-align: left;
                }
                QPushButton:hover, QPushButton:checked {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f8cff, stop:1 #6ec6ff);
                    color: #fff;
                }
            ''')
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, i=idx: self.switch_table(i))
            menu_layout.addWidget(btn)
            self.menu_buttons[key] = btn
        menu_layout.addStretch(1)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setWidget(self.menu_widget)
        self.dock = QDockWidget()
        self.dock.setTitleBarWidget(QWidget())
        self.dock.setWidget(scroll)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock.setMinimumWidth(340)
        self.dock.setMaximumWidth(400)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        # Выделяем первую таблицу в меню
        first_key = TABLES[0][0]
        self.menu_buttons[first_key].setChecked(True)

    def switch_table(self, idx):
        self.central_stack.setCurrentIndex(idx)
        for i, table_key in enumerate([t[0] for t in TABLES]):
            self.menu_buttons[table_key].setChecked(i == idx)
        # Показываем меню если вдруг оно было скрыто
        self.dock.show()

    def show_profile(self):
        if self.profile_screen:
            self.central_stack.removeWidget(self.profile_screen)
        self.profile_screen = ProfileScreen(self.user_info, services=self.services)
        self.profile_screen.back_btn.clicked.connect(self.back_from_profile)
        self.central_stack.addWidget(self.profile_screen)
        self.central_stack.setCurrentWidget(self.profile_screen)
        self.dock.hide()
        for btn in self.menu_buttons.values():
            btn.setChecked(False)

    def back_from_profile(self):
        self.central_stack.setCurrentIndex(0)
        self.dock.show()
        # Выделяем первую таблицу (или ту, что была до профиля)
        self.menu_buttons[TABLES[0][0]].setChecked(True)

    def show_sql(self):
        if self.raw_sql_widget:
            self.central_stack.setCurrentWidget(self.raw_sql_widget)
            self.dock.hide()
            for btn in self.menu_buttons.values():
                btn.setChecked(False)
            # Безопасно отключаем сигнал, чтобы не было RuntimeWarning
            try:
                self.raw_sql_widget.back_btn.clicked.disconnect()
            except Exception:
                pass
            self.raw_sql_widget.back_btn.clicked.connect(self.back_from_sql)

    def back_from_sql(self):
        self.central_stack.setCurrentIndex(0)
        self.dock.show()
        # Выделяем первую таблицу (или ту, что была до SQL)
        self.menu_buttons[TABLES[0][0]].setChecked(True)

    def show_user_queries(self):
        if self.user_query_widget:
            if self.central_stack.indexOf(self.user_query_widget) == -1:
                self.central_stack.addWidget(self.user_query_widget)
            self.central_stack.setCurrentWidget(self.user_query_widget)
            self.dock.hide()
            # Кнопка назад
            # ...

    def back_from_user_queries(self):
        self.central_stack.setCurrentIndex(0)
        self.dock.show()

    def logout(self):
        self.user_info = None
        self.stacked.setCurrentWidget(self.login_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 