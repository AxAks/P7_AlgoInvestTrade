"""
General functions to be re-used several times throughout the project
"""
import re

import pandas as pd


def get_portfolio_net_roi(portfolio: tuple) -> float:
    """
    Calculates the net return on Investment of a portfolio of shares
    """
    cost = get_portfolio_cost(portfolio)
    average_roi = get_portfolio_average_roi(portfolio)
    net_roi = cost * average_roi / 100
    return net_roi


def get_portfolio_cost(portfolio: tuple) -> float:
    """
    Calculates the cost of a given portfolio
    """
    portfolio_cost = 0
    for share in portfolio:
        portfolio_cost += share['cost']
    return portfolio_cost


def get_portfolio_average_roi(portfolio: tuple) -> float:
    """
    Calculates the return on Investment of a portfolio of shares
    """
    shares_roi_sum = 0
    for share in portfolio:
        shares_roi_sum += share['roi']
        portfolio_average_roi = shares_roi_sum / len(portfolio)
    return portfolio_average_roi


def serialize(portfolio: tuple) -> str:
    """
    gets a portfolio of shares a list of dict
    and returns the names of the shares in the portfolio as a string
    """
    portfolio_str = str([str(share['name']) for share in portfolio])
    cleaned_portfolio_str = re.sub(r"'| |\[|]", '', portfolio_str).replace(',', ', ')
    return cleaned_portfolio_str


def deserialize(portfolio_str: str, shares_list: list[dict]) -> tuple[dict]:
    """
    gets a string with the shares names of a portfolio
    and transforms them as a portfolio of shares object with the values : cost and roi
    """
    deserialized_portfolio = []
    for share_name in portfolio_str.split(', '):
        for share in shares_list:
            if share_name in share['name'] and share_name != '':
                deserialized_portfolio.append(share)
    return tuple(deserialized_portfolio)


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
        for row in df.itertuples(index=False) if row[price_index] > 0.0]
    return shares_list
