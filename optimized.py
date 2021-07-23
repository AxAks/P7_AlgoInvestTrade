import logging
from datetime import datetime

from commons import csv_filepath_args_parser, serialize, from_csv_to_list_of_dict, \
    get_portfolio_cost, get_portfolio_net_roi, get_portfolio_average_roi


def fill_portfolio(sorted_shares_list: list[dict], cost_limit: float) -> tuple[dict]:
    """
    Fills a portfolio with highest-profit shares according to the space left in the portfolio
    """
    portfolio = []
    portfolio_cost = 0.0
    n = 0
    while n < len(sorted_shares_list):
        next_share = sorted_shares_list[n]
        if portfolio_cost + next_share['cost'] <= cost_limit:
            portfolio.append(next_share)
            portfolio_cost = get_portfolio_cost(portfolio)
        n += 1
    return tuple(portfolio)


def get_sorted_shares_list(shares_list: list[dict]) -> list[dict]:
    """
    returns a list of shares sorted from higher to lower score (ROI)
    """
    return sorted(shares_list, key=lambda share: share['roi'], reverse=True)


def main() -> tuple[dict]:
    """
    Sorts the list of shares from highest ROI to lowest and fills the portfolio
    until the portfolio cost reaches the limit (500€ by default if not set)
    """
    args = csv_filepath_args_parser()
    csv_filepath = args.csv_filepath
    cost_limit = args.cost_limit if args.cost_limit else 500
    shares_list = from_csv_to_list_of_dict(csv_filepath)
    logging.basicConfig(filename="logs/optimized.log", level=logging.INFO, filemode='w')
    timer_0 = datetime.now()
    logging.info(f'Scan Start: {datetime.now()}')
    sorted_shares_list = get_sorted_shares_list(shares_list)
    final_portfolio = fill_portfolio(sorted_shares_list, cost_limit)
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
