import string
import random


def random_room():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(6))
    return result_str
