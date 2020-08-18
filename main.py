import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from config import *

class AutoInvestBot:

    def __init__(self):
        self.api = tradeapi.REST(api_key, api_secret_key, ALPACA_BASE_ENDPOINT, api_version='v2')

    # Obtain and print account information
    def account_info(self):
        account = self.api.get_account()
        print(account)

if __name__ == "__main__":
    AutoInvestBot().account_info()