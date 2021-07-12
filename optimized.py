import logging
from datetime import datetime
from commons import serialize, from_csv_to_list_of_dict, get_portfolio_cost, get_portfolio_net_roi, \
    get_portfolio_average_roi


def fill_portfolio(sorted_shares_list: list) -> tuple:
    """
    Fill a portfolio with shares according to the space left in the portfolio
     .... (to be detailed !)
    """
    portfolio = []
    portfolio_cost = 0.0
    portfolio_average_roi = 0.0
    portfolio_net_roi = 0.0
    n = 0
    while portfolio_cost <= 500.0 and n < len(sorted_shares_list):
        next_share = sorted_shares_list[n]
        next_share_name = next_share['name']
        portfolio_net_roi = get_portfolio_net_roi(portfolio) if portfolio else 0.0
        if portfolio_cost + get_share_cost(next_share) <= 500.0\
                and get_share_net_roi(next_share) != 0.0\
                and portfolio_net_roi + get_share_net_roi(next_share) > portfolio_net_roi:
            print(f'\nPortfolio cost limit not reached, new share added: {next_share_name}:')
            portfolio.append(next_share)
            portfolio_cost = get_portfolio_cost(portfolio)
            portfolio_net_roi = get_portfolio_net_roi(portfolio)
            portfolio_average_roi = get_portfolio_average_roi(portfolio)
            print(f'Portfolio: {serialize(portfolio)}')
            print(f'Cost: {round(portfolio_cost, 2)} €')
            print(f'Relative ROI: {round(portfolio_average_roi, 2)} %')
            print(f'Net ROI after two years: {round(portfolio_net_roi, 2)} €')
        n += 1
    print(f'\nOptimized portfolio found ({len(portfolio)} shares): {serialize(portfolio)} '
          f'for a cost of: {round(portfolio_cost, 2)} € investment\n'
          f'-> Relative ROI: {round(portfolio_average_roi, 2)} %\n'
          f'-> Net ROI after two years: {round(portfolio_net_roi, 2)} €')
    return tuple(portfolio)


def get_share_net_roi(share: dict) -> float:
    """
    Calculate the net return on investment for a specific share
    """
    if not share:
        return 0.0
    else:
        return round(get_share_cost(share) * share['roi'], 5)


def get_share_cost(share: dict) -> float:
    """
    Give the cost of a specific share
    """
    if share:
        return share['cost']


def get_share_score(share: dict) -> float:
    """
    Extracts the return on investment in % for a specific share
    """
    if not share:
        return 0.0
    else:
        return share['roi']


def get_sorted_shares_list(shares_list: list) -> list:
    """
    returns a list of shares sorted from higher to lower score (net ROI)
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
    logging.info(f'Scan Result : Best Portfolio (Net ROI: {round(final_portfolio_net_roi, 2)} €):\n'
                 f'-> {serialize(final_portfolio)}\n'
                 f'for a investment of {get_portfolio_cost(final_portfolio)} € in {len(final_portfolio)} shares')
    execution_time = datetime.now() - timer_0
    logging.info(f'Execution Time = {execution_time}')
    print(f'\nExecution Time = {execution_time}')
    return final_portfolio


"""
il faudrait pouvoir choisir le fichier (le passer en arg dans le terminal)...
"""
# shares_list = from_csv_to_list_of_dict('data/initial_values.csv')
shares_list = from_csv_to_list_of_dict('data/dataset1_Python+P7.csv')
# shares_list = from_csv_to_list_of_dict('data/dataset2_Python+P7.csv')

if __name__ == "__main__":
    main(shares_list)
