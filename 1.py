from threading import Thread


def simple_function(some_arg: any) -> None:
    pass


flag = True
while flag:
    try:
        count = int(input("Введите количество потоков, которое вы хотите создать: "))
        flag = False
    except ValueError:
        print("Неправильно введенное количество потоков!")

arg = True
threads = [Thread(target=simple_function, args=(arg, )) for _ in range(count)]
print(f"Имена {count} потоков:", *[thread.name for thread in threads], sep="\n")
