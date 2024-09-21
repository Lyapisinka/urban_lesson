def introspection_info(obj):
    # Получаем тип объекта
    obj_type = type(obj)

    # Получаем атрибуты объекта
    attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith("__")]

    # Получаем методы объекта
    methods = [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith("__")]

    # Получаем модуль, к которому принадлежит объект
    obj_module = obj.__class__.__module__

    # Формируем результат
    result = {'type': obj_type.__name__, 'attributes': attributes, 'methods': methods, 'module': obj_module}

    return result


# Пример использования
class MyClass:
    def __init__(self, value):
        self.value = value

    def my_method(self):
        return self.value


# Создаем объект класса MyClass
my_instance = MyClass(42)

# Анализируем объект
info = introspection_info(my_instance)
print(info)
