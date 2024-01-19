import random
from string import ascii_letters, digits

from faker import Faker


def random_string(min_length=20, max_length=None, prefix="", characters=ascii_letters + digits):
    if max_length is None:
        max_length = min_length
    length = random.randint(min_length - len(prefix), max_length - len(prefix))
    random_part = "".join(random.choices(characters, k=length))
    return f"{prefix}{random_part}"


fake = Faker()


def random_paragraphs(n=5) -> list[str]:
    return fake.paragraphs(n)


def random_text(n=256) -> str:
    return fake.text(n)
