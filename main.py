import alpha_model

AAPLE = alpha_model.CheckForOpportunity("AAPL.US", False, False)
print(AAPLE.get_technical_trend())
