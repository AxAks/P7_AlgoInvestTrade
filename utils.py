"""
General functions to be re-used several times through the project
"""
import pandas as pd


def read_file(file: str) -> str:
    """
    enables to read the file to load data
    """
    with open(file, 'r') as file:
        content = file.read()
    return content


def write_file(_input: str) -> None:
    """
    enables to write to the file to save data
    """
    with open('results_backups/bruteforce_result_save.txt', 'w') as file:
        file.write(_input)


def from_csv_to_list_of_dict(csv_file: str, sep: str = ',') -> list[dict]:
    """
    reads a csv file with a list of shares with respective information
    and returns the list of shares as a list of dicts
    """
    df = pd.read_csv(csv_file, sep)
    name_index = 0
    price_index = 1
    profit_index = 2
    shares_list = [
        {'name': row[name_index], 'cost': row[price_index], 'roi': row[profit_index]}
        for row in df.itertuples(index=False)]
    return shares_list