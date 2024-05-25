
class Pair:
    """
    This class should store the data of each stock that is currently traded.
    To reduce overhead, no getter and setter methods were used.
    """

    def __init__(self,
                 tickers: tuple,
                 currency: str):

        # TODO Prüfen ob es sich lohnen würde zwei unterschiedliche currencies zulassen.

        a,b = tickers

        self.tickers: tuple = tickers
        self.ticker_a: str = a
        self.ticker_b: str = b
        self.contract_a: ib_insync.contract.Stock = None
        self.contract_b: ib_insync.contract.Stock = None
        self.quotes_a = None 
        self.quotes_b = None
        self.equation: tuple = None  # (const, slope, threshold)
        self.currency: str = currency
    
