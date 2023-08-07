import re


def is_valid(email: str):
    pat = "^[a-z0-9A-Z][a-zA-Z0-9-_\.]+@[a-zA-Z0-9-]+(\.[a-z]{1,15}){1,4}$"  # noqa
    return re.match(pat, email)


def is_empty(value: str):
    value = re.sub(r'^\s*$', '', value)
    return not value


def the_same_emails(email_1: str, email_2: str):
    return str.lower(email_1) == str.lower(email_2)
