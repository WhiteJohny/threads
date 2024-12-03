import math
from concurrent.futures import ThreadPoolExecutor, as_completed


def factorial(n):
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    return math.factorial(n)


def power(base, exponent):
    return base ** exponent


def integrate(function, a, b, steps=1000):
    """Численное интегрирование методом прямоугольников."""
    if a > b:
        raise ValueError("Левая граница интеграла должна быть меньше правой")
    step = (b - a) / steps
    result = sum(function(a + i * step) * step for i in range(steps))
    return result


def calculate(task):
    """Обработчик задач."""
    operation = task['operation']
    try:
        if operation == 'factorial':
            return factorial(task['n'])
        elif operation == 'power':
            return power(task['base'], task['exponent'])
        elif operation == 'integrate':
            return integrate(task['function'], task['a'], task['b'], task.get('steps', 1000))
        else:
            raise ValueError("Неизвестная операция")
    except Exception as e:
        return f"Ошибка: {e}"


if __name__ == "__main__":
    tasks = [
        {'operation': 'factorial', 'n': 5},
        {'operation': 'power', 'base': 2, 'exponent': 10},
        {'operation': 'integrate', 'function': math.sin, 'a': 0, 'b': math.pi},
        {'operation': 'factorial', 'n': -1},  # Ошибка
        {'operation': 'power', 'base': 10, 'exponent': -2},
    ]

    results = []
    with ThreadPoolExecutor() as executor:
        future_to_task = {executor.submit(calculate, task): task for task in tasks}
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                results.append((task, result))
            except Exception as e:
                results.append((task, f"Ошибка выполнения: {e}"))

    for task, result in results:
        print(f"Задача: {task}, Результат: {result}")
