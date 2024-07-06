data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]


def calculate_structure_sum(data, is_end=False):
    result = []

    if isinstance(data, list) or isinstance(data, tuple):
        for item in data:
            result.extend(calculate_structure_sum(item))
    elif isinstance(data, set):
        for item in data:
            result.extend(calculate_structure_sum(item))
    elif isinstance(data, dict):
        for key, value in data.items():
            result.append(len(key))
            result.extend(calculate_structure_sum(value))
    elif isinstance(data, str):
        result.append(len(data))
    else:
        result.append(data)

    if not is_end:
        return result
    else:
        return sum(result)


result = calculate_structure_sum(data_structure, True)
print(result)
