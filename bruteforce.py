from itertools import combinations
from tests import sample_values

"""
recupérer la liste des actions via l'import d'un fichier csv ? 
"""

"""
Actions;Coût_par_action(euros);Bénéfice(après_2ans)
Action-1;20;5% 
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

Action-2;30;10%
Action-3;50;15%
"""

"""
total_cost = 0
while total_cost <= 500:
    total_cost += 1
    pass


def first_test(iterable, r):
    test = combinations(iterable, r)
    with open('tests/test.txt', 'a') as file:
        [file.write(str(f'{t}\n')) for t in test]
"""


def get_portfolio_score(portfolio):
    pass


def get_all_available_portfolios(actions_list, count):
    generator = combinations(actions_list, count)
    for portfolio in generator:
        # if sum
        print(portfolio)


actions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
           'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']


actions = sample_values.actions_list
for actions_amount in range(1, 2):
    get_all_available_portfolios(actions, actions_amount)


