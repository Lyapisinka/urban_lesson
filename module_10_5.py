import os
import time
from multiprocessing import Pool


def read_info(name):
    all_data = []
    with open(name, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            all_data.append(line)


if __name__ == "__main__":
    filenames = [f'./file {number}.txt' for number in range(1, 5)]

    # Линейный вызов
    start_time = time.time()
    for filename in filenames:
        read_info(filename)
    linear_duration = time.time() - start_time
    print(f"Линейный вызов занял: {linear_duration:.6f} секунд")

    # Многопроцессный вызов
    start_time = time.time()
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(read_info, filenames)
    parallel_duration = time.time() - start_time
    print(f"Многопроцессный вызов занял: {parallel_duration:.6f} секунд")