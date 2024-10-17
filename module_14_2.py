import sqlite3

conn = sqlite3.connect('not_telegram2.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')

users_data = [
    ('User1', 'example1@gmail.com', 10, 1000),
    ('User2', 'example2@gmail.com', 20, 1000),
    ('User3', 'example3@gmail.com', 30, 1000),
    ('User4', 'example4@gmail.com', 40, 1000),
    ('User5', 'example5@gmail.com', 50, 1000),
    ('User6', 'example6@gmail.com', 60, 1000),
    ('User7', 'example7@gmail.com', 70, 1000),
    ('User8', 'example8@gmail.com', 80, 1000),
    ('User9', 'example9@gmail.com', 90, 1000),
    ('User10', 'example10@gmail.com', 100, 1000)
]
cursor.executemany('''
INSERT INTO Users (username, email, age, balance)
SELECT ?, ?, ?, ?
WHERE NOT EXISTS (SELECT 1 FROM Users)
''', users_data)

cursor.execute('''
UPDATE Users SET balance = 500 WHERE (id % 2) = 1
''')

cursor.execute('SELECT id FROM Users')
rows = cursor.fetchall()
ids_to_delete = [row[0] for i, row in enumerate(rows) if (i % 3) == 0]

cursor.executemany('DELETE FROM Users WHERE id = ?', [(id,) for id in ids_to_delete])

cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
result = cursor.fetchall()

for row in result:
    print(f'Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}')

cursor.execute('DELETE FROM Users WHERE id = 6')

cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]

cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]

if total_users > 0:
    print(all_balances / total_users)
else:
    print("Нет пользователей для расчета среднего баланса.")

conn.commit()

conn.close()
