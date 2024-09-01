first_strings = ['Elon', 'Musk', 'Programmer', 'Monitors', 'Variable']
second_strings = ['Task', 'Git', 'Comprehension', 'Java', 'Computer', 'Assembler']

# Создание first_result
first_result = [len(s) for s in first_strings if len(s) >= 5]

# Создание second_result
second_result = [(s1, s2) for s1 in first_strings for s2 in second_strings if len(s1) == len(s2)]

# Создание third_result
third_result = {s: len(s) for s in first_strings + second_strings if len(s) % 2 == 0}

# Вывод результатов
print(first_result)   # Вывод: [10, 8, 8]
print(second_result)  # Вывод: [('Elon', 'Task'), ('Elon', 'Java'), ('Musk', 'Task'), ('Musk', 'Java'), ('Monitors', 'Computer'), ('Variable', 'Computer')]
print(third_result)   # Вывод: {'Elon': 4, 'Musk': 4, 'Programmer': 10, 'Monitors': 8, 'Variable': 8, 'Task': 4, 'Java': 4, 'Computer': 8}