def apply_all_func(int_list, *functions):
    results = {}

    for func in functions:
        func_name = func.__name__
        try:
            result = func(int_list)
            results[func_name] = result
        except Exception as e:
            results[func_name] = f'Error: {str(e)}'

    return results


print(apply_all_func([6, 20, 15, 9], max, min))
print(apply_all_func([6, 20, 15, 9], len, sum, sorted))