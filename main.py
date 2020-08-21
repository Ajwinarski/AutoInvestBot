import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import threading
import time
import datetime

from config import *


class AutoInvestBot:
    def __init__(self):
        self.alpaca = tradeapi.REST(
            API_KEY, API_SECRET_KEY, ALPACA_BASE_ENDPOINT)

    # Obtain and print account information
    def account_info(self):
        account = self.alpaca.get_account()
        print(account)

    # Used to submit buy or sell orders
    def order(self, side, stock, qty):
        # Check that qty is greater than 0
        if(qty > 0):
            try:
                self.alpaca.submit_order(stock, qty, side, "market", "day")
                print("Purchased " + str(qty) + " shares of " + stock + ".")
            except:
                print("ERROR: Purchase order for " + str(qty) +
                      " shares of " + stock + " did not go through.")


if __name__ == "__main__":
    bot = AutoInvestBot()

    bot.account_info()
