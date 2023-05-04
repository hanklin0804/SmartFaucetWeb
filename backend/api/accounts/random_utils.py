import random 
import string


class RandomGenerateString():
    def generate_numbers(len: int) -> str:
        return ''.join([str(random.randint(0, 9)) for _ in range(len)])
    def generate_string(len: int) -> str:
        return ''.join([str(random.choice(string.ascii_letters + string.digits)) for _ in range(len)])

