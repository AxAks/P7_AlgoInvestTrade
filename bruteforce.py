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


def get_portfolio_roi_cost_index(portfolio: tuple):  # faux !? ce qui compte c'est pas le ratio, mais le montant réél initial en euros
    """
    enables to evaluate the Return on investment of the portfolio after two years
    takes into account the initial cost of the portfolio
    """
    portfolio_average_roi = get_portfolio_average_roi(portfolio)
    portfolio_cost = get_portfolio_cost(portfolio)
    portfolio_roi_cost_index = round(portfolio_average_roi / portfolio_cost, 6)
    print(f'Portfolio Cost: {portfolio_cost}')  # à enlever ensuite
    print(f"Portfolio Average ROI: {portfolio_average_roi}")  # à enlever ensuite
    print(f"Portfolio ROI/Cost index : {portfolio_roi_cost_index}\n")  # à enlever ensuite
    return portfolio_roi_cost_index


def get_portfolio_average_roi(portfolio: tuple):
    """
    enables to calculate the raw Return on Investment of a portfolio
    helps calculate the ROI/Cost index of a portfolio
    :param portfolio:
    :return: portfolio_average_roi
    """
    shares_roi_sum = 0
    for share in portfolio:
        print(f"Share Name: {share['name']} , Cost: {share['cost']}, ROI: {share['roi']}")  # à enlever ensuite
        shares_roi_sum += share['roi']
        portfolio_average_roi = round(shares_roi_sum / len(portfolio), 4)
    return portfolio_average_roi


def get_portfolio_cost(portfolio: tuple):
    #  ajouter la notion de cout du portefeuille dans le calcul de l'indice ? si oui comment ?
    #  si on garde, expliquer la formule average_roi / portfolio_cost et voir comment on selectionne le meilleur indice cost/ROI
    """
    calculates the total cost of a portfolio based on the shares prices
    Helps to calculate the Return on Investment after two years
    """
    portfolio_cost = 0
    for share in portfolio:
        portfolio_cost += share['cost']
    return portfolio_cost


def filter_cost_acceptable_portfolio(portfolio: tuple):
    """
    Checks whether a portfolio is under 500€ or not
    :param portfolio:
    :return:
    """
    portfolio_cost = get_portfolio_cost(portfolio)
    if portfolio_cost <= 500:
        print(f'Great Portfolio under 500€: {portfolio_cost}€')
        print(portfolio)  # à enlever ensuite
        print(len(portfolio))  # à enlever ensuite
        return portfolio
    else:
        print(f'this portfolio represents more than 500€ investment: {portfolio_total_cost}€')
        return False


def find_best_portfolio(shares_list: list[dict], replacement: bool = False) -> list[tuple]:  # à retravailler
    """
    Returns all possible combinations of shares under the given criteria:
    - Cost of portfolio under 500€
    - Share only buyable once
    - Share cannot be sold partially
    Give the possibility to choose whether an share can be
    bought several times (if needed later for evolution)
    """
    for shares_amount in range(1, 2):
    #  à changer pour (1, 21) (pour arriver à 20 shares !) (tester en changeant les ranges de 1 à 21
        if replacement:
            generator = combinations_with_replacement(shares_list, shares_amount)  # facultatif, par défaut en False
        else:
            generator = combinations(shares_list, shares_amount)
        all_acceptable_portfolios = []
        for portfolio in generator:
            if portfolio:
                all_acceptable_portfolios.append(filter_cost_acceptable_portfolio(portfolio))
        print(f'Amount of Possible Portfolios: {len(all_acceptable_portfolios)}\n')  # à enlever ensuite
        for portfolio in all_acceptable_portfolios:
            get_portfolio_roi_cost_index(portfolio)

    return all_acceptable_portfolios







"""
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
# portfolios = \
find_best_portfolio(shares)

#find_best_portfolio(shares)
#for portfolio in portfolios:
#    get_portfolio_roi_cost_index(portfolio)
