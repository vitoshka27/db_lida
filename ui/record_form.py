from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox

class RecordForm(QDialog):
    def __init__(self, columns, values=None, parent=None, pk_columns=None, fk_options=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование записи" if values else "Добавление записи")
        self.layout = QFormLayout(self)
        self.inputs = {}
        self.pk_columns = pk_columns or []
        self.fk_options = fk_options or {}
        # Список булевых полей (можно расширить при необходимости)
        BOOL_FIELDS = {'is_urgent', 'is_profi_client', 'is_active', 'is_admin', 'is_deleted'}
        for i, col in enumerate(columns):
            # --- FK: если есть опции, используем QComboBox ---
            if col in self.fk_options:
                cb = QComboBox(self)
                cb.addItem('Не выбрано', None)
                options = self.fk_options[col]
                for id_val, display in options:
                    cb.addItem(str(display), id_val)
                if values:
                    id_val = values[i]
                    idx = next((j+1 for j, (idv, _) in enumerate(options) if str(idv) == str(id_val)), 0)
                    cb.setCurrentIndex(idx)
                self.layout.addRow(col, cb)
                self.inputs[col] = cb
                continue
            # --- order_type: человеко-понятный текст <-> код ---
            if col == 'order_type':
                cb = QComboBox(self)
                cb.addItem('Проявка плёнки', 'film')
                cb.addItem('Печать фотографий', 'print')
                cb.addItem('Проявка + печать', 'both')
                if values:
                    val = values[i]
                    idx = {None: 0, 'film': 1, 'print': 2, 'both': 3}.get(val, 0)
                    cb.setCurrentIndex(idx)
                self.layout.addRow(col, cb)
                self.inputs[col] = cb
                continue
            # --- Boolean поля: Да/Нет/Не выбрано ---
            if col in BOOL_FIELDS:
                cb = QComboBox(self)
                cb.addItem('Не выбрано', None)
                cb.addItem('Да', True)
                cb.addItem('Нет', False)
                if values:
                    val = values[i]
                    if val in (1, True, '1', 'TRUE', 'True', 'Да'):
                        cb.setCurrentIndex(1)
                    elif val in (0, False, '0', 'FALSE', 'False', 'Нет'):
                        cb.setCurrentIndex(2)
                    else:
                        cb.setCurrentIndex(0)
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
        BOOL_FIELDS = {'is_urgent', 'is_profi_client', 'is_active', 'is_admin', 'is_deleted'}
        for col, widget in self.inputs.items():
            if isinstance(widget, QComboBox):
                val = widget.currentData()
                # Для булевых полей возвращаем 1/0/None
                if col in BOOL_FIELDS:
                    if val is True:
                        data.append(1)
                    elif val is False:
                        data.append(0)
                    else:
                        data.append(None)
                else:
                    data.append(None if val is None or val == '' else val)
            else:
                text = widget.text()
                data.append(text if text != '' else None)
        return data