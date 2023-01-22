import alpha_model

AAPL = alpha_model.CheckForOpportunity("AAPL")
print(AAPL.get_technical_trend())
AAPL.get_current_trend()
print("Sell Signal:", AAPL.sell_signal, "Buy Signal:", AAPL.buy_signal)
