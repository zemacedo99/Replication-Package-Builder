"""Data validation"""
import csv
import os
import re


def find_strings_in_csv(csv_file_path, strings_to_find):
    """
    TODO
    """
    # ANSI escape codes for colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    RESET = '\033[0m'  # Reset to default color

    # Process each string in the list
    processed_strings_to_find = {process_string(s): s for s in strings_to_find}
    found_strings = set()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if 'ProcessedTitle' not in row:
                print(RED + "'ProcessedTitle' column not found in the CSV." + RESET)  # noqa: E501
                return

            for processed_string in list(processed_strings_to_find):
                if processed_string in row['ProcessedTitle']:
                    found_strings.add(
                        processed_strings_to_find[processed_string]
                    )
                    del processed_strings_to_find[processed_string]

    not_found_strings = set(strings_to_find) - found_strings

    if not_found_strings:
        print(RED + "Strings not found in the 'ProcessedTitle' column:" + RESET)  # noqa: E501
        for string in not_found_strings:
            print(RED + string + RESET)
    else:
        print(GREEN + "All strings were found in the 'ProcessedTitle' column." + RESET)  # noqa: E501


def process_string(s):
    """
    TODO
    """
    # Convert to lowercase and remove special characters
    s = s.lower()
    s = re.sub(r'[!@#$%^&*()_+\-=[\]\{};:\'",.<>?/~`|\\]+', '', s)
    return s


def read_strings_from_file(file_path):
    """
    TODO
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


def validate_results():
    """
    TODO
    """
    current_dir = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
    csv_file_path = os.path.normpath(
        os.path.join(current_dir, '..', 'data_results', 'unique_results.csv')
    )
    strings_file_path = os.path.normpath(
        os.path.join(current_dir, 'titles_to_validate.txt')
    )

    strings_to_find = read_strings_from_file(strings_file_path)
    find_strings_in_csv(csv_file_path, strings_to_find)
