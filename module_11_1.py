import requests
import pandas as pd
import numpy as np


def fetch_data():
    # Отправка GET-запроса на API
    response = requests.get("https://api.github.com/repos/psf/requests")

    # Проверка успешности запроса
    if response.status_code == 200:
        # Получение JSON-данных
        data = response.json()

        # Вывод интересующих данных в консоль
        print(f"Repository: {data['name']}")
        print(f"Description: {data['description']}")
        print(f"Stars: {data['stargazers_count']}")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


fetch_data()


def analyze_data():
    # Чтение данных из CSV файла
    df = pd.read_csv('data.csv')

    # Вывод первых 5 строк данных
    print(df.head())

    # Группировка данных по колонке и вычисление среднего значения другой колонки
    group_mean = df.groupby('category')['value'].mean()
    print(group_mean)

    # Фильтрация данных по условию
    filtered_df = df[df['value'] > 50]
    print(filtered_df)


analyze_data()


def perform_operations():
    # Создание массива чисел от 0 до 9
    arr = np.arange(10)
    print("Original array:", arr)

    # Выполнение математических операций
    arr_squared = np.square(arr)
    print("Squared array:", arr_squared)

    # Вычисление среднего значения
    mean_value = np.mean(arr)
    print("Mean value:", mean_value)

    # Создание двумерного массива и выполнение матричных операций
    matrix = np.array([[1, 2], [3, 4]])
    print("Original matrix:\n", matrix)
    matrix_inv = np.linalg.inv(matrix)
    print("Inverse matrix:\n", matrix_inv)


perform_operations()
