from threading import Thread
from time import sleep


class Knight(Thread):
    def __init__(self, name, power):
        super().__init__()
        self.name = name
        self.power = power
        self.days = 0  # Для отслеживания количества дней

    def run(self):
        enemy_count = 100
        print(f"{self.name}, на нас напали!")

        while enemy_count > 0:
            self.days += 1
            sleep(1)  # Задержка в 1 секунду
            enemy_count -= self.power
            if enemy_count < 0:
                enemy_count = 0
            print(f"{self.name}, сражается {self.days} день(дня)..., осталось {enemy_count} воинов.")

        print(f"{self.name} одержал победу спустя {self.days} дней(дня)!")


if __name__ == "__main__":
    # Создание объектов класса Knight
    first_knight = Knight('Sir Lancelot', 10)
    second_knight = Knight("Sir Galahad", 20)

    # Запуск потоков
    first_knight.start()
    second_knight.start()

    # Остановка текущего потока до завершения работы потоков-рыцарей
    first_knight.join()
    second_knight.join()

    # Вывод строки об окончании сражения
    print("Все битвы закончились!")