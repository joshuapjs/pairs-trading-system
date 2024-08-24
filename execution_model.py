"""
This Module contains the functions necessary to size and place orders on behalf of the Alpha Model. 
"""
import ib_insync
import asyncio as aio
import portfolio_model
from tws_connection import ib, build_connection


# Check if a connection exists already
if not ib.isConnected():
    build_connection()


def stock_limit_order(contract: ib_insync.contract.Stock, limit_price: int, action: str, quantity: int):
    """
    Wrapper for an ib_insync Limit-Order to increase readability.
    :param contract: The ib_insync.contract.Stock Object, necessary for the exection of the order.
    :param limit_price: The desired price.
    :param action: Intention to "BUY" or "SELL".
    :param quantity: The quantity of shares to be bought or sold.
    :return:
    """
    order = ib_insync.LimitOrder(action, quantity, limit_price)
    ib.placeOrder(contract, order)
    ib.sleep(1)


def stock_market_order(contract: ib_insync.contract.Stock, action: str, quantity: int) :
    """
    Wrapper for an ib_insync Market-Order to increase readability.
    :param contract: The ib_insync.contract.Stock Object, necessary for the exection of the order.
    :param action: Intention to "BUY" or "SELL".
    :param quantity: The quantity of shares to be bought or sold.
    :return:
    """
    order = ib_insync.MarketOrder(action, quantity)
    ib.placeOrder(contract, order)
    ib.sleep(1)


def execute_portfolio_adjustments(portfolio_class: portfolio_model.Portfolio, portfolio_adjustments: dict):
    """
    Execution of the portfolio_adjustments, give as preferred new position sizes.
    :param portfolio_class: The class of the current Portfolio from the Module portfolio_model.py.
    :param portfolio_adjustments: Dictionary with ticker strings as Keys and Position Size as values.
    :return: 
    """
    if portfolio_adjustments == {}:
        print("EXECUTION MODEL : No portfolio adjustments received.")
        return 
    for ticker, ideal_positions_size in portfolio_adjustments.items():
        # Check if a position that should be adjusted even exists, if not the old position size is zero.
        try: old_position_size = portfolio_class[ticker]
        except KeyError:
            old_position_size = 0
        # Determinte the delta and the action of the execution.
        position_size = ideal_position_size - old_position_size  
        pair = portfolio_class.pairs_traded[ticker]
        if pair.ticker_a == ticker:
            contract = pair.contract_a
        else:
            contract = pair.contract_b
        if positions_size < 0:
            stock_market_order(contract, "SELL", quantity=position_size)
            # Caution: If the Model should work with a more complex execution Algorithm like Limit-Orders
            # that might need to be canceled, it CAN'T  be assumed that the positions size is always completely executed.
            # NOTE: There is an cancelOrder Method for IB.
            portfolio_class.portfolio[ticker] = positions_size  # Record what the current portfolio looks like.
            continue
        elif position_size > 0:
            stock_market_order(contract, "BUY", quantity=position_size)
            portfolio_class.portfolio[ticker] = positions_size
            continue
        else:
            print(f"EXECUTION MODEL : Zero positional change - no execution necessary for {ticker}.")
            continue

