from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox

class RecordForm(QDialog):
    def __init__(self, columns, values=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование записи" if values else "Добавление записи")
        self.layout = QFormLayout(self)
        self.inputs = {}
        for i, col in enumerate(columns):
            if i == 0 and (col.lower() == 'id' or col.endswith('_id')):
                if values:
                    le = QLineEdit(self)
                    le.setText(str(values[i]))
                    le.setReadOnly(True)
                    le.setStyleSheet('''
                        QLineEdit {
                            color: #23272e;
                            background: #fff;
                            border: 1.5px solid #e0e4ea;
                            border-radius: 8px;
                            padding: 6px 10px;
                            font-size: 16px;
                            font-family: "Segoe UI", "Arial", sans-serif;
                            selection-background-color: #e3f0ff;
                            selection-color: #23272e;
                            caret-color: #23272e;
                        }
                    ''')
                    self.layout.addRow(col, le)
                    self.inputs[col] = le
                continue  # не добавлять поле id для добавления
            le = QLineEdit(self)
            le.setStyleSheet('''
                QLineEdit {
                    color: #23272e;
                    background: #fff;
                    border: 1.5px solid #e0e4ea;
                    border-radius: 8px;
                    padding: 6px 10px;
                    font-size: 16px;
                    font-family: "Segoe UI", "Arial", sans-serif;
                    selection-background-color: #e3f0ff;
                    selection-color: #23272e;
                    caret-color: #23272e;
                }
            ''')
            if values:
                le.setText(str(values[i]))
            self.layout.addRow(col, le)
            self.inputs[col] = le
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_data(self):
        return [self.inputs[col].text() for col in self.inputs] 