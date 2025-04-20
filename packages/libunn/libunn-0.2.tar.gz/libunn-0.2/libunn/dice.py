# Part of libunn, view: https://github.com/juanvel4000/libunn
import random, time
random.seed(int(time.time()))
def roll():

    return random.randint(1, 6)
def rollMultiple(dies=2):
    if not isinstance(dies, int):
        return False
    result = 0
    for i in range(dies):
        result += roll()
    return result