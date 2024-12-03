import time
import threading


class Park:
    def __init__(self):
        self.places = [Place() for _ in range(2)]

    def parking(self, hold_time):
        for place in self.places:
            if place.is_free:
                threading.Timer(interval=hold_time, function=self.exit, args=(place, )).start()
                place.parking()
                return True

        return False

    @staticmethod
    def exit(place):
        place.exit()


class Place:
    def __init__(self):
        self.is_free = True

    def parking(self):
        self.is_free = False

    def exit(self):
        self.is_free = True
        print("Free!")


park = Park()
while True:
    hold_time = int(input("park?"))
    if park.parking(hold_time):
        print("Success!")
    else:
        print("No places to park!")
