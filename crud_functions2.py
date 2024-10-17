import sqlite3


def initiate_db():
    conn = sqlite3.connect('product2.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')

    # Создание таблицы пользователей, если она еще не создана
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
    ''')

    conn.commit()
    conn.close()


def get_all_products():
    conn = sqlite3.connect('product2.db')
    cursor = conn.cursor()

    cursor.execute('SELECT title, description, price FROM Products')
    products = cursor.fetchall()

    conn.close()
    return products


def add_user(username, email, age):
    conn = sqlite3.connect('product2.db')
    cursor = conn.cursor()

    # Добавление нового пользователя
    cursor.execute('''
        INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)
    ''', (username, email, age))

    conn.commit()
    conn.close()


def is_included(username):
    conn = sqlite3.connect('product2.db')
    cursor = conn.cursor()

    cursor.execute('SELECT 1 FROM Users WHERE username = ?', (username,))
    user_exists = cursor.fetchone() is not None

    conn.close()
    return user_exists