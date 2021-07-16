import logging

from datetime import datetime
from itertools import combinations, combinations_with_replacement
from typing import Callable, Any

from utils import read_file, write_file, csv_filepath_args_parser
from commons import serialize, deserialize, from_csv_to_list_of_dict, get_portfolio_cost, get_portfolio_average_roi, \
    get_portfolio_net_roi


def new_high_score(new_score: float, previous_score: float) -> bool:
    """
    checks whether the new portfolio score is higher
    than the previously registered portfolio score
    """
    return new_score > previous_score


def main(scan_strength: int, _filter: Callable[[Any], bool], score: Callable[[Any], float],
         replacement: bool = False, secure: bool = False, scan_begin: int = 1) -> list[tuple]:
    """
    Returns all possible combinations of shares under the given criteria:
    - Cost of portfolio under 500€
    - Share only to be bought once
    - Share cannot be sold partially
    Give the possibility to choose whether an share can be
    bought several times (if needed later for evolution)
    By default, the best result is saved in a variable,
    the Option Secure enables to save the result in a .txt file
    """
    args = csv_filepath_args_parser()
    shares_list = from_csv_to_list_of_dict(args.csv_filepath)
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
        file = 'results_backups/bruteforce_buffer_result.txt'
        best_portfolio = deserialize(read_file(file), shares_list)
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
                        file = f'results_backups/bruteforce_buffer_result.txt'
                        write_file(file, serialize(best_portfolio))

                else:
                    best_portfolio_score = round(score(best_portfolio), 2)
                    portfolio_score = round(score(portfolio), 2)
                    portfolio_roi = get_portfolio_average_roi(portfolio)
                    if new_high_score(portfolio_score, best_portfolio_score):
                        best_portfolio = portfolio
                        best_portfolio_cost = acceptable_cost
                        best_portfolio_score = portfolio_score
                        best_portfolio_roi = portfolio_roi
                        print(f'-> New High: {best_portfolio_score} €')
                        logging.info(f'-> New High: {best_portfolio_score} €')
                        if secure:
                            file = f'results_backups/bruteforce_buffer_result.txt'
                            write_file(file, serialize(best_portfolio))

    if best_portfolio:
        print(f'\nHere is the Best Possible Portfolio of all:\n'
              f'- Investment: {best_portfolio_cost} €\n'
              f'- Portfolio Average ROI: {round(best_portfolio_roi, 2)} %\n'
              f'- Net ROI after 2 years: {round(best_portfolio_score, 2)} €\n'
              f'- Portfolio ({len(best_portfolio)} Shares): {serialize(best_portfolio)}\n'
              f'- Details: {best_portfolio}\n')

    else:
        print('No portfolio was found under the investment limit !')

    logging.info(f'Latest scan step proceeded: {shares_amount}')
    logging.info(f'Scan End: {datetime.now()}')
    logging.info(f'Scan Result : Best Portfolio (Net ROI: {round(get_portfolio_net_roi(best_portfolio), 2)} €):\n'
                 f'-> {serialize(best_portfolio)}\n'
                 f'for a investment of {get_portfolio_cost(best_portfolio)} € in {len(best_portfolio)} shares')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    print(f'Execution Time = {execution_time}')
    return best_portfolio


if __name__ == "__main__":
    main(20, lambda x: x <= 500, get_portfolio_net_roi, secure=False)
