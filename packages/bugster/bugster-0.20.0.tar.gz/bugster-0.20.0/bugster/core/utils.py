"""
Bugster utils
"""

import random
import string


def random_string(length=5):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def random_integer(length=5):
    min_value = 10 ** (length - 1)
    max_value = 10**length - 1
    return str(random.randint(min_value, max_value))

def random_email():
    return f"{random_string(5)}@bugster.dev"

def random_phone_number():
    return f"+0{random_integer(10)}"

def random_url():
    return f"https://{random_string(5)}.bugster.dev"

def random_ip_address():
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

