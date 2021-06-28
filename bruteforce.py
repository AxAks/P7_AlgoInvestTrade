from itertools import combinations
from typing import Union
import json

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
    with open('tests/test.txt', 'w') as file:
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


def get_all_possible_portfolios(actions_list: list[dict]) -> list[tuple]:  # à retravailler
    """
    returns all possible combinations of actions under the given criteria:
    - cost of portfolio under 500€
    - Actions only buyable once
    """
    all_possible_portfolios = []
    for actions_amount in range(1, 4): # à changer pour 21(pour arriver à 20 actions !) (tester en changeant les ranges de 1 à 21
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


def find_best_portfolio(actions_list: list[dict]):
    for actions_amount in range(17, 21):
        generator = combinations(actions_list, actions_amount)
        for portfolio in generator:
            portfolio_total_cost = 0
            for action in portfolio:
                portfolio_total_cost += action['cost']
                if portfolio_total_cost <= 500:
                    print(f'Great Portfolio under 500€: {portfolio_total_cost}€')
                    """
                    with open('tests/test.txt', 'r+') as file:
                        # voir s'il y a deja un portefeuille dans le fichier
                        # si oui comparer les deux 
                        # si le deuxieme a un meilleur indice de rentabilité remplacer le portefeuille enregistré dans le fichier 
                        previous_portfolio = file.read()
                        print(previous_portfolio)
                        if tuple(previous_portfolio) != () and \
                                get_average_roi(tuple(previous_portfolio)) <= get_average_roi(portfolio):
                            print(portfolio)  # à enlever ensuite
                            print(len(portfolio))  # à enlever ensuite
                            print("this portfolio is better than the previous one, let's keep it !")
                            
                            file.write(str(portfolio))
                        else:
                            print('oups !')
                            continue
                        """
                else:
                    print(f'this portfolio represents more than 500€ investment: {portfolio_total_cost}€')
                    print('grrr')

"""
# Program to show the use of lambda functions

double = lambda x: x * 2
print(double(5))
"""

# tests
actions = sample_values.actions_list
test_portfolio = sample_values.test_portfolio


# functions execution
#portfolios = get_all_possible_portfolios(actions)
find_best_portfolio(actions)
#for portfolio in portfolios:
#    get_average_roi(portfolio)
