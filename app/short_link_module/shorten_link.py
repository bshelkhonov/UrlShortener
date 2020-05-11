import re
import random
from string import digits, ascii_lowercase, ascii_uppercase

from app.database import db
from .models import Link


def is_valid(link: str) -> bool:
    pattern = r"(^https?:\/\/)?[a-z0-9~_\-\.]+\.[a-z]{2,9}(\/|:|\?[!-~]*)?"
    match = re.fullmatch(pattern, link)
    return bool(match)


def shorten() -> str:
    alphabet = digits + ascii_lowercase + ascii_uppercase
    n = random.randint(0, 62 ** 5)
    short = ""
    short += alphabet[n % 62]
    n //= 62

    while n > 0:
        short += alphabet[n % 62]
        n //= 62
    return short[::-1]


def add_to_db(link: str):
    find_link = Link.query.filter(Link.original_link == link).all()
    if len(find_link) != 0:
        return find_link[0].short_link
    short = shorten()
    new_elem = Link(original_link=link, short_link=short)
    db.session.add(new_elem)
    db.session.commit()
    return short
