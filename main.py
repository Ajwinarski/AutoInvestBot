import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from config import *

class AutoInvestBot:

    def __init__(self):
        self.api = tradeapi.REST(api_key, api_secret_key, ALPACA_BASE_ENDPOINT, api_version='v2')

    def run(self):
        #obtain and print account information
        account = self.api.get_account()
        print(account)

        # Async example
        # async def on_minute(conn, channel, bar):
            # Entry for purchase
            # if bar.close >= bar.open and (bar.open - bar.low) > 0.1:
            #     print("Buying on Doji Candle")
            #     self.alpaca.submit_order("MSFT", 1, 'buy', 'market', 'day')

if __name__ == "__main__":
    AutoInvestBot().run()