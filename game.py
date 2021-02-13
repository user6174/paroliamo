import random
import threading
import time

with open('paroliamo.txt', 'r') as f:
    treccani = [tuple(w[:-1].split(' ')) for w in f.readlines()]


def generate_letters():
    ret = list()
    for i in range(2):
        for j in range(5):
            p = ['e', 'a', 'i', 'o', 'u'] if i == 1 else \
                ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'z']
            w = [11.79, 11.74, 11.28, 9.83, 3.01] if i == 1 else \
                [.92, 4.5, 3.73, .95, 1.64, 1.54, 6.51, 2.51, 6.88, 3.05, .51, 6.37, 4.98, 5.62, 2.10, .49]
            ret.append(random.choices(population=p, weights=w)[0])
    return ret


def is_valid_word(l, w):
    tmp_l = [ch for ch in l]
    for ch in w:
        if ch not in tmp_l:
            return False
        tmp_l.remove(ch)
    return w in [cane[1] for cane in treccani]


def timer(s):
    for tick in range(s, -1, -1):
        if tick in (60, 30, 10, 5, 3, 2, 1):
            print(f'\n{tick} second{"s" if tick - 1 else ""} left\n')
        time.sleep(1)


def play_round():
    count = threading.Thread(target=timer, args=(90,))
    count.start()
    score = ('', 0)
    letters = generate_letters()
    print(letters)
    while count.is_alive():
        x = input('parola: ')
        if is_valid_word(letters, x):
            if len(x) >= score[1]:
                score = (x, len(x))
            print(f'la tua parola migliore: {score[0]} ({score[1]}p)')


play_round()
