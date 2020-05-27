import random
from string import digits, ascii_lowercase, ascii_uppercase

from flask_login import current_user
from urllib.parse import urlparse
from urllib.parse import urljoin

from app.database import db
from app.users_module.models import User
from .models import Link

MAX_TAGS_PER_USER = 100


def http_normalize_slashes(url):
    url = str(url)
    segments = url.split('/')
    correct_segments = []
    for segment in segments:
        if segment != '':
            correct_segments.append(segment)
    first_segment = str(correct_segments[0])
    if first_segment.find('http') == -1:
        correct_segments = ['http:'] + correct_segments
    correct_segments[0] = correct_segments[0] + '/'
    normalized_url = '/'.join(correct_segments)
    return normalized_url


def add_prefix(link: str) -> str:
    parsed_url = urlparse(link)
    if not parsed_url.scheme:
        parsed_url = parsed_url._replace(scheme="http")
    return http_normalize_slashes(parsed_url.geturl())


def is_valid(link: str) -> bool:
    parsed_url = urlparse(urljoin(link, "/"))
    is_correct = (all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])
                  and len(parsed_url.netloc.split(".")) > 1)
    return is_correct


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
