glist = []


def list_(args):
    for i in args:
        for j in i:
            for k in j:
                if isinstance(k, int):
                    glist.append(k)
                elif isinstance(k, str):
                    glist.append(len(k))
                elif isinstance(k, tuple):
                    for l in k:
                        if isinstance(l, int):
                            glist.append(l)
                        elif isinstance(l, str):
                            glist.append(len(l))


def str_(args):
    glist.append(len(args))


def dict_(**args):
    for key, j in args.items():
        key = len(key)
        glist.append(key)
        glist.append(j)


def tuple_(*args):
    for k in args:
        if isinstance(k, int):
            glist.append(k)
        elif isinstance(k, dict):
            dict_(**k)
        elif isinstance(k, list):
            list_(k)


def calculate_structure_sum(*args):
    for i in range(len(args)):
        if isinstance(args[i], list):
            glist.extend(args[i])
            continue
        elif isinstance(args[i], dict):
            dict_(**args[i])
            continue
        elif isinstance(args[i], tuple):
            tuple_(*args[i])
            continue
        elif isinstance(args[i], str):
            str_(args[i])
            continue
    return sum(glist)

data_structure = [
    [1, 2, 3],
    {'a': 4, 'b': 5},
    (6, {'cube': 7, 'drum': 8}),
    "Hello",
    ((), [{(2, 'Urban', ('Urban2', 35))}])
]


result = calculate_structure_sum(*data_structure)
print(result)
