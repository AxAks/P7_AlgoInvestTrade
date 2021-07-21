import logging
from datetime import datetime
from utils import csv_filepath_args_parser
from commons import serialize, from_csv_to_list_of_dict, get_portfolio_cost, get_portfolio_net_roi, \
    get_portfolio_average_roi

#  /n +1
def fill_portfolio(sorted_shares_list: list[dict]) -> tuple[dict]:
    """
    Fills a portfolio with highest-profit shares according to the space left in the portfolio
    """
    portfolio = []
    portfolio_cost = 0.0
    timer_0_fill = datetime.now()
    n = 0
    while n < len(sorted_shares_list):  #  n : worse cas il parcourt toute la liste et ajoute tout
        next_share = sorted_shares_list[n]
        if portfolio_cost + next_share['cost'] <= 500.0:  #  worse case => toujours vrai !: 1
            portfolio.append(next_share)
            portfolio_cost = get_portfolio_cost(portfolio)
        n += 1
    timer_1_fill = datetime.now() - timer_0_fill
    print(timer_1_fill)
    return tuple(portfolio)


def get_sorted_shares_list(shares_list: list[dict]) -> list[dict]:
    """
    returns a list of shares sorted from higher to lower score (ROI)
    """
    timer_0_sort = datetime.now()
    sorted_list = sorted(shares_list, key=lambda share: share['roi'], reverse=True)
    timer_1_sort = datetime.now() - timer_0_sort
    print(timer_1_sort)
    return sorted_list

# Big-O : O((n * log n) + n)
def main() -> tuple[dict]:
    """
    Sorts the list of shares from highest ROI to lowest and fills the portfolio
    until the portfolio cost reaches the limit of 500€
    """
    csv_filepath = csv_filepath_args_parser()
    shares_list = from_csv_to_list_of_dict(csv_filepath)
    logging.basicConfig(filename="logs/optimized.log", level=logging.INFO, filemode='w')
    timer_0 = datetime.now()
    logging.info(f'Scan Start: {datetime.now()}')
    sorted_shares_list = get_sorted_shares_list(shares_list)  # n log n  ,à revérifier !
    final_portfolio = fill_portfolio(sorted_shares_list)  #  n
    logging.info(f'Scan End: {datetime.now()}')
    final_portfolio_net_roi = get_portfolio_net_roi(final_portfolio)
    final_portfolio_average_roi = get_portfolio_average_roi(final_portfolio)
    print(f'Scan Result : Final Portfolio (Net ROI: {round(final_portfolio_net_roi, 2)} €, '
          f'{round(final_portfolio_average_roi, 2)} %):\n'
          f'-> {serialize(final_portfolio)}\n'
          f'for a investment of {round(get_portfolio_cost(final_portfolio), 2)} € '
          f'in {len(final_portfolio)} shares')
    logging.info(f'Scan Result : Final Portfolio (Net ROI: {round(final_portfolio_net_roi, 2)} €, '
                 f'{round(final_portfolio_average_roi, 2)} %):\n'
                 f'-> {serialize(final_portfolio)}\n'
                 f'for a investment of {round(get_portfolio_cost(final_portfolio), 2)} € '
                 f'in {len(final_portfolio)} shares')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    return final_portfolio


if __name__ == "__main__":
    main()
