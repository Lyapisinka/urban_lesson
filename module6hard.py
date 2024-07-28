class Figure:
    sides_count = 0

    def __init__(self, color, *sides):
        self.__sides = []
        self.__color = color
        self.filled = False

        if len(sides) == self.sides_count:
            self.set_sides(*sides)
        else:
            self.__sides = [1] * self.sides_count

    def get_sides(self):
        return self.__sides

    def get_color(self):
        return self.__color

    def __is_valid_color(self, r, g, b):
        if isinstance(r, int) and isinstance(g, int) and isinstance(b, int):
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                return True
        return False

    def __is_valid_sides(self, *sides):
        if isinstance(self, Triangle) and len(sides) == self.sides_count:
            a, b, c = sides
            if a > 0 and b > 0 and c > 0:
                return a ** 2 + b ** 2 == c ** 2
        else:
            if len(sides) == self.sides_count:
                for side in sides:
                    if not isinstance(side, int) or side < 0:
                        return False
            return True

    def get_valid_sides(self, *new_sides):
        return self.__is_valid_sides(*new_sides)

    def set_sides(self, *new_sides):
        if self.__is_valid_sides(*new_sides):
            self.__sides = list(new_sides)

    def set_color(self, r, g, b):
        if self.__is_valid_color(r, g, b):
            self.__color = [r, g, b]

    def __len__(self):
        return sum(self.__sides)


class Circle(Figure):
    sides_count = 1

    def __init__(self, color, *sides):
        super().__init__(color, *sides)
        self.__radius = sides[0] / (2 * 3.14)

    def set_sides(self, *new_sides):
        if len(new_sides) == 1:
            super().set_sides(*new_sides)
            self.__radius = new_sides[0] / (2 * 3.14)

    def get_square(self):
        return 3.14 * (self.__radius ** 2)


class Triangle(Figure):
    sides_count = 3

    def __init__(self, color, *sides):
        super().__init__(list(color), *sides)
        self.__height = self.calculate_height()

    def calculate_height(self):
        # Можно использовать формулу Герона для вычисления высоты
        a, b, c = self.get_sides()
        s = (a + b + c) / 2
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        return 2 * area / a  # Высота по основанию a

    def get_square(self):
        return 0.5 * self.get_sides()[0] * self.__height  # Площадь = (1/2) * основание * высота

    def set_sides(self, *new_sides):
        if self.get_valid_sides(*new_sides):
            super().set_sides(*new_sides)
            self.__height = self.calculate_height()


class Cube(Figure):
    sides_count = 12

    def __init__(self, color, *sides):
        super().__init__(list(color), *sides)
        self.set_sides(*sides)

    def get_volume(self):
        return self.get_sides()[0] ** 3

    def set_sides(self, *new_sides):
        if len(new_sides) == 1:
            super().set_sides(*[new_sides[0]] * self.sides_count)


circle1 = Circle((200, 200, 100), 10)
circle1.set_color(55, 66, 77)
print(circle1.get_color())

circle1.set_sides(15)
print(circle1.get_sides())

circle1.set_sides(3, 30)
print(circle1.get_sides())

print(circle1.get_square())
print(len(circle1))

cube1 = Cube((222, 35, 130), 6)
cube1.set_color(300, 70, 15)
print(cube1.get_color())

cube1.set_sides(5, 3, 12, 4, 5)
print(cube1.get_sides())
print(cube1.get_volume())

rectangle1 = Triangle((155, 55, 55), 3, 4, 5)
rectangle1.set_color(300, 70, 15)
print(rectangle1.get_color())
rectangle1.set_sides(12, 4, 5)
print(rectangle1.get_sides())
print(rectangle1.get_square())

circle2 = Circle((200, 200, 100), 10)
print(circle2.get_sides())

cube2 = Cube((200, 200, 100), 14, 5)
print(cube2.get_sides())
