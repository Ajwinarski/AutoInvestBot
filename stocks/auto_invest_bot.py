# Common Imports
import time

# Absolute Imports
from modules.csv_handler import CSV_Handler
from modules.trader import Trader

# API imports
from config import *

# Libraries
import yfinance as yf


class AutoInvestBot:
    def __init__(self):
        # self.api = api_info
        self.csv = CSV_Handler()

    # Obtain and print account information
    def account_info(self):
        pass
        # account = self.api.get_account()
        # print(account)

    # def worker_thread(self):
    #     analyzer = Analyzer()
    #     trader = Trader()
    #     while True:
    #         analysis_result = analyzer.analyze_result()
    #         trade_result = trader.trade_result(analysis_result)
    #         print(trade_result)
    #         time.sleep(10)

    # Used to submit buy or sell orders
    def order(self, side, stock, qty):
        # Check that qty is greater than 0
        if (qty > 0):
            try:
                # self.api.submit_order(stock, qty, side, "market", "day")
                print("Purchased " + str(qty) + " shares of " + stock + ".")
            except:
                print("ERROR: Purchase order for " + str(qty) +
                      " shares of " + stock + " did not go through.")

    # Holds the information for the given stocks
    # - stocks arg is a string of stocks separated with spaces
    def tickers(self, stocks: str):
        return yf.Tickers(stocks)

# TODO: Remove this and add functionality to Stock_Evaluation class


# class Analyzer:
#     # Hard coding for now, but look through current holdlings to determine if should sell.
#     # If balance available (within some threshold of account value) look for additional stocks to purchase
#     def analyze_result(self) -> AnalysisResult:
#         return AnalysisResult("SPY", Action.Buy, 100)
