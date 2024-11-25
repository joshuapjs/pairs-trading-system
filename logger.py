"""
This Module contains the Logger class, a integral for all logging operations in this project.
"""
import sqlite3
import os
import time
from constants import PATH
from constants import DATABASE_NAME

current_time = time.strftime('%Y-%m-%d %H:%M:%S')

def initialize_logger():
    if not os.path.exists(PATH + DATABASE_NAME):
        with sqlite3.connect(PATH + DATABASE_NAME) as log:
            try:
                cur = log.cursor()
                create_table1 = f"""CREATE TABLE Signals(Time SmallDateTime, Deviation double, Sign int, Ticker_a char(15), 
                                    Ticker_b Char(15), Const double, Slope double, Threshold double);"""
                cur.execute(create_table1)
                create_table2 = f"CREATE TABLE Trades(Time SmallDateTime, Type char(15), Action char(5), Quantity int, Stock char(15), Price double);"
                cur.execute(create_table2)
                log.commit()
                print("\033[32mLOGGER\033[0m: Database was created with tables 'Trades' and 'Signals'")
            except sqlite3.OperationalError as e:
                print("\033[32mLOGGER\033[0m: Something went wrong with the creation of tables or database itself.")
                print(e)
    else:
        print("\033[32mLOGGER\033[0m : Database ready;")


def log_trade(trade_type: str, action: str, quantity: int, stock_ticker: str, price: int):
    """
    This function used by the execution model logs all trades that were sent to IBKR.
    :param trade_type: The type of the Trade so usually MARKET (Market Order) or LIMIT (Limit Order).
    :param action : BUY or SELL
    :param quantity: The amount of shares traded.
    :param stock_ticker: The ticker of the stock traded.
    :param price: The Price of the asset executed.
    """

    try:
        with sqlite3.connect(PATH + DATABASE_NAME) as log:
            cur = log.cursor()
            execution_command = f"INSERT INTO Trades (Time, Type, Action, Quantity, Stock, Price)"  \
                                f"VALUES (?, ?, ?, ?, ?, ?)"""
            values = (current_time, trade_type, action, quantity, stock_ticker, price)
            cur.execute(execution_command, values)
            log.commit()
            print(f"LOG : New Trade of {stock_ticker} written in Table Trades;")
    except sqlite3.OperationalError as e:
        print("\033[32mLOGGER\033[0m : Writing trade data to database not successful;", e)


def log_signal(deviation: float, sign: int, ticker_a: str, ticker_b: str, const: float, slope: float, threshold: float):
    """
    This function used by the alpha model logs all signals generated.
    :param deviation: The Deviation of the two stock prices from their equilibrium.
    :param sign: The sign of the deviation. This is separated to indicate the direction of the deviation.
    :param ticker_a: Ticker of the first Stock.
    :param ticker_b: Ticker of the second Stock.
    """

    try:
        with sqlite3.connect(PATH + DATABASE_NAME) as log:
            cur = log.cursor()
            execution_command = f"INSERT INTO Signals (Time, Deviation, Sign, Ticker_a, Ticker_b, Const, Slope, Threshold)"  \
                                    f"VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            cur.execute(execution_command, (current_time, deviation, sign, ticker_a, ticker_b, const, slope, threshold))
            log.commit()
            print(f"\033[32mLOGGER\033[0m : New Signal of {ticker_a}/{ticker_b} written in Table Signals;")
    except sqlite3.OperationalError as e:
        print("\033[32mLOGGER\033[0m : Writing signal data to database not successful;", e)
