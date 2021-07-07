"""
à rediger / optimisation !
"""
import re
import logging
from datetime import datetime
from itertools import combinations, combinations_with_replacement
from typing import Callable, Any

from tests import sample_values

logging.basicConfig(filename="optimized.log", level=logging.INFO, filemode='w')
"""
recupérer la liste des actions via l'import d'un fichier csv ? 
"""

"""
algo glouton : http://nsi4noobs.fr/ PDF exemple/explication
Une méthode approchée a pour but de trouver une solution avec un bon compromis entre la qualité de la
solution et le temps de calcul. Pour le problème du sac à dos, voici un exemple d’algorithme de ce type :
• calculer le rapport (vi / mi) pour chaque objet i ;
• trier tous les objets par ordre décroissant de cette valeur ;
• sélectionner les objets un à un dans l’ordre du tri et ajouter l’objet sélectionné dans le sac si le poids
maximal reste respecté.

=>
-> obtenir la liste des actions et leurs caracteristiques (nom, cout, rentablitité)
    -> pour chaque action:
        -> calculer le rapport: Net Roi / Share cost (score)
        -> trier les actions par score decroissant (liste)
        -> sélectionner les actions et ajouter au portfeuille tant que le cout maximal autorisé du portfeuille 
        n'est pas atteint
"""


def fill_portfolio(sorted_shares_list: list) -> tuple:
    """
    Fill a portfolio with shares according to the space left in the portfolio
     .... (to be detailled !)
    """
    print(sorted_shares_list)
    portfolio = []
    portfolio_cost = 0.0
    portfolio_net_roi = 0.0
    n = 0
    while portfolio_cost <= 500.0:
        print(n)
        if portfolio_cost + get_share_cost(sorted_shares_list[n]) <= 500.0:
            portfolio.append(sorted_shares_list[n])
        portfolio_cost = get_portfolio_cost(portfolio)
        portfolio_net_roi = round(get_portfolio_net_roi(portfolio), 2)
        print(portfolio)
        print(portfolio_cost)
        print(portfolio_net_roi)
        n += 1

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

#  -> sélectionner les actions et ajouter au portfeuille tant que le cout maximal autorisé du portfeuille n'est pas atteint
#  la limite est le cout du portefeuille (500€)


def main(shares_list):
    sorted_shares_list = get_sorted_shares_list(shares_list)
    final_portfolio = fill_portfolio(sorted_shares_list)
    print(final_portfolio)
    return final_portfolio


if __name__ == "__main__":
    main(sample_values.shares_list)



"""
def get_portfolio_cost(portfolio: tuple):
    portfolio_cost = 0
    for share in portfolio:
        portfolio_cost += share['cost']
    return portfolio_cost


def get_portfolio_net_roi(portfolio: tuple):
    cost = get_portfolio_cost(portfolio)
    average_roi = get_portfolio_average_roi(portfolio)
    net_roi = cost * average_roi
    return net_roi


def get_portfolio_average_roi(portfolio: tuple):
    shares_roi_sum = 0
    for share in portfolio:
        shares_roi_sum += share['roi']
        portfolio_average_roi = round(shares_roi_sum / len(portfolio), 5)
    return portfolio_average_roi


def new_high_score(new_score: float, previous_score: float) -> bool:
    # >= on a le meme ROI mais avec plus d'actions
    # > -> on a le meme ROI avec un nombre d'actions moindre
    return new_score > previous_score


def read_file() -> str:
    with open('results_save.txt', 'r') as file:
        content = file.read()
    return content


def write_file(_input: str) -> None:
    with open('results_save.txt', 'w') as file:
        file.write(_input)


def deserialize(portfolio_str: str, shares_list: list[dict]) -> tuple:
    deserialized_portfolio = []
    for share_name in portfolio_str.split('-'):
        for share in shares_list:
            if share_name in share['name'] and share_name != '':
                deserialized_portfolio.append(share)
    return tuple(deserialized_portfolio)
    # pb s'il ne trouve pas le share_name dans la liste d'actions,
    # il ne l'ajoute pas dans le portefeuile,
    # mais ne retourne pas d'erreur


def serialize(portfolio: tuple) -> str:
    portfolio_str = str([str(share['name']) for share in portfolio])
    cleaned_portfolio_str = re.sub(r"'| |\[|]", '', portfolio_str).replace(',', '-')
    return cleaned_portfolio_str


def main(shares_list: list[dict],
         scan_begin: int, scan_strength: int, _filter: Callable[[Any], bool], score: Callable[[Any], float],
         replacement: bool = False, secure: bool = False) -> list[tuple]:  # à ooptimiser !
    timer_0 = datetime.now()
    logging.info(f'Scan Start: {datetime.now()}')
    best_portfolio = ({})
    best_portfolio_cost = 0.0
    best_portfolio_roi = 0.0
    best_portfolio_score = 0.0
    if secure:
        logging.info('Secure Mode On -> saving results in file')
        # sauvegarde dans un fichier
        best_portfolio = deserialize(read_file(), shares)
        if best_portfolio:
            best_portfolio_cost = get_portfolio_cost(best_portfolio)
            best_portfolio_roi = get_portfolio_average_roi(best_portfolio)
            best_portfolio_score = score(best_portfolio)

    else:
        logging.info('Secure Mode Off -> no writing in a file')

    for shares_amount in range(scan_begin, scan_strength):
        # attention strength = 21 s'il y a 20 action, c'est exclusif
        if replacement:
            generator = combinations_with_replacement(shares_list, shares_amount)
            # facultatif, par défaut en False
        else:
            generator = combinations(shares_list, shares_amount)
        n = 1
        logging.info(f'Scan Step {shares_amount}')
        for portfolio in generator:
            portfolio_str = serialize(portfolio)
            print(f'Processing Portfolio #{n} : {portfolio_str}')
            n += 1
            cost = get_portfolio_cost(portfolio)
            if _filter(cost):
                acceptable_cost = cost
                if not best_portfolio:
                    best_portfolio = portfolio
                    best_portfolio_cost = acceptable_cost
                    best_portfolio_score = get_portfolio_net_roi(portfolio)
                    print(f'New best Portfolio: {best_portfolio}, '
                          f'Cost: {best_portfolio_cost} '
                          f'Net ROI: {best_portfolio_score}')
                    if secure:
                        write_file(serialize(best_portfolio))

                else:
                    best_portfolio_score = round(score(best_portfolio), 2)
                    portfolio_score = round(score(portfolio), 2)
                    if new_high_score(portfolio_score, best_portfolio_score):
                        best_portfolio = portfolio
                        best_portfolio_cost = acceptable_cost
                        best_portfolio_score = portfolio_score
                        print(f'-> New High: {best_portfolio_score}€')
                        if secure:
                            write_file(serialize(best_portfolio))

            else:
                print('DROP !')

    if best_portfolio:
        print(f'\nHere is the Best Possible Portfolio of all:\n'
              f'- Investment: {best_portfolio_cost}\n'
              f'- Portfolio Average ROI: {round(best_portfolio_roi * 100, 2)} %\n'
              f'- Net ROI after 2 years: {best_portfolio_score} €\n'
              f'- Portfolio: {serialize(best_portfolio)} ({len(best_portfolio)} Shares)\n'
              f'- Details: {best_portfolio}\n')

    else:
        print('No portfolio was found under the investment limit !')

    execution_time = datetime.now() - timer_0
    print(f' Execution Time = {execution_time}')
    logging.info(f'Scan End: {datetime.now()}')
    logging.info(f'Scan Result : Best Portfolio -> {serialize(best_portfolio)}')
    return best_portfolio


# test samples
shares = sample_values.shares_list
# Ou est ce qu'on doit recupérer la lsite des actions à traiter ?
# depuis un fichier, code à adapter
"""

"""
# functions execution
main(shares, 1, 21, lambda x: x <= 500, get_portfolio_net_roi, secure=False)
#  min et max ne peuvent pas etre egaux ca incl et excl
"""

"""
if __name__ == "__main__":
    main(shares, 1, 21, lambda x: x <= 500, get_portfolio_net_roi, secure=True)
"""