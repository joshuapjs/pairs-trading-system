import alpha_model
import data_grabber
import time

AAPLE = alpha_model.CheckForOpportunity("AAPL.US", False, False)
#print(AAPLE.short_term_trend())
data_grabber.real_time_data()
