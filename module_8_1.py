def add_everything_up(a, b):
    try:
        # Попытка сложить два данных
        result = a + b
    except TypeError:
        # Если возникает TypeError, возвращаем строковое представление обоих данных
        result = str(a) + str(b)
    return result


print(add_everything_up(123.456, 'строка'))
print(add_everything_up('яблоко', 4215))
print(add_everything_up(123.456, 7))
