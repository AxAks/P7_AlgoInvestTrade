"""
General functions to be re-used several times through the project
"""
import re
import pandas as pd


def serialize(portfolio: tuple) -> str:  # pas utilisé pour le moment
    portfolio_str = str([str(share['name']) for share in portfolio])
    cleaned_portfolio_str = re.sub(r"'| |\[|]", '', portfolio_str).replace(',', '-')
    return cleaned_portfolio_str


def deserialize(portfolio_str: str, shares_list: list[dict]) -> tuple:
    """
    gets a string with the shares names of a portfolio
    and transforms them as a portfolio of shares object with the values : cost and roi
    """
    deserialized_portfolio = []
    for share_name in portfolio_str.split('-'):
        for share in shares_list:
            if share_name in share['name'] and share_name != '':
                deserialized_portfolio.append(share)
    return tuple(deserialized_portfolio)


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