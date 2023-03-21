from random import randint


class RandomModelGenerator:

    MANUFACTURER = ['motorola', 'samsung', 'asus', 'xiaomi']
    MOBILE_MODEL = [['moto g(6)', 'moto e5', 'MotoG3', 'Moto G (4)'],
                    ['SM-G991B', 'SM-G950U', 'SM-G610M', 'SM-N920C'],
                    ['ASUS_Z01QD', 'ZS600KL', 'ASUS_Z00AD', 'ASUS_Z00UD'],
                    ['Redmi 4X', 'Redmi 4', 'Redmi 5A', 'Redmi 4A']]

    @staticmethod
    def get_manufacturer():
        rand_manufacturer = randint(0, 3)
        return RandomModelGenerator.MANUFACTURER[rand_manufacturer]

    @staticmethod
    def get_mob_model(manufacturer):
        index = RandomModelGenerator.MANUFACTURER.index(manufacturer)
        return RandomModelGenerator.MOBILE_MODEL[index][randint(0, 3)]
