import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from config import *
from enum import Enum, unique
import time

@unique
class Action(Enum):
    Buy = 1
    Self = 2

class AnalysisResult:
    def __init__(self, ticker: str, action: Action, amount: int):
        self.ticker = ticker
        self.action = action
        self.amount = amount

class Analyzer: 
    # Hard coding for now, but look through current holdlings to determine if should sell.
    # If balance available (within some threshold of account value) look for additional stocks to purchase
    def analyze_result(self) -> AnalysisResult:
        return AnalysisResult("SPY", Action.Buy, 100)

class Trader:
    def trade_result(self, AnalysisResult) -> str:
        return "hi"

class AutoInvestBot:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET_KEY, ALPACA_BASE_ENDPOINT)

    # Obtain and print account information
    def account_info(self):
        account = self.api.get_account()
        print(account)

    def worker_thread(self):
        analyzer = Analyzer()
        trader = Trader()
        while True:
            analysis_result = analyzer.analyze_result()
            trade_result = trader.trade_result(analysis_result)
            print(trade_result)
            time.sleep(10)

if __name__ == "__main__":
    bot = AutoInvestBot()
    
    bot.account_info()

    bot.worker_thread()
    