import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validates an email address format using a regular expression.

    :param email: The email string to validate.

    :return:  bool: True if the email format is valid, False otherwise.
    """

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_password(password: str)-> bool:
    """
    Validates password strength (e.g., minimum length).

    :param password: The password string to validate.

    :return: bool: True if the password meets the criteria, False otherwise.
    """

    return len(password) >= 8

def validate_amount(amount_str: str)-> Optional[Decimal]:
    """
    Validates and converts a string to a positive Decimal.

    :param amount_str: The amount string from user input.

    :return: Optional[Decimal]: The converted Decimal amount if valid and positive, otherwise None.
    """

    try:
        amount = Decimal(amount_str)
        if amount > 0:
            return amount

    except InvalidOperation:
        return None

    return None

def validate_date(date_str: str, fmt: str = '%Y-%m-%d') -> Optional[datetime]:
    """
     Validates and converts a date string to a datetime object.

    :param date_str: The date string from user input.
    :param fmt: The expected date format. Defaults to "%Y-%m-%d".

    :return: Optional[datetime]: The datetime object if the string is a valid date, otherwise None.
    """

    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        return None

def validate_not_empty(text: str) -> bool:
    """
    Validates that a string is not empty or just whitespace.

    :param text: The string to validate.

    :return: bool: True if the string is not empty, False otherwise.
    """

    return bool(text and not text.isspace())