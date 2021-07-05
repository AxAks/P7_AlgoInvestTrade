import re
from datetime import datetime
from itertools import combinations, combinations_with_replacement
from typing import Union, Callable, Any

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


def get_portfolio_average_roi(portfolio: tuple):
    """
    enables to calculate the raw Return on Investment of a portfolio
    helps calculate the ROI/Cost index of a portfolio
    """
    shares_roi_sum = 0
    for share in portfolio:
        # print(f"Share Name: {share['name']} , Cost: {share['cost']}, ROI: {share['roi']}")  # à enlever ensuite
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
    with open('tests/test.txt', 'r') as file:
        content = file.read()
    return content


def write_file(_input : str) -> None:
    """
    enables to write to the file to save data
    """
    with open('tests/test.txt', 'w') as file:
        file.write(_input)


def deserialize(portfolio_str: str, shares_list: list[dict]) -> tuple:
    """
    gets a string with the shares names of a portfolio
    and transforms them as a portfolio of shares object with the values : cost and roi
    """
    deserialized_portfolio = []
    for share_name in portfolio_str.split('-'):
        for share in shares_list:
            if share_name in share['name']:
                deserialized_portfolio.append(share)
    return tuple(deserialized_portfolio)


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
    timer_0 = datetime.now()
    if not secure:
        best_portfolio = ({})
        for shares_amount in range(scan_begin,
                                   scan_strength):  # attention strength = 21 s'il y a 20 action, c'est exclusif
            if replacement:
                generator = combinations_with_replacement(shares_list,
                                                          shares_amount)  # facultatif, par défaut en False
            else:
                generator = combinations(shares_list, shares_amount)

            for portfolio in generator:
                cost = get_portfolio_cost(portfolio)
                if _filter(cost):
                    print(f'Portfolio cost: {cost}')
                    acceptable_cost = cost
                    print(f'This Portfolio is acceptable: {portfolio} for {acceptable_cost}€ '
                          f'and a ROI of {get_portfolio_average_roi(portfolio) * 100}%.\n'
                          f'Let\'s compare it')
                    if not best_portfolio:
                        best_portfolio = portfolio
                        best_portfolio_cost = acceptable_cost
                        print(f'First Portfolio, automatically added: {best_portfolio}')
                    else:
                        best_portfolio_score = score(best_portfolio)
                        portfolio_score = score(portfolio)
                        print(
                            f'Previous Portfolio: {best_portfolio_score}% -VS- Current Portfolio: {portfolio_score}%')
                        if new_high_score(portfolio_score, best_portfolio_score):
                            best_portfolio = portfolio
                            best_portfolio_cost = acceptable_cost
                            print(f'New best Portfolio found: {best_portfolio}')
                else:
                    print(f'Portfolio cost: {cost}')
                    print(f'This Portfolio is NOT acceptable: {portfolio} for {cost}€\n'
                          f'Let\'s DROP it, Next !')

            if not best_portfolio:
                print('No portfolio was found under the investment limit !')
            else:
                print(f'Here is the Best Possible Portfolio of all :\n'
                      f' - Amount of shares: {len(best_portfolio)}\n'
                      f' - Portfolio Cost: {best_portfolio_cost}\n'
                      f' - Portfolio Details: {best_portfolio}\n'
                      f' - Portfolio average ROI after 2 years: {best_portfolio_score * 100}%')

    if secure:  # sauvegarde dans un fichier
        best_portfolio = deserialize(read_file(), shares)
        for shares_amount in range(scan_begin,
                                   scan_strength):  # attention strength = 21 s'il y a 20 action, c'est exclusif
            best_portfolio = deserialize(read_file(), shares)
            if replacement:
                generator = combinations_with_replacement(shares_list,
                                                          shares_amount)  # facultatif, par défaut en False
            else:
                generator = combinations(shares_list, shares_amount)
            for portfolio in generator:
                cost = get_portfolio_cost(portfolio)
                if _filter(cost):
                    print(f'Portfolio cost: {cost}')
                    acceptable_cost = cost
                    print(f'This Portfolio is acceptable: {portfolio} for {acceptable_cost}€ '
                          f'and a ROI of {score(portfolio) * 100}%.\n'
                          f'Let\'s compare it')
                    if not best_portfolio:
                        best_portfolio = portfolio
                        best_portfolio_cost = acceptable_cost
                        write_file(serialize(best_portfolio))
                        print(f'First Portfolio, automatically added: {best_portfolio}')
                    else:
                        best_portfolio_score = score(best_portfolio)
                        portfolio_score = score(portfolio)
                        print(
                            f'Previous Portfolio: {best_portfolio_score}% -VS- Current Portfolio: {portfolio_score}%')
                        if new_high_score(portfolio_score, best_portfolio_score):
                            best_portfolio = portfolio
                            best_portfolio_cost = acceptable_cost
                            write_file(serialize(best_portfolio))
                            print(f'New best Portfolio found: {best_portfolio}')
                else:
                    print(f'Portfolio cost: {cost}')
                    print(f'This Portfolio is NOT acceptable: {portfolio} for {cost}€\n'
                          f'Let\'s DROP it, Next !')

        if not best_portfolio:
            print('No portfolio was found under the investment limit !')
        else:
            print(f'Here is the Best Possible Portfolio of all :\n'
                  f' - Amount of shares: {len(best_portfolio)}\n'
                  f' - Portfolio Cost: {best_portfolio_cost}\n'
                  f' - Portfolio Details: {best_portfolio}\n'
                  f' - Portfolio average ROI after 2 years: {best_portfolio_score * 100}%')

    execution_time = datetime.now() - timer_0
    print(f' Execution Time = {execution_time}')
    return best_portfolio



# test samples
shares = sample_values.shares_list
test_portfolio = sample_values.test_portfolio
test_portfolio_to_serialize = sample_values.test_portfolio2

# functions execution
# portfolios = \
# main(shares, 3, 4, lambda x: x <= 500, get_portfolio_average_roi, secure=True)  # min et max ne peuvent pas etre egaux ca incl et excl pb autour de 17
#  15-16 OK, 15-17 OK -> best portfolio trouvé , 15-18 NOT OK -> pas de portfolio trouvé en dessous de 500€ !!!! why

print('Serialized')
portfolio_str = serialize(test_portfolio_to_serialize)
print(portfolio_str)
print('Deserialized')
deserialized_portfolio = deserialize(portfolio_str, sample_values.shares_list)
print(deserialized_portfolio)  # find_best_portfolio(shares)

# for portfolio in portfolios:
# get_portfolio_roi_cost_index(portfolio)
