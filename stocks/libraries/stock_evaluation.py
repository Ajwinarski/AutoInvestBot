# Common Imports

class StockEvaluation:
    def __init__(self, ticker: str, action: Action, amount: int):
        self.ticker = ticker
        self.action = action
        self.amount = amount