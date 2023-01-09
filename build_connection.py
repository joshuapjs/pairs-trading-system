from eod import EodHistoricalData
import os


def build_connection():
    key = os.environ["API_EOD"]
    client = EodHistoricalData(key)
    return client
