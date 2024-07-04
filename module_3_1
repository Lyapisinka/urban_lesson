calls = 0


def count_calls():
    global calls
    calls += 1


def string_info(string):
    count_calls()
    str_inf = (len(string), string.upper(), string.lower())
    return str_inf

def is_contains(is_str, is_list):
    count_calls()
    lowercase_list = []
    for i in is_list:
        lowercase_list.append(i.lower())
    return is_str.lower() in lowercase_list


print(string_info('Capybara'))
print(string_info('Armageddon'))
print(is_contains('Urban', ['ban', 'BaNaN', 'urBAN']))
print(is_contains('cycle', ['recycling', 'cyclic']))
print(calls)
