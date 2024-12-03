import threading
import time

LOCK = threading.Lock()
COND = threading.Condition()


class ATM:
    def __init__(self, bill):
        self.bill: str = bill
        self.__money: float = 10000000.0
        self.__clients = []

    def add_client(self, client) -> bool:
        self.__clients.append(client)
        return True

    def bill_checking(self, bill: str):
        for client in self.__clients:
            if bill == client.bill:
                return True

        return False

    def debiting(self, amount: float, bill: str) -> (bool, bool):
        flag = False
        if self.bill_checking(bill):
            flag = True
            balance = self.__money - amount
            if balance >= 0:
                LOCK.acquire()
                self.__money = balance
                LOCK.release()
                return flag, True

        return flag, False

    def refill(self, amount: float, bill: str) -> bool:
        if self.bill_checking(bill):
            LOCK.acquire()
            self.__money += amount
            LOCK.release()
            return True

        return False


class Client:
    def __init__(self, bill):
        self.bill: str = bill
        self.__money: float = 0.0

    def refill(self, amount: float, atm: ATM) -> (bool, bool):
        cl, mn = atm.debiting(amount, self.bill)
        if cl and mn:
            LOCK.acquire()
            self.__money += amount
            LOCK.release()

        return cl, mn

    def debiting(self, amount: float, atm: ATM):
        if atm.refill(amount, self.bill):
            LOCK.acquire()
            self.__money -= amount
            LOCK.release()
            return True

        return False


ATM1 = ATM("ATM1")


def scum(client: Client, amount: float):
    while True:
        cl, mn = client.refill(amount, ATM1)
        if not cl:
            print(client.bill, "does not have access to", ATM1.bill)
        elif not mn:
            print(client.bill, ATM1.bill, "has not that amount of value")
            with COND:
                COND.wait()
                print(client.bill, "wait for refill", ATM1.bill)
        else:
            print(client.bill, "earned money from", ATM1.bill)

        time.sleep(2)


def refill_bill(amount: float, bill: str):
    time.sleep(10)
    ATM1.refill(amount, bill)
    with COND:
        print("Bill refilled!")
        COND.notify_all()


def main():
    flag = True
    while flag:
        try:
            count = int(input("Enter amount of clients: "))
            if count > 0:
                flag = False
            else:
                print("Enter the number > 1")
        except ValueError:
            print("Wrong count")

    clients = [Client(f'Client{str(i)}') for i in range(1, count + 1)]
    amount1 = 500456.56
    amount2 = 100000000.01

    for cl in clients:
        ATM1.add_client(cl)

    threads = [threading.Thread(target=scum, args=(clients[i], amount1)) for i in range(count)]
    threads.append(threading.Thread(target=refill_bill, args=(amount2, clients[0].bill)))
    for th in threads:
        th.start()

    for th in threads:
        th.join()


if __name__ == "__main__":
    main()
