import re
import datetime

def validate_amount(amount):
    try:
        amt = float(amount)
        if amt < 0:
            raise ValueError('Amount Must be Positive.')
        return amt
    except ValueError as e:
        raise e

def validate_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception:
        raise ValueError('Invalid Date Format, Required YYYY-MM-DD.')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValueError('Invalid Email Format.')
    return email