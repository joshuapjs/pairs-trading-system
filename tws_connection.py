"""
This module enables the program to share the connection to tws.
"""

from ib_insync import IB

ib = IB()

def build_connection():
    # Connect to TWS through ib_insync.
    connection = ib.connect("127.0.0.1", 7497, clientId=15)

