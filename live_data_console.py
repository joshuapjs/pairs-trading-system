import asyncio
from ib_insync import IB, Stock, TickByTickAllLast

async def market_data():
    ib = IB()
    await ib.connectAsync("127.0.0.1", 7497, clientId=1)

    contract = Stock(symbol='TSLA', exchange='SMART', currency='USD')
    ib.reqMarketDataType(3)
    await ib.qualifyContractsAsync(contract)

    ticker = ib.reqTickByTickData(contract, 'AllLast')

    # Print the latest tick data immediately
    while True:
        await asyncio.sleep(2)
        print(ticker.time, ticker.last)

def main():
    asyncio.run(market_data())

if __name__ == '__main__':
    main()
