class UserAgent:

    def __new__(cls, filename):
        with open(filename, encoding='utf-8') as f:
            lines = f.read().splitlines()
        return lines
