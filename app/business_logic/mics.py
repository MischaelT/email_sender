import datetime
import random
from typing import List
import names

from settings import DATE_FORMAT


def date_by_adding_business_days(from_date: str, add_days: int) -> datetime:

    business_days_to_add = add_days
    current_date = datetime.datetime.strptime(from_date, DATE_FORMAT)
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date.date()


def date_by_adding_days(from_date: str, add_days: int) -> datetime:

    current_date = datetime.datetime.strptime(from_date, DATE_FORMAT)
    current_date += datetime.timedelta(days=add_days)

    while True:
        if current_date.weekday() >= 5:
            current_date += datetime.timedelta(days=1)
        else:
            break

    return current_date.date()


def generate_random_email(website_address) -> List[str]:
    emails = []

    em = ['info', 'seo', 'ceo', 'support', 'inquiries', 'enquiries', 'communications',
          'president', 'partners', 'director', 'ads', 'advertisement', 'Marketing',
          'publicidad', 'sales', 'commercial', 'Deals']

    for _ in range(2):
        email = f'{random.choice(em)}@{website_address}'
        emails.append(email)

    for _ in range(2):
        first_name = names.get_first_name(random.choice(['male', 'female']))
        surname = names.get_last_name()
        email = f"{first_name}{random.choice(['.', '_', '-', ''])}{surname}@{website_address}"

        if bool(random.getrandbits(1)):
            email = email.lower()

        emails.append(email)

    return emails
