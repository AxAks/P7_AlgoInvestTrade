from datetime import datetime
from itertools import combinations
from typing import Callable, Any

from utils import csv_filepath_args_parser
from commons import serialize, from_csv_to_list_of_dict, get_portfolio_cost, get_portfolio_average_roi, \
    get_portfolio_net_roi


def new_high_score(new_score: float, previous_score: float) -> bool:
    """
    checks whether the new portfolio score is higher
    than the previously registered portfolio score
    """
    return new_score > previous_score


def main(_filter: Callable[[Any], bool], score: Callable[[Any], float],
         scan_begin: int = 1, scan_strength: int = 20) -> list[tuple]:
    """
    Returns all possible combinations of shares under the given criteria
    """
    timer_0 = datetime.now()
    csv_filepath = csv_filepath_args_parser()
    shares_list = from_csv_to_list_of_dict(csv_filepath)
    best_portfolio = ({})
    best_portfolio_cost = 0.0
    best_portfolio_roi = 0.0
    best_portfolio_score = 0.0

    #  Big-O =>  O(2^n)  : ((2^n -1) * n +2)
    for shares_amount in range(scan_begin, scan_strength + 1):  # n
        generator = combinations(shares_list, shares_amount)
        for portfolio in generator:  # 2^n -1
            cost = get_portfolio_cost(portfolio)
            if _filter(cost):  # 1
                acceptable_cost = cost
                if not best_portfolio:
                    best_portfolio = portfolio
                    best_portfolio_cost = acceptable_cost
                    best_portfolio_score = get_portfolio_net_roi(portfolio)
                else:
                    best_portfolio_score = score(best_portfolio)
                    portfolio_score = score(portfolio)
                    portfolio_roi = get_portfolio_average_roi(portfolio)
                    if new_high_score(portfolio_score, best_portfolio_score):  #  1
                        best_portfolio = portfolio
                        best_portfolio_cost = acceptable_cost
                        best_portfolio_score = portfolio_score
                        best_portfolio_roi = portfolio_roi
    if best_portfolio:
        print(f'\nHere is the Best Possible Portfolio of all:\n'
              f'- Investment: {best_portfolio_cost} €\n'
              f'- Portfolio Average ROI: {round(best_portfolio_roi, 2)} %\n'
              f'- Net ROI after 2 years: {round(best_portfolio_score, 2)} €\n'
              f'- Portfolio ({len(best_portfolio)} Shares): {serialize(best_portfolio)}\n'
              f'- Details: {best_portfolio}\n')

    else:
        print('No portfolio was found under the investment limit !')
    timer_1 = datetime.now() - timer_0
    print(timer_1)
    return best_portfolio


if __name__ == "__main__":
    main(lambda x: x <= 500, get_portfolio_net_roi, scan_strength=20)
