import bcrypt

positions = [
    ('Администратор', 'admin'),
    ('Фотограф', 'photo'),
    ('Реставратор', 'rest')
]

print("INSERT INTO Workplace(branch_id, kiosk_id, position, duties, username, password_hash) VALUES")
rows = []
for branch_id in range(1, 9):
    for pos_ru, pos_en in positions:
        login = f'{pos_en}{branch_id}'
        duties = {
            'admin': 'Приём заказов, печать/проявка, работа с клиентами',
            'photo': 'Фотосъёмка (документы, художественное, ретро)',
            'rest': 'Реставрация фотографий, сканирование, оформление'
        }[pos_en]
        hash_ = bcrypt.hashpw(login.encode(), bcrypt.gensalt()).decode()
        rows.append(f"({branch_id}, NULL, '{pos_ru}', '{duties}', '{login}', '{hash_}')")

for kiosk_id in range(1, 9):
    login = f'kiosk{kiosk_id}'
    hash_ = bcrypt.hashpw(login.encode(), bcrypt.gensalt()).decode()
    rows.append(f"(NULL, {kiosk_id}, 'Оператор киоска', 'Приём заказов и продажа фототоваров/услуг', '{login}', '{hash_}')")

print(",\n".join(rows) + ";")