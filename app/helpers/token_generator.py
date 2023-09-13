import secrets
import string


class TokenGenerator:
    def __init__(self, length:int = 16):
        self.length = length

        self.letters = string.ascii_letters
        self.digits = string.digits
        self.special_chars = string.punctuation
        self.alphabet = self.letters + self.digits + self.special_chars
        # self.alphabet = self.letters + self.digits

    def generate(self):
        password = ""
        for i in range(self.length):
            password += ''.join(secrets.choice(self.alphabet))

        while True:
            password = ''
            for i in range(self.length):
                password += ''.join(secrets.choice(self.alphabet))

            if (any(char in self.special_chars for char in password) and
                    any(char in self.digits for char in password) == 1):
                break

        return password
