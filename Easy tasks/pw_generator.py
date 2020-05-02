import string
from random import randint


# Simple password generator
def makepassword(length):
    letters = string.printable
    password = ''
    for i in range(length):
        temp = randint(0, len(letters) - 1)
        password += letters[temp]

    return password


print(makepassword(20))