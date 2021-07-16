"""
General functions to be useful in any project
"""

import argparse


def csv_filepath_args_parser():
    """
    This function enables to launch a script with a CSV filepath as an argument.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_filepath", help="enter the path of your CSV file", type=str)
    args = parser.parse_args()
    return args.csv_filepath


def read_file(file: str) -> str:
    """
    enables to read the file to load data
    """
    with open(file, 'r') as file:
        content = file.read()
    return content


def write_file(file: str, _input: str) -> None:
    """
    enables to write to the file to save data
    """
    with open(file, 'w') as file:
        file.write(_input)
