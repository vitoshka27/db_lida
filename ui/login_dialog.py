from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon

class FloatingLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet('font-size: 15px; color: #7bb0ff; padding-left: 2px;')
        self.setVisible(False)

class LoginScreen(QWidget):
    login_success = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('''
            QWidget {
                background: #181c24;
            }
        ''')
        # Горизонтальное центрирование
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        # Карточка
        card = QWidget()
        card.setFixedWidth(420)
        card.setStyleSheet('''
            QWidget {
                background: #23272e;
                border-radius: 18px;
            }
        ''')
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(32)
        # Заголовок
        title = QLabel("Добро пожаловать!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 32px; font-weight: bold; color: #7bb0ff; letter-spacing: 1px; margin-bottom: 8px;')
        card_layout.addWidget(title)
        # Логин
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Логин')
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet('''
            QLineEdit {
                font-size: 18px;
                padding: 8px 16px 8px 12px;
                border-radius: 8px;
                border: none;
                border-bottom: 2px solid #3a4256;
                background: #23272e;
                color: #e0e4ea;
                qproperty-alignment: AlignLeft;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #7bb0ff;
                background: #23272e;
            }
        ''')
        card_layout.addWidget(self.username_input)
        # Пароль
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet('''
            QLineEdit {
                font-size: 18px;
                padding: 8px 16px 8px 12px;
                border-radius: 8px;
                border: none;
                border-bottom: 2px solid #3a4256;
                background: #23272e;
                color: #e0e4ea;
                qproperty-alignment: AlignLeft;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #7bb0ff;
                background: #23272e;
            }
        ''')
        card_layout.addWidget(self.password_input)
        # Кнопка
        self.login_btn = QPushButton("Войти")
        self.login_btn.setMinimumHeight(44)
        self.login_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.login_btn.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f8cff, stop:1 #6ec6ff);
                color: #fff;
                border-radius: 10px;
                font-size: 20px;
                font-weight: bold;
                padding: 10px 0;
                margin-top: 18px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6ec6ff, stop:1 #4f8cff);
            }
        ''')
        self.login_btn.clicked.connect(self.try_login)
        card_layout.addWidget(self.login_btn)
        # Ошибка
        self.error_label = QLabel()
        self.error_label.setStyleSheet('color: #e53935; font-size: 16px; margin-top: 8px;')
        self.error_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.error_label)
        card_layout.addStretch(1)
        outer_layout.addStretch(1)
        outer_layout.addWidget(card, alignment=Qt.AlignCenter)
        outer_layout.addStretch(1)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            self.error_label.setText('Введите логин и пароль')
            return
        self.error_label.setText('')
        self.login_success.emit(username, password) 