import alpha_model

AAPLE = alpha_model.CheckForOpportunity("AAPL.US", False, False)
AAPLE.get_trend()
print(AAPLE.sell_signal)
