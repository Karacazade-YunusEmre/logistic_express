from random import random


def get_freight_number():
    with open("utilities/alphabe", "r") as file:
        alphabe = file.read()

    number = str.join("", random.sample(list(alphabe), 6))
    return number