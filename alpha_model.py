import data_collector as data


# Class to create signals for buying or selling a Currency depending on its trend
class Pair:

    def __init__(self,
                 symbol,
                 buy_signal=False,
                 sell_signal=False):

        self.symbol = symbol
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal

# Method to set a buy or sell signal depending on the kind of trend
    def get_technical_trend(self):
        long_period = data.close_data(self.symbol, data.two_hundred_days)
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

# Calculating the current momentum of a given symbol expressed by the return in the past week
    def calculate_rsi(self, period=14):
        """
        Calculate the Relative Strength Index (RSI) for a given DataFrame of stock prices.

        :param period: the number of periods to use in the RSI calculation (default=14)
        :return: pandas Series with the RSI values
        """
        close_price = data.close_data(self.symbol,
                                      data.five_years_ago)['adjusted_close']
        delta = close_price.diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

