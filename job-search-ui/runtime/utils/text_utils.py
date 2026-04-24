import re
from email.utils import parseaddr


def normalize_text(value):
    return re.sub(r'\s+', ' ', (value or '').strip()).lower()


def normalize_company(value):
    text = normalize_text(value)
    return re.sub(r'\b(inc|llc|ltd|corp|corporation|company|co)\b', '', text).strip(' ,.-')


def extract_domain(value):
    email = parseaddr(value or '')[1]
    if '@' in email:
        return email.split('@', 1)[1].lower()
    return ''
