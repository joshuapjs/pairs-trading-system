import pandas as pd
import eod_data_collector as data


# Class to create signals for buying or selling a Currency depending on its trend
class Pair:

    def __init__(self,
                 symbol,
                 buy_signal=False,
                 sell_signal=False):

        self.symbol = symbol
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal

    def get_technical_trend(self, currency):
        """
        identifying the current technical trend and creating a buy or sell signal
        :param currency: symbol of the foreign currency
        :return: Dictionary including the signals for display
        """
        long_period = data.close_data(self.symbol + currency, data.two_hundred_days)
        short_period = long_period[str(data.seven_days):]
        long_average = long_period["adjusted_close"].mean()
        short_average = short_period["adjusted_close"].mean()

        if long_average < short_average:
            self.buy_signal = True
        else:
            self.sell_signal = True

        output = {"buy_signal": self.buy_signal,
                  "sell_signal": self.sell_signal}

        return output

    def calculate_rsi(self, currency, period=14):
        """
        Calculate the Relative Strength Index (RSI) for a given DataFrame of stock prices.
        :param currency: symbol of the foreign currency
        :param period: the number of periods to use in the RSI calculation (default=14)
        :return: pandas Series with the RSI values
        """
        close_price = data.close_data(self.symbol + currency,
                                      data.five_years_ago)['adjusted_close']
        delta = close_price.diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_spread(self):
        """
        Calculating the rate spreads between the central bank rates of the most liquid currencies
        :return: DataFrame containing the spreads depending on the currency of choice
        """
        rates = data.current_cb_rates()
        spreads = {}

        for currency in rates.index:
            spreads[self.symbol + currency] = rates['Central bank interest rate (%)'].loc[self.symbol]\
                                              - rates['Central bank interest rate (%)'].loc[currency]

        spreads_df = pd.DataFrame(data={'Spreads': spreads.values()}, index=spreads.keys())\
            .drop(self.symbol * 2, axis=0)

        return spreads_df


# def model(currency_pair, param1, param2, param3):
# If rsi is >30 and <70 no signal - otherwise, bet on trend reversal - news check??
# If technical trend positive but rsi negative bet on reversal and vice versa
# big positive spread --> forex rate might rise
