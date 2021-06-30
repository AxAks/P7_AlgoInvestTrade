from itertools import combinations, combinations_with_replacement
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
    with open('tests/test.txt', 'w') as file:
        [file.write(str(f'{t}\n')) for t in test]
"""


def get_average_roi(portfolio: Union[tuple, list]):  # peut etre juste tuple en fait
    """
    enables to evaluate the Return on investment of the portfolio after two years
    """
    shares_roi_sum = 0
    # portfolio_total_cost = 0   #  ajouter la notion de cout du portefeuille dans le calcul de l'indice ? si oui comment ?
    for share in portfolio:
        print(f"Share Name: {share['name']} , Cost: {share['cost']}, ROI: {share['roi']}")  # à enlever ensuite
        shares_roi_sum += share['roi']
        # portfolio_total_cost += share['cost']
    portfolio_average_roi = shares_roi_sum / len(portfolio)
    print(f"Portfolio Average ROI: {portfolio_average_roi}\n")  # à enlever ensuite
    return portfolio_average_roi


def get_all_possible_portfolios(shares_list: list[dict], replacement: bool = False) -> list[tuple]:  # à retravailler
    """
    Returns all possible combinations of shares under the given criteria:
    - Cost of portfolio under 500€
    - Share only buyable once
    - Share cannot be sold partially
    Give the possibility to choose whether an share can be
    bought several times (if needed later for evolution)
    """
    all_possible_portfolios = []
    for shares_amount in range(1, 3): # à changer pour (1, 21) (pour arriver à 20 shares !) (tester en changeant les ranges de 1 à 21
        if replacement:
            generator = combinations_with_replacement(shares_list, shares_amount)
        else:
            generator = combinations(shares_list, shares_amount)
        for portfolio in generator:
            portfolio_total_cost = 0
            for share in portfolio:
                portfolio_total_cost += share['cost']
            if portfolio_total_cost <= 500:
                print(f'Great Portfolio under 500€: {portfolio_total_cost}€')
                all_possible_portfolios.append(portfolio)
                print(portfolio)  # à enlever ensuite
                print(len(portfolio))  # à enlever ensuite
            else:
                print(f'this portfolio represents more than 500€ investment: {portfolio_total_cost}€')
    print(f'Amount of Possible Portfolios: {len(all_possible_portfolios)}')  # à enlever ensuite
    return all_possible_portfolios


def find_best_portfolio(shares_list: list[dict]):  # ajouter notions de filtre montant fortefeuille et de score via des lambdas
    for shares_amount in range(17, 21):
        generator = combinations(shares_list, shares_amount)
        acceptable_portfolios_list = []
        for portfolio in generator:
            portfolio_cost = lambda x: sum([x['cost']])
            if portfolio_cost <= 500:
                print(f'Great Portfolio under 500€: {portfolio_cost}€')
                acceptable_portfolios_list.append(portfolio)
                # keep !
                # une fonction lambda pour voir si le portefeuille est acceptable
                # une fonction lambda pour definir son score de rentabilité
            else:
                print(f'this portfolio represents more than 500€ investment: {portfolio_cost}€')
                print('grrr')
                # skip automatically !
    return acceptable_portfolios_list


    """
    with open('tests/test.txt', 'r+') as file:
        # voir s'il y a deja un portefeuille dans le fichier
        # si oui comparer les deux 
        # si le deuxieme a un meilleur indice de rentabilité remplacer le portefeuille enregistré dans le fichier 
        previous_portfolio = file.read()
        print(previous_portfolio)
        if tuple(previous_portfolio) != ():
            if get_average_roi(tuple(previous_portfolio)) <= get_average_roi(portfolio):
                print(portfolio)  # à enlever ensuite
                print(len(portfolio))  # à enlever ensuite
                print("this portfolio is better than the previous one, let's keep it !")

                file.write(str(portfolio))
                print('portfolio saved')
            else:
                print('oups !')
                continue
        else:
            file.write(str(portfolio))
            print('portfolio saved')
    """



"""
# Program to show the use of lambda functions

double = lambda x: x * 2
print(double(5))
"""

# test samples
shares = sample_values.shares_list
test_portfolio = sample_values.test_portfolio


# functions execution
portfolios = get_all_possible_portfolios(shares)
#find_best_portfolio(shares)
for portfolio in portfolios:
    get_average_roi(portfolio)
