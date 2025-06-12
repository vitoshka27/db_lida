from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox

class RecordForm(QDialog):
    def __init__(self, columns, values=None, parent=None, pk_columns=None, fk_options=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование записи" if values else "Добавление записи")
        self.layout = QFormLayout(self)
        self.inputs = {}
        self.pk_columns = pk_columns or []
        self.fk_options = fk_options or {}
        for i, col in enumerate(columns):
            # --- FK: если есть опции, используем QComboBox ---
            if col in self.fk_options:
                cb = QComboBox(self)
                options = self.fk_options[col]
                for id_val, display in options:
                    cb.addItem(str(display), id_val)
                if values:
                    # выставить по id
                    id_val = values[i]
                    idx = next((j for j, (idv, _) in enumerate(options) if str(idv) == str(id_val)), -1)
                    if idx >= 0:
                        cb.setCurrentIndex(idx)
                self.layout.addRow(col, cb)
                self.inputs[col] = cb
                continue
            # --- PK: только для чтения, если это обычный id (не FK) ---
            if (col.lower() == 'id' or col in (self.pk_columns or [])) and (col not in self.fk_options):
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
                }
            ''')
            if values:
                le.setText(str(values[i]))
            # PK поля только для чтения при редактировании
            if values and col in self.pk_columns:
                le.setReadOnly(True)
                le.setStyleSheet('background: #eee; color: #888;')
            self.layout.addRow(col, le)
            self.inputs[col] = le
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_data(self):
        data = []
        for col, widget in self.inputs.items():
            if isinstance(widget, QComboBox):
                data.append(widget.currentData())
            else:
                data.append(widget.text())
        return data