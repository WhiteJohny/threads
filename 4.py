from concurrent.futures import ThreadPoolExecutor


def factorial(num1: int, num2: int) -> int:
    res = 1
    while num1 <= num2:
        res *= num1
        num1 += 1

    return res


def entering(text: str) -> int:
    while True:
        try:
            print(text, end=" ")
            n = int(input())
            if n > 0:
                return n
        except ValueError:
            print("Число введено неправильно!")


num = entering("Введите целое число большее 0:")
threads_count = entering(f"Введите количество (не менее 1) потоков для нахождения {num}!:")
diff = num // threads_count
divided_ranges = [[diff * i + 1, diff * (i + 1)] for i in range(threads_count)]
divided_ranges[-1][1] = num if divided_ranges[-1][1] != num else divided_ranges[-1][1]

return_values = []
for r in divided_ranges:
    with ThreadPoolExecutor() as executor:
        future = executor.submit(factorial, r[0], r[1])
        return_value = future.result()
        return_values.append(return_value)

res = 1
for v in return_values:
    res *= v
print(return_values)
print(res)
