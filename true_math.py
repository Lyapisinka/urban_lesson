from math import inf


def devide(first, second):
    try:
        return first/second
    except ZeroDivisionError:
        return inf