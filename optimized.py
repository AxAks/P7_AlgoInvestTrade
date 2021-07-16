import logging
from datetime import datetime
from commons import serialize, from_csv_to_list_of_dict, get_portfolio_cost, get_portfolio_net_roi


def fill_portfolio(sorted_shares_list: list) -> tuple:
    """
    Fills a portfolio with highest-profit shares according to the space left in the portfolio
    """
    portfolio = []
    portfolio_cost = 0.0
    n = 0
    while portfolio_cost <= 500.0 and n < len(sorted_shares_list):
        next_share = sorted_shares_list[n]
        if portfolio_cost + get_share_cost(next_share) <= 500.0:
            portfolio.append(next_share)
            portfolio_cost = get_portfolio_cost(portfolio)
        n += 1
    return tuple(portfolio)


def get_share_cost(share: dict) -> float:
    """
    Give the cost of a specific share
    """
    return share['cost']


def get_share_score(share: dict) -> float:
    """
    Extracts the return on investment in % for a specific share
    """
    return share['roi']


def get_sorted_shares_list(shares_list: list) -> list:
    """
    returns a list of shares sorted from higher to lower score (ROI)
    """
    return sorted(shares_list, key=lambda share: get_share_score(share), reverse=True)


def main(shares_list):
    logging.basicConfig(filename="logs/optimized.log", level=logging.INFO, filemode='w')
    timer_0 = datetime.now()
    logging.info(f'Scan Start: {datetime.now()}')
    sorted_shares_list = get_sorted_shares_list(shares_list)
    final_portfolio = fill_portfolio(sorted_shares_list)
    logging.info(f'Scan End: {datetime.now()}')
    final_portfolio_net_roi = get_portfolio_net_roi(final_portfolio)
    print(f'Scan Result : Best Portfolio (Net ROI: {round(final_portfolio_net_roi, 2)} €):\n'
          f'-> {serialize(final_portfolio)}\n'
          f'for a investment of {round(get_portfolio_cost(final_portfolio), 2)} € '
          f'in {len(final_portfolio)} shares')
    logging.info(f'Scan Result : Best Portfolio (Net ROI: {round(final_portfolio_net_roi, 2)} €):\n'
                 f'-> {serialize(final_portfolio)}\n'
                 f'for a investment of {round(get_portfolio_cost(final_portfolio), 2)} € '
                 f'in {len(final_portfolio)} shares')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    return final_portfolio


"""
il faudrait pouvoir choisir le fichier (le passer en arg dans le terminal)...
"""

# shares_list = from_csv_to_list_of_dict('data/initial_values.csv')
# shares_list = from_csv_to_list_of_dict('data/dataset1_Python+P7.csv')
shares_list = from_csv_to_list_of_dict('data/dataset2_Python+P7.csv')

if __name__ == "__main__":
    main(shares_list)
