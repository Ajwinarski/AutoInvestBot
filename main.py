import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from config import *

class AutoInvestBot:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET_KEY, ALPACA_BASE_ENDPOINT)

    # Obtain and print account information
    def account_info(self):
        account = self.api.get_account()
        print(account)

if __name__ == "__main__":
    bot = AutoInvestBot()
    
    bot.account_info()