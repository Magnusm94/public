import random

# Super simple password generator

characters = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$^&*"

length = input("How many characters do you want your password to be? ")
length = int(length)
password = ''


for c in range(length):
    password += characters[random.randint(0, len(characters))]
print(password)