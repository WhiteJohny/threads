import math
import threading
from queue import Queue


q = Queue()
COND = threading.Condition()


def f(x):
    return x ** 2


def factorial(n):
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")

    result = math.factorial(n)
    print(result)


def power(base, exponent):
    result = base ** exponent
    print(result)


def integrate(function, a, b, steps=1000):
    if a > b:
        raise ValueError("Левая граница интеграла должна быть меньше правой")
    step = (b - a) / steps
    result = sum(function(a + i * step) * step for i in range(steps))
    print(result)


def enter():
    operations = {1: "factorial", 2: "power", 3: "integrate"}
    flag = False
    while True:
        while True:
            try:
                data = input("Choose your operation\n1: factorial\n2: power\n3: integrate\nEnter `exit` to close\n")
                if data.lower() == "exit":
                    q.put("exit")
                    with COND:
                        COND.notify()

                    flag = True
                    break

                operation = operations.get(int(data))
                if operation is not None:
                    break
            except ValueError:
                pass

            print("Wrong operation!")

        if flag:
            break

        calculate(operation)


def calculate(operation):
    if operation == "integrate":
        while True:
            try:
                a, b = map(int, input("Enter two numbers split by space: ").split(" "))
                q.put(threading.Thread(target=integrate, args=(f, a, b)))
                break
            except ValueError:
                print("Wrong numbers!")
    elif operation == "power":
        while True:
            try:
                a, b = map(int, input("Enter two numbers split by space: ").split(" "))
                q.put(threading.Thread(target=power, args=(a, b)))
                break
            except ValueError:
                print("Wrong numbers!")
    elif operation == "factorial":
        while True:
            try:
                n = int(input("Enter absolute integer number: "))
                q.put(threading.Thread(target=factorial, args=(n,)))
                break
            except ValueError:
                print("Wrong number!")
    with COND:
        COND.notify()


def consumer():
    while True:
        if q.empty():
            with COND:
                COND.wait()

        data = q.get()
        if data == "exit":
            break

        print(data.name, "start")
        data.start()


def main():
    th1 = threading.Thread(target=enter, args=())
    th2 = threading.Thread(target=consumer, args=())

    th1.start()
    th2.start()

    th1.join()


if __name__ == "__main__":
    main()
