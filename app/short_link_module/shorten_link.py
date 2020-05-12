import re
import random
from string import digits, ascii_lowercase, ascii_uppercase

import requests

from app.database import db
from .models import Link


def add_prefix(link: str) -> str:
    if len(link) < 5:
        return "http://" + link
    prefix = link[:5].lower()
    if not prefix.startswith("http") and not prefix.startswith("https"):
        link = "http://" + link
    return link


def is_valid(link: str) -> bool:
    try:
        response = requests.head(link)
        return response.status_code < 400
    except requests.exceptions.ConnectionError:
        return False


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
