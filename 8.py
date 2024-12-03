import os
import threading
from queue import Queue

SEM = threading.Semaphore(2)


def producer(q: Queue, threads: list[threading.Thread]):
    for th in threads:
        print(th.name, "put")
        q.put(th)


def consumer(q: Queue):
    while not q.empty():
        th = q.get()
        print(th.name, "start")
        th.start()
        SEM.acquire()


def add_catalogs(catalogs):
    while True:
        catalog = input("Enter your catalog or `exit` to exit: ")
        if catalog.lower() == "exit":
            break

        if not (os.path.exists(catalog) and os.access(catalog, os.R_OK)):
            print("Invalid path to catalog!")
        else:
            catalogs.append(catalog)


def choose_pattern():
    pattern = " "
    while pattern not in "12":
        pattern = input("Choose pattern:\n1: File name\n2: File extension\n")
        if pattern.lower() == "exit":
            return pattern

    return pattern


def find_extension(pattern: str, catalog: str, match: list):
    names = [name for name in os.listdir(catalog) if "." in name]
    for name in names:
        if name[name.find(".") + 1:] == pattern:
            match.append(name)
    print("end")
    SEM.release()


def find_filename(pattern: str, catalog: str, match: list):
    names = os.listdir(catalog)
    for name in names:
        if name.startswith(pattern):
            match.append(name)
    print("end")
    SEM.release()


def main():
    q = Queue()
    match = []
    catalogs = []
    add_catalogs(catalogs)
    if not catalogs:
        return

    pattern_mode = choose_pattern()
    if pattern_mode != "exit":
        count = len(catalogs)
        pattern = input("Enter the pattern: ")
        if pattern_mode == 1:
            threads = [threading.Thread(target=find_filename, args=(pattern, catalogs[i], match))
                       for i in range(count)]

        else:
            threads = [threading.Thread(target=find_extension, args=(pattern, catalogs[i], match))
                       for i in range(count)]

        th1 = threading.Thread(target=producer, args=(q, threads))
        th2 = threading.Thread(target=consumer, args=(q, ))

        th1.start()
        th2.start()

        th1.join()
        th2.join()

        print(match)

    return


if __name__ == "__main__":
    main()
