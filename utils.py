"""
General functions to be useful in any project
"""
import argparse


def url_args_parser():
    # récupéré de p2, à adapter pour selectionner le fichier CSV source avec la liste des actions depuis le terminal
    """
    Cette fonction permet de lancer le script depuis le terminal bash en mentionnant une URL en tant qu'argument.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="scrapes all the products URLs on the page given as argument", type=str)
    args = parser.parse_args()
    return args

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




