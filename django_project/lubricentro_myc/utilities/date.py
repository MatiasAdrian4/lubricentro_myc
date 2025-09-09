from datetime import datetime

from django_project.settings import DATE_FORMAT


def str_to_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, DATE_FORMAT)
