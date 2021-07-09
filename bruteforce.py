import logging

from datetime import datetime
from itertools import combinations, combinations_with_replacement
from typing import Callable, Any

from utils import read_file, write_file, serialize, deserialize, from_csv_to_list_of_dict

from tests import sample_values

"""
recupérer la liste des actions via l'import d'un fichier csv ? 
"""

"""
-> obtenir la liste des actions et leurs caracteristiques (nom, cout, rentablitité)
-> lancer le process pour trouver toutes les combinaisons possibles
(donner un nom a chaque portfolio ou pas besoin?)
-> pour chaque combinaison:
    -> verifier la limite de montant.
        -> Si au dessus, on vire , si en dessous on garde (+ ou - 500€)
    -> calculer le score de rentablitié (gains nets /invest "ROI")
    (quid de l'investissement de départ, depend du client/choix !!)
    (profil prudent: investir moins, moins de rentabilité, profil risque: investir plus: gain possible plus grands,
    quel choix)
    mettre la possibilité d'ajouter un parametre de choix de "type de profil, type d'investisseur"?
    dans un 1er temps, on reste sur le pourcentage de rentabilité pour faire simple
        -> si premier en dessous de la limite de montant on garde(pas de comparaison possible), si suivant,
         on compare avec le précedent.
        -> on ne garde que celui qui a le meilleur score sur les deux portefeuilles

je voulais prendre en compte le cout d'investissement de départ (mais à revoir, pas utile pour le projet) 
// donner ensuite la possibilité de choix entre option : profil prudent/ profil prise de risque
-> favoriser un cout d'investimment moindre OU favoriser le profit maximum meme si le cout de déparrt est plus elevé 
"""


def get_portfolio_cost(portfolio: tuple):
    """
    calculates the total cost of a portfolio based on the shares prices
    Helps to calculate the Return on Investment after two years
    """
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
    """
    enables to calculate the average Return on Investment ratio of a portfolio
    helps calculate the net Return on Investment in Euros of a portfolio
    """
    shares_roi_sum = 0
    for share in portfolio:
        shares_roi_sum += share['roi']
        portfolio_average_roi = round(shares_roi_sum / len(portfolio), 5)
    return portfolio_average_roi


def new_high_score(new_score: float, previous_score: float) -> bool:
    """
    checks whether the new portfolio score is higher
    than the previously registered portfolio score
    """
    return new_score > previous_score


def main(shares_list: list[dict],
         scan_strength: int, _filter: Callable[[Any], bool], score: Callable[[Any], float],
         replacement: bool = False, secure: bool = False, scan_begin: int = 1) -> list[tuple]:
    """
    Returns all possible combinations of shares under the given criteria:
    - Cost of portfolio under 500€
    - Share only buyable once
    - Share cannot be sold partially
    Give the possibility to choose whether an share can be
    bought several times (if needed later for evolution)
    By default, the best result is saved in a variable,
    the Option Secure enables to save the result in a .txt file
    """
    logging.basicConfig(filename="logs/bruteforce.log", level=logging.INFO, filemode='w')
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

    for shares_amount in range(scan_begin, scan_strength + 1):
        if shares_amount != 1:
            logging.info(f'Latest scan step proceeded: {shares_amount - 1}')
        if replacement:
            generator = combinations_with_replacement(shares_list, shares_amount)
        else:
            generator = combinations(shares_list, shares_amount)
        logging.info(f'Beginning scan step {shares_amount}')
        for portfolio in generator:
            portfolio_str = serialize(portfolio)
            print(f'Processing Portfolio: {portfolio_str}')
            cost = get_portfolio_cost(portfolio)
            if _filter(cost):
                acceptable_cost = cost
                if not best_portfolio:
                    best_portfolio = portfolio
                    best_portfolio_cost = acceptable_cost
                    best_portfolio_score = get_portfolio_net_roi(portfolio)
                    logging.info(f'-> New High: {best_portfolio_score} €')
                    if secure:
                        write_file(serialize(best_portfolio))

                else:
                    best_portfolio_score = round(score(best_portfolio), 2)
                    portfolio_score = round(score(portfolio), 2)
                    if new_high_score(portfolio_score, best_portfolio_score):
                        best_portfolio = portfolio
                        best_portfolio_cost = acceptable_cost
                        best_portfolio_score = portfolio_score
                        print(f'-> New High: {best_portfolio_score} €')
                        logging.info(f'-> New High: {best_portfolio_score} €')
                        if secure:
                            write_file(serialize(best_portfolio))

    if best_portfolio:
        print(f'\nHere is the Best Possible Portfolio of all:\n'
              f'- Investment: {best_portfolio_cost}\n'
              f'- Portfolio Average ROI: {round(best_portfolio_roi * 100, 2)} %\n'
              f'- Net ROI after 2 years: {round(best_portfolio_score, 2)} €\n'
              f'- Portfolio: {serialize(best_portfolio)} ({len(best_portfolio)} Shares)\n'
              f'- Details: {best_portfolio}\n')

    else:
        print('No portfolio was found under the investment limit !')

    logging.info(f'Latest scan step proceeded: {shares_amount}')
    logging.info(f'Scan End: {datetime.now()}')
    logging.info(f'Scan Result : Best Portfolio -> {serialize(best_portfolio)} '
                 f'(Net ROI: {round(get_portfolio_net_roi(best_portfolio), 2)} €)')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    print(f'Execution Time = {execution_time}')
    return best_portfolio


# test samples
# shares = sample_values.shares_list



if __name__ == "__main__":
    shares = from_csv_to_list_of_dict('tests/initial_values.csv', sep=';')
    main(shares, 4, lambda x: x <= 500, get_portfolio_net_roi)
    # print(from_csv_to_list_of_dict(r'tests/dataset1_Python+P7.csv'))
    # print(from_csv_to_list_of_dict(r'tests/dataset2_Python+P7.csv'))
