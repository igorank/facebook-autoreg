import random
import string


class RandomGenerator:

    @staticmethod
    def random_username(length):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    @staticmethod
    def random_password(length):
        random_pass = ''.join(random.choices(string.ascii_lowercase, k=length))
        return random_pass
