import threading
from random import randint
from time import sleep


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = threading.Lock()

    def deposit(self):
        for _ in range(100):  # Совершить 100 транзакций пополнения
            amount = randint(50, 500)
            with self.lock:
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")  # Если баланс >= 500 и замок заблокирован, ничего не делать (self.lock у нас не будет заблокирован на этом этапе)
            sleep(0.001)  # Имитируем задержку между операциями

    def take(self):
        for _ in range(100):  # Совершить 100 транзакций снятия
            amount = randint(50, 500)
            print(f"Запрос на {amount}")
            with self.lock:
                if amount <= self.balance:
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")  # При блокировке поток будет заблокирован для дальнейших действий
            sleep(0.001)  # Имитируем задержку между операциями


if __name__ == "__main__":
    bk = Bank()

    # Создание и запуск потоков
    th1 = threading.Thread(target=Bank.deposit, args=(bk,))
    th2 = threading.Thread(target=Bank.take, args=(bk,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()

    # Вывод итогового баланса
    print(f'Итоговый баланс: {bk.balance}')