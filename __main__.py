from data_connector import Pair
from tws_connection import ib, build_connection
import execution_model
import alpha_model
from constants import ACCOUNT_NUMBER, PAIRS_TRADED, BUDGET
from portfolio_model import Portfolio

# TODO The Executionfunction should try to minimize trading cost. This Calculation should run during the initialization there must be an initialize function, that calculates current relevant measures for the execution model and possibly the Regression.
# A data base is needed that stores the current Volume weighted cost for each asset. 
# This is the moment where the initializer function has to be declared as such a calculation should be made
# prior to trading. 
# A simple CSV is enough - it should be loaded into memory - Redis ?
# We can use the distirbution of minute to minute price differences to estimate the slippage for each trade.
# We can assign a probability to each of the possible price jumps and calculate an expected price jump that should be compensated
# by the expected return.

# TODO implement controls through terminal
# TODO Ask or Bid should be used correctly when determining if an adjustment would make sense - not all positions are positive. NOTE: ib_insync could provide a solution for that.

# Check if a connection exists already
if not ib.isConnected():
    build_connection()

def connect_pairs(pairs):
    for pair in pairs:
        pair.connect_data()

if __name__ == "__main__":
    portfolio = Portfolio(account_number=ACCOUNT_NUMBER, slots=PAIRS_TRADED, budget=BUDGET)
    # TODO Replace test data with real data.
    test_pairs = [Pair(("AAPL", "MSFT"), "USD", (1,1,1)),
                  Pair(("GM", "TSLA"), "USD", (1,1,1)),
                  Pair(("AMZN", "CPNG"), "USD", (1,1,1))]

    connect_pairs(test_pairs)
    ib.sleep(3)
    
    signals = alpha_model.generate_signals(test_pairs)

    # Erstelle das Initale Portfolio
    initial_execution = portfolio.analyze_signals(signals)
    execution_model.execute_portfolio_adjustments(portfolio, initial_execution)

    while True:
        ib.sleep(10)
        new_adjustments = portfolio.optimize()
        execution_model.execute_portfolio_adjustments(portfolio, new_adjustments)

else:
    raise ImportError("This module is not for external use")

