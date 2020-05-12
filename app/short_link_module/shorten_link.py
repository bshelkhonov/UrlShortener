import re
import random
from string import digits, ascii_lowercase, ascii_uppercase

import requests
from flask_login import current_user

from app.database import db
from app.users_module.models import User
from .models import Link

MAX_TAGS_PER_USER = 100


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


def make_short_link() -> str:
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
    short = make_short_link()
    while Link.query.filter_by(short_link=short).first():
        short = make_short_link()
    new_elem = Link(original_link=link, short_link=short)
    db.session.add(new_elem)
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.id).first()
        user.links.append(new_elem)
    db.session.commit()
    return short
