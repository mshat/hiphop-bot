import random
import string


def randomword(length):
    letters = string.ascii_lowercase + string.digits
    word = ''.join(random.choice(letters) for i in range(length))
    return word.upper()
