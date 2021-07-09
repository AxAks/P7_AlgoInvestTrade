import logging

from datetime import datetime

from utils import deserialize, serialize, from_csv_to_list_of_dict
from tests import sample_values

"""
recupérer la liste des actions via l'import d'un fichier csv ? 
"""
"""
algo glouton =>
-> obtenir la liste des actions et leurs caracteristiques (nom, cout, rentablitité)
    -> pour chaque action:
        -> calculer le rapport: Net Roi / Share cost (score)
        -> trier les actions par score decroissant (liste)
        -> sélectionner les actions et ajouter au portfeuille tant que le cout maximal autorisé du portfeuille 
        n'est pas atteint
"""


def deserialize(portfolio_str: str, shares_list: list[dict]) -> tuple:  # pas utilisé pour le moment
    deserialized_portfolio = []
    for share_name in portfolio_str.split('-'):
        for share in shares_list:
            if share_name in share['name'] and share_name != '':
                deserialized_portfolio.append(share)
    return tuple(deserialized_portfolio)


def fill_portfolio(sorted_shares_list: list) -> tuple:
    """
    Fill a portfolio with shares according to the space left in the portfolio
     .... (to be detailled !)
    """
    portfolio = []
    portfolio_cost = 0.0
    portfolio_average_roi = 0.0
    n = 0
    while portfolio_cost <= 500.0 and n < len(sorted_shares_list):
        next_share_name = sorted_shares_list[n]['name']
        if portfolio_cost + get_share_cost(sorted_shares_list[n]) <= 500.0 \
                and get_share_score(sorted_shares_list[n]) != 0.0:
            print(f'\nPortfolio cost limit not reached, new share added: {next_share_name}:')
            portfolio.append(sorted_shares_list[n])
            portfolio_cost = get_portfolio_cost(portfolio)
            portfolio_net_roi = round(get_portfolio_net_roi(portfolio), 2)
            portfolio_average_roi = round(get_portfolio_average_roi(portfolio), 2)
            print(f'Portfolio: {serialize(portfolio)}')
            print(f'Cost: {portfolio_cost} €')
            print(f'Relative ROI: {portfolio_average_roi} %')
            print(f'Net ROI after two years: {round(portfolio_net_roi / 100, 2)} €')
        n += 1
    print(f'\nOptimized portfolio found ({len(portfolio)} shares): {serialize(portfolio)} '
          f'for a cost of: {portfolio_cost} € investment\n'
          f'-> Relative ROI: {portfolio_average_roi} %\n'
          f'-> Net ROI after two years: {round(portfolio_net_roi / 100, 2)} €')
    return tuple(portfolio)


def get_portfolio_average_roi(portfolio: tuple):
    """
    Calculates the return on Investment of a portfolio of shares as a ratio
    """
    shares_roi_sum = 0
    for share in portfolio:
        shares_roi_sum += share['roi']
        portfolio_average_roi = round(shares_roi_sum / len(portfolio), 5)
    return portfolio_average_roi


def get_portfolio_net_roi(portfolio: tuple):
    """
    Calculates the net return on Investment of a portfolio of shares
    """
    cost = get_portfolio_cost(portfolio)
    average_roi = get_portfolio_average_roi(portfolio)
    net_roi = cost * average_roi
    return net_roi


def get_portfolio_cost(portfolio: tuple) -> float:
    """
    Calculates the cost of a given portfolio
    """
    portfolio_cost = 0
    for share in portfolio:
        portfolio_cost += share['cost']
    return portfolio_cost


def get_share_cost(share: dict) -> float:
    """
    Give the cost of a specific share
    """
    if share:
        return share['cost']


def get_share_score(share: dict) -> float:
    """
    Calculate the net return on investment for a specific share
    """
    if not share:
        return 0.0
    else:
        return round(get_share_cost(share) * share['roi'], 5)


def get_sorted_shares_list(shares_list: list) -> list:
    """
    returns a list of shares sorted from higher to lower score (net ROI)
    """
    return sorted(shares_list, key=lambda share: get_share_score(share), reverse=True)


def main(shares_list):
    logging.basicConfig(filename="logs/optimized.log", level=logging.INFO, filemode='w')
    timer_0 = datetime.now()
    logging.info(f'Scan Start: {datetime.now()}')
    sorted_shares_list = get_sorted_shares_list(shares_list)
    final_portfolio = fill_portfolio(sorted_shares_list)
    logging.info(f'Scan End: {datetime.now()}')
    final_portfolio_net_roi = get_portfolio_net_roi(final_portfolio)
    logging.info(f'Scan Result : Best Portfolio -> {serialize(final_portfolio)} '
                 f'(Net ROI: {final_portfolio_net_roi} €)')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    print(f'\nExecution Time = {execution_time}')
    return final_portfolio

"""
il faudrait pouvoir choisir le fichier (le passer en arg dans le terminal)...
"""
# shares_list = sample_values.shares_list
# shares_list = from_csv_to_list_of_dict('tests/initial_values.csv')
shares_list = from_csv_to_list_of_dict('tests/dataset2_Python+P7.csv')

if __name__ == "__main__":
    main(shares_list)
