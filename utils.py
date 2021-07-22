"""
General functions to be useful in any project
"""


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
