import os
import getpass
from typing import List, Dict, Any, Callable, Optional
from tabulate import tabulate
from validators import *

def clear_screen():
    """
    Clears the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(title: str):
    """
    Prints a formatted title bar.

    :param title: The title text to display.
    """
    width = 80
    print('=' * width)
    print(f'{title.center(width)}')
    print('=' * width)

def print_table(data: List[Dict[str, Any]], headers: List[str]):
    """
    Prints data in a formatted table using the tabulate library.

    :param data: A list of dictionaries representing the rows.
    :param headers: A list of strings for the table headers.
    """
    if not data:
        print('\nNo Data To Display.')
        return

    # Convert List of Dicts to List of Lists for Tabulate:
    table_data = [[row.get(header.lower().replace(' ','_'), '') for header in headers] for row in data]

    print(tabulate(table_data, headers= headers, tablefmt= 'grid'))

def get_input(prompt: str, validator: Optional[Callable[[str], Any]] = None, error_message: str = 'Invalid Input') -> Any:
    """
    Prompts the user for input and validates it using a provided function.

    :param prompt: The message to display to the user.
    :param validator: A function to validate and process the input. Defaults to None.
    :param error_message: The error message to show on validation failure. Defaults to "Invalid input."

    :return: Any: The validated and processed user input.
    """

    while True:
        user_input = input(f'{prompt}: ').strip()

        if validator:
            validated_input = validator(user_input)

            if validated_input is not None:
                return validated_input
            else:
                print(error_message)

        else:
            return user_input


def get_password_input(prompt: str = 'Password') -> str:
    """
     Prompts the user for a password without showing the input on the screen.

    :param prompt: The message to display. Defaults to "Password".

    :return: The password entered by the user.
    """

    return getpass.getpass(f'{prompt}: ')