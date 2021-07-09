import re
import logging

from datetime import datetime

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
    # pb s'il ne trouve pas le share_name dans la liste d'actions,
    # il ne l'ajoute pas dans le portefeuile,
    # mais ne retourne pas d'erreur


def serialize(portfolio: tuple) -> str:  # pas utilisé pour le moment
    portfolio_str = str([str(share['name']) for share in portfolio])
    cleaned_portfolio_str = re.sub(r"'| |\[|]", '', portfolio_str).replace(',', '-')
    return cleaned_portfolio_str


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
        if portfolio_cost + get_share_cost(sorted_shares_list[n]) <= 500.0:
            print(f'\nPortfolio cost limit not reached, new share added: {next_share_name}:')
            portfolio.append(sorted_shares_list[n])
            portfolio_cost = get_portfolio_cost(portfolio)
            portfolio_net_roi = round(get_portfolio_net_roi(portfolio), 2)
            portfolio_average_roi = round(get_portfolio_average_roi(portfolio), 2) * 100
            print(f'Portfolio: {serialize(portfolio)}')
            print(f'Cost: {portfolio_cost} €')
            print(f'Relative ROI: {portfolio_average_roi} %')
            print(f'Net ROI: {portfolio_net_roi} €')
        n += 1
    print(f'\nOptimized portfolio found: {serialize(portfolio)} ({len(portfolio)} shares) '
          f'for a cost of: {portfolio_cost} € investment\n'
          f'-> Relative ROI: {portfolio_average_roi} %\n'
          f'-> Net ROI after two years: {portfolio_net_roi} €')
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


def get_sorted_shares_list(shares_list: list) -> list:
    """
    returns a list of shares sorted from higher to lower score (net ROI)
    """
    return sorted(shares_list, key=lambda share: get_share_score(share), reverse=True)


def get_share_cost(share: dict) -> float:
    """
    Give the cost of a specific share
    """
    return share['cost']


def get_share_score(share: dict) -> float:
    """
    Calculate the net return on investment for a specific share
    """
    return round(get_share_cost(share) * share['roi'], 5)


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


shares = sample_values.shares_list

if __name__ == "__main__":
    main(shares)

"""
def read_file() -> str:
    with open('results_backups/optimized_result_save.txt', 'r') as file:
        content = file.read()
    return content


def write_file(_input: str) -> None:
    with open('results_backups/optimized_result_save.txt', 'w') as file:
        file.write(_input)
"""
