from threading import Thread
from math import sqrt


def main():
    while True:
        try:
            start, end = map(int, input("Введите два целых числа через пробел: ").split(" "))
        except ValueError:
            print("Неправильный ввод диапазона!")
            continue

        if start > end:
            end, start = start, end

        while True:
            try:
                threads_count = int(input(
                    f"Введите количество потоков для нахождения простых чисел на промежутке [{start}, {end}]: "))
            except ValueError:
                print("Неправильный ввод количества потоков!")
                continue
            if threads_count > 0:
                diff = (end - start) // threads_count
                divided_ranges = [[start + diff * i, start + diff * (i + 1)]
                                  for i in range(threads_count)]
                divided_ranges[-1][1] = end + 1 if divided_ranges[-1][1] != end else divided_ranges[-1][1] + 1

                threads = []
                for r in divided_ranges:
                    thread = Thread(target=find_simple_numbers, args=(r[0], r[1]))
                    threads.append(thread)
                    thread.start()

                for th in threads:
                    th.join()

                return 0
            else:
                print("Количество потоков должно быть минимум 1!")


def find_simple_numbers(s: int, e: int) -> None:
    for num in range(s, e):
        if check_simple(num):
            simple_numbers.append(num)


def check_simple(num: int) -> bool:
    for div in range(2, int(sqrt(num) + 1)):
        if num % div == 0:
            return False

    if num == 1:
        return False

    return True


if __name__ == "__main__":
    simple_numbers = []
    if not main():
        print(simple_numbers)
