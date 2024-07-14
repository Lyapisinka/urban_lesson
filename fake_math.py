def devide(first, second):
    try:
        return first/second
    except ZeroDivisionError:
        return "Ошибка"