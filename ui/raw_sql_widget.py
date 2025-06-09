from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QTableWidget, QTableWidgetItem
import mysql.connector
from config import DB_CONFIG
from PySide6.QtGui import QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QByteArray, Qt, QSize

class RawSQLWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        # SVG стрелка
        arrow_svg = '''<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 8L12 16L20 24" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
        self.back_btn = QPushButton()
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        svg_widget = QSvgWidget()
        svg_widget.load(QByteArray(arrow_svg.encode()))
        svg_widget.renderer().render(painter)
        painter.end()
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
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.back_btn)
        top_bar.addStretch(1)
        main_layout.addLayout(top_bar)
        self.query_edit = QTextEdit(self)
        self.query_edit.setPlaceholderText('Введите SQL-запрос...')
        main_layout.addWidget(self.query_edit)
        self.button_layout = QHBoxLayout()
        self.execute_btn = QPushButton('Выполнить')
        self.button_layout.addWidget(self.execute_btn)
        main_layout.addLayout(self.button_layout)
        self.result_label = QLabel(self)
        main_layout.addWidget(self.result_label)
        self.result_table = QTableWidget(self)
        main_layout.addWidget(self.result_table)
        self.execute_btn.clicked.connect(self.execute_query)

    def execute_query(self):
        query = self.query_edit.toPlainText().strip()
        if not query:
            self.result_label.setText('Введите SQL-запрос')
            return
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(query)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                self.result_table.setRowCount(len(rows))
                self.result_table.setColumnCount(len(columns))
                self.result_table.setHorizontalHeaderLabels(columns)
                for i, row in enumerate(rows):
                    for j, val in enumerate(row):
                        self.result_table.setItem(i, j, QTableWidgetItem(str(val)))
                self.result_label.setText(f'Результатов: {len(rows)}')
            else:
                conn.commit()
                self.result_table.setRowCount(0)
                self.result_table.setColumnCount(0)
                self.result_label.setText('Запрос выполнен успешно (без вывода)')
            cursor.close()
            conn.close()
        except Exception as e:
            self.result_label.setText(f'Ошибка: {e}')
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0) 