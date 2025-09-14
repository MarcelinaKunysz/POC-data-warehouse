# file_utils.py

import glob
from config import *


def debug(msg):
    if LOG_LEVEL.upper() == "DEBUG":
        print(msg)


def load_numbers_from_txt():
    """Loads contract numbers from text file"""
    try:
        with open(CONTRACTS_FILE, "r", encoding=ENCODING) as file:
            numbers = []
            for line in file:
                number = line.strip()
                if number:
                    numbers.append(number)
            debug(f"Found the names of the Excel files. {numbers}")
            return numbers
    except FileNotFoundError:
        print(f"Error: File '{CONTRACTS_FILE}' not found")
        exit()


def find_excel_files():
    """Finds all Excel files in directory"""
    all_files = glob.glob(f"{SPREADSHEETS_PATH}/*{FILE_EXTENSION}")
    debug(f"Found the Excel files. {all_files}")
    return all_files


def find_file_for_contract(number, all_files):
    """Finds Excel file for specific contract number"""
    for file in all_files:
        if file.endswith(f"{number}{FILE_EXTENSION}"):
            debug("Found the contracts.")
            return file
    debug("No contracts found")
    return None


def find_all_contracts_with_files():
    """Finds all contracts and their corresponding files"""
    contract_numbers = load_numbers_from_txt()
    all_files = find_excel_files()

    found = []
    not_found = []

    for number in contract_numbers:
        file = find_file_for_contract(number, all_files)
        if file:
            found.append((number, file))
        else:
            not_found.append(number)

    return found, not_found
