import threading


def words_counter(arr: list[str]):
    words_count = dict()
    for row in arr:
        words = row.split(" ")
        for word in words:
            if not words_count.get(word):
                words_count[word] = 1
            else:
                words_count[word] += 1

    counters.append(words_count)


counters = []
path = input("Enter the path to the file: ")
flag = True
while flag:
    try:
        count = int(input("Enter amount of threads: "))
        if count > 0:
            flag = False
        else:
            print("Enter the number > 1")
    except ValueError:
        print("Wrong count")

try:
    with open(path, "r") as file:
        text = file.readlines()
except FileNotFoundError:
    print("File not found")

length = len(text) // count

divided_text = [[text[j].replace("\n", "") for j in range(length * i, length * i + length)] for i in range(count)]
diff = len(text) - length
k = length
while diff > 0:
    divided_text[-1].append(text[k])
    k += 1
    diff -= 1

threads = [threading.Thread(target=words_counter, args=(divided_text[i], )) for i in range(count)]
for th in threads:
    th.start()

for th in threads:
    th.join()

words_count = dict()
for counter in counters:
    words_count.update(counter)

print(words_count)
