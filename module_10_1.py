from time import sleep, time
import threading


def write_words(word_count, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for i in range(1, word_count + 1):
            file.write(f"Какое-то слово № {i}\n")
            sleep(0.1)
    print(f"Завершилась запись в файл {file_name}")


if __name__ == "__main__":
    # Взятие текущего времени
    start_time = time()

    # Запуск функций с аргументами из задачи
    write_words(10, "example1.txt")
    write_words(30, "example2.txt")
    write_words(200, "example3.txt")
    write_words(100, "example4.txt")

    # Взятие текущего времени
    end_time = time()

    # Вывод разницы начала и конца работы функций
    print("Работа функций", end_time - start_time)

    # Взятие текущего времени
    start_time_threads = time()

    # Создание и запуск потоков с аргументами из задачи
    thread1 = threading.Thread(target=write_words, args=(10, "example5.txt"))
    thread2 = threading.Thread(target=write_words, args=(30, "example6.txt"))
    thread3 = threading.Thread(target=write_words, args=(200, "example7.txt"))
    thread4 = threading.Thread(target=write_words, args=(100, "example8.txt"))

    threads = [thread1, thread2, thread3, thread4]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # Взятие текущего времени
    end_time_threads = time()

    # Вывод разницы начала и конца работы потоков
    print("Работа потоков", end_time_threads - start_time_threads)