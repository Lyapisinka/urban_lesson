import logging
import unittest

# Настройка логирования
logging.basicConfig(filename='runner_tests.log',
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    encoding='utf-8')


class Runner:
    def __init__(self, name, speed=5):
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой.")
        if not isinstance(speed, (int, float)) or speed < 0:
            raise ValueError("Скорость должна быть положительным числом.")

        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name
        return False


class RunnerTest(unittest.TestCase):
    def test_walk(self):
        try:
            runner = Runner('TestRunner', speed=-5)
            runner.walk()
            logging.info('"test_walk" выполнен успешно')
        except ValueError:
            logging.warning("Неверная скорость для Runner")

    def test_run(self):
        try:
            runner = Runner(123, speed=5)  # ошибка: имя не строка
            runner.run()
            logging.info('"test_run" выполнен успешно')
        except TypeError:
            logging.warning("Неверный тип данных для объекта Runner")


if __name__ == '__main__':
    unittest.main()
