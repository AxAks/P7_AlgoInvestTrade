import re
import logging

from datetime import datetime
from itertools import combinations, combinations_with_replacement
from typing import Callable, Any

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
    # >= on a le meme ROI mais avec plus d'actions
    # > -> on a le meme ROI avec un nombre d'actions moindre
    return new_score > previous_score


def read_file() -> str:
    """
    enables to read the file to load data
    """
    with open('results_backups/bruteforce_result_save.txt', 'r') as file:
        content = file.read()
    return content


def write_file(_input: str) -> None:
    """
    enables to write to the file to save data
    """
    with open('results_backups/bruteforce_result_save.txt', 'w') as file:
        file.write(_input)


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
    # pb s'il ne trouve pas le share_name dans la liste d'actions,
    # il ne l'ajoute pas dans le portefeuile,
    # mais ne retourne pas d'erreur


def serialize(portfolio: tuple) -> str:
    """
    gets a portfolio of shares with the values : name, cost and roi
    and transforms it into a string with the shares names of a portfolio
    """
    portfolio_str = str([str(share['name']) for share in portfolio])
    cleaned_portfolio_str = re.sub(r"'| |\[|]", '', portfolio_str).replace(',', '-')
    return cleaned_portfolio_str


def main(shares_list: list[dict],
         scan_begin: int, scan_strength: int, _filter: Callable[[Any], bool], score: Callable[[Any], float],
         replacement: bool = False, secure: bool = False) -> list[tuple]:  # à retravailler
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

    for shares_amount in range(scan_begin, scan_strength):
        # attention strength = 21 s'il y a 20 action, c'est exclusif
        if shares_amount != 1:
            logging.info(f'Latest scan step proceeded: {shares_amount - 1}')
        if replacement:
            generator = combinations_with_replacement(shares_list, shares_amount)
            # facultatif, par défaut en False
        else:
            generator = combinations(shares_list, shares_amount)
        logging.info(f'Beginning scan step {shares_amount}')
        for portfolio in generator:
            portfolio_str = serialize(portfolio)
            print(f'Processing Portfolio: {portfolio_str}')
            cost = get_portfolio_cost(portfolio)
            if _filter(cost):
                print('KEEP !')
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

    logging.info(f'Latest scan step proceeded: {shares_amount}')
    logging.info(f'Scan End: {datetime.now()}')
    logging.info(f'Scan Result : Best Portfolio -> {serialize(best_portfolio)}')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    print(f'Execution Time = {execution_time}')
    return best_portfolio


# test samples
shares = sample_values.shares_list
# Ou est ce qu'on doit recupérer la lsite des actions à traiter ?
# depuis un fichier, code à adapter

if __name__ == "__main__":  #  min et max ne peuvent pas etre egaux ca incl et excl
    main(shares, 1, 21, lambda x: x <= 500, get_portfolio_net_roi, secure=True)
