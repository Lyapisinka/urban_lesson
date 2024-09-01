def personal_sum(numbers):
    result = 0
    incorrect_data = 0

    # Перебор элементов коллекции
    for item in numbers:
        try:
            result += item
        except TypeError:
            incorrect_data += 1
            print(f'Некорректный тип данных для подсчёта суммы - {item}')

    # Возвращаем кортеж с суммой и количеством некорректных данных
    return result, incorrect_data


def calculate_average(numbers):
    try:
        # Сумма и количество некорректных данных из функции personal_sum
        total_sum, incorrect_data = personal_sum(numbers)

        # Проверка на пустую коллекцию
        count = len(numbers) - incorrect_data
        if count == 0:
            raise ZeroDivisionError

        # Вычисление среднего арифметического
        average = total_sum / count
        return average
    except ZeroDivisionError:
        # Обработка деления на ноль
        return 0
    except TypeError:
        # Обработка некорректного типа данных
        print('В numbers записан некорректный тип данных')
        return None


print(f'Результат 1: {calculate_average("1, 2, 3")}')  # Строка перебирается, но каждый символ - строковый тип
print(f'Результат 2: {calculate_average([1, "Строка", 3, "Ещё Строка"])}')  # Учитываются только 1 и 3
print(f'Результат 3: {calculate_average(567)}')  # Передана не коллекция
print(f'Результат 4: {calculate_average([42, 15, 36, 13])}')  # Всё должно работать
