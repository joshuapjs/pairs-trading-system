from scipy import stats
import data_collector


# Class to create signals for buying or selling a stock according to the trend
class Asset:

    def __init__(self,
                 symbol,
                 buy_signal=False,
                 sell_signal=False):

        self.symbol = symbol
        self.buy_signal = buy_signal
        self.sell_signal = sell_signal

# Method to set a buy or sell signal depending on the kind of trend
    def get_technical_trend(self):
        long_period = data_collector.close_data(self.symbol, data_collector.start_long_period)
        short_period = long_period[str(data_collector.start_short_period):]
        long_average = long_period["adjusted_close"].mean()
        short_average = short_period["adjusted_close"].mean()

        if long_average < short_average:
            self.buy_signal = True
        else:
            self.sell_signal = True

        output = {"buy_signal": self.buy_signal,
                  "sell_signal": self.sell_signal}

        return output


