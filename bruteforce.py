from itertools import combinations
from typing import Union

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
    (profil prudent: investir moins, moins de rentabilité, profil risque: investir plus: gain possible plus grands, quel choix)
    mettre la possibilité d'ajouter un parametre de choix de "type de profil, type d'investisseur"?
    dans un 1er temps, on reste sur le pourcentage de rentabilité pour faire simple
        -> si premier en dessous de la limite de montant on garde(pas de comparaison possible), si suivant, on compare avec le précedent.
        -> on ne garde que celui qui a le meilleur score sur les deux portefeuilles
"""

"""
# juste un test à supprimer!
def first_test(iterable, r):
    test = combinations(iterable, r)
    with open('tests/test.txt', 'a') as file:
        [file.write(str(f'{t}\n')) for t in test]
"""


def get_average_roi(portfolio: Union[tuple, list]):  # peut etre juste tuple en fait
    """
    enables to evaluate the Return on investment of the portfolio after two years
    """
    actions_roi_sum = 0
    # portfolio_total_cost = 0   #  ajouter la notion de cout du portefeuille dans le calcul de l'indice ? si oui comment ?
    for action in portfolio:
        print(action['roi'])  # à enlever ensuite
        actions_roi_sum += action['roi']
        # print(action['cost'])
        # portfolio_total_cost += action['cost']
    portfolio_average_roi = actions_roi_sum / len(portfolio)

    print(portfolio_average_roi)  # à enlever ensuite
    return portfolio_average_roi


def get_all_possible_portfolios(actions_list: list[dict]):  # à retravailler
    """
    returns all possible combinations of actions under the given criteria:
    - cost of portfolio under 500€
    - Actions only buyable once
    """
    all_possible_portfolios = []
    for actions_amount in range(1, 4): # à changer pour 21(pour arriver à 20 actions !) (pour tester changer les range entre 1 et 21
        generator = combinations(actions_list, actions_amount)
        for portfolio in generator:
            portfolio_total_cost = 0
            for action in portfolio:
                portfolio_total_cost += action['cost']
                if portfolio_total_cost <= 500:
                    print(f'Great Portfolio under 500€: {portfolio_total_cost}€')
                    all_possible_portfolios.append(portfolio)
                    print(portfolio)  # à enlever ensuite
                    print(len(portfolio))  # à enlever ensuite
                else:
                    print(f'this portfolio represents more than 500€ investment: {portfolio_total_cost}€')
    print(len(all_possible_portfolios))  # à enlever ensuite
    return all_possible_portfolios


# tests
actions = sample_values.actions_list
test_portfolio = sample_values.test_portfolio


# functions execution
get_all_possible_portfolios(actions)
get_average_roi(test_portfolio)
