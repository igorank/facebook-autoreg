from random import randint


class RandomNumGenerator:

    mobile_operators = ["067", "096", "097", "098", "066", "095", "099", "063", "073", "093"]

    @staticmethod
    def __random_with_n_digits(num):
        range_start = 10 ** (num - 1)
        range_end = (10 ** num) - 1
        return randint(range_start, range_end)

    @staticmethod
    def get_rand_mob_num():
        return "38" + RandomNumGenerator.mobile_operators[randint(0, 9)]\
            + str(RandomNumGenerator.__random_with_n_digits(7))
