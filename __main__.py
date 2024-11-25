from data_connector import Pair
from tws_connection import ib, build_connection
import execution_model
import alpha_model
import logger as log
from constants import PAIRS_TRADED, BUDGET, CURRENCY, THRESHOLD
from personal_constants import ACCOUNT_NUMBER
from portfolio_model import Portfolio

if not ib.isConnected():
    build_connection()

# For all Pairs a subscription to the data from TWS has to be made when the program start.
def connect_pairs(pairs):
    for pair in pairs:
        pair.connect_data()

if __name__ == "__main__":
    # The log will not be pushed to the repo so it must be ensured that it exists, before the program can start.
    log.initialize_logger()
    ib.sleep(5)

    portfolio = Portfolio(account_number=ACCOUNT_NUMBER, slots=PAIRS_TRADED, budget=BUDGET)

    # TODO: The test data obviously has to be replaced by real data.
    # For further explaination about the Pairs class, please refer to the data_connector module.
    test_pairs = [Pair(("AAPL", "MSFT"), CURRENCY, (1,1)),
                  Pair(("GM", "TSLA"), CURRENCY, (1,1)),
                  Pair(("AMZN", "CPNG"), CURRENCY, (1,1))]

    connect_pairs(test_pairs)
    ib.sleep(3)

    while True:
        """
        The logic follows iteratively that same pattern.

        1. Generate new Signals for each of the Pairs that are currently traded.
        2. The Signals generated in 1. have to be evaulated by the portfolio.analyze_signals method.
        3. During the analysis, instructions about what the new positions should look like, were created.
           Those will be directed to the Execution Model in the next step.
        4. In the last step, current positions and Signals that could not be followed, because the maximum amount of trades 
           we want to be in at the same time was reached, will be analyzed and the portfolio adjusted if a position fullfilled its
           predicted potential or if the position is blocking a better opportunity.

        """
        ib.sleep(10)
        signals = alpha_model.generate_signals(test_pairs, threshold=THRESHOLD)
        portfolio_changes = portfolio.analyze_signals(signals) 
        execution_model.execute_portfolio_adjustments(portfolio, portfolio_changes)
        new_adjustments = portfolio.optimize()
        execution_model.execute_portfolio_adjustments(portfolio, new_adjustments)

else:
    raise ImportError("THE MODULE __main__.py IS NOT INTENDED TO BE IMPORTED")

