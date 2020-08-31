import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from config import *
from enum import Enum, unique

import csv
import time
import os.path
from os import path

import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objs as go
import numpy as np
from sklearn import linear_model as lm
from datetime import datetime

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

class CSV_Handler:
    def __init__(self):
        pass

    # Pulls the current S&P 500 companies
    def update_sp500(self, update_all_files: bool = False):
        table=pd.read_html(io='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        df = table[0]
        df.to_csv("./db/S&P500-Info.csv")
        df.to_csv("./db/S&P500-Symbols.csv", columns=['Symbol'])

        if update_all_files:
            test_stocks = pd.read_csv("./db/S&P500-Symbols.csv", squeeze=True)
            test_stocks_list = test_stocks.Symbol.to_list()

            self.create_csvs(test_stocks_list, start="2020-1-1", end="2020-8-21")

    # Generate CSVs containing all stock data or a portion of the stock data 
    def create_csvs(self, stocks, start=None, end=None):
        if type(stocks) is not list: 
            stocks = [ stocks ]

        for stock in stocks:
            data = yf.download(stock, start, end)
            data.to_csv('./db/'+stock+'.csv')

    # Grab all relevant data from a specified csv file
    # Review: http://beancoder.com/linear-regression-stock-prediction/
    def get_data(self, filename: str, show_plot: bool = False):
        dates = []
        open_prices = []
        close_prices = []
        high_prices = []
        low_prices = []
        volume = []

        with open(filename, 'r') as csvfile:
            csvFileReader = csv.reader(csvfile)
            next(csvFileReader)     # skip first row
            for row in csvFileReader:
                date_time_obj = datetime.strptime(row[0], '%Y-%m-%d')
                dates.append((int)(date_time_obj.strftime("%Y%m%d")))
                open_prices.append(float(row[1]))
                close_prices.append(float(row[4]))
                high_prices.append(float(row[2]))
                low_prices.append(float(row[3]))
                volume.append(int(row[6]))

        if show_plot:
            self.show_LR_plot(dates,open_prices)

        return dates,open_prices,close_prices,high_prices,low_prices,volume

    def show_LR_plot(self, dates, prices):
        # Do for roughly the following date ranges (3 month, 6 month, 1 year, 3 year, 5 year)
        # roughly because we'll use 20 trading days to signify a month
        # converting to matrix of n X 1
        dates = np.reshape(dates,(len(dates),1))
        prices = np.reshape(prices,(len(prices),1))

        #set up the lm models we'll use (for each time horizon)
        linear_mod_1m = lm.LinearRegression()
        linear_mod_3m = lm.LinearRegression()
        linear_mod_6m = lm.LinearRegression()
        linear_mod_1y = lm.LinearRegression()
        linear_mod_3y = lm.LinearRegression()
        linear_mod_5y = lm.LinearRegression()

        #Fitting the data points in the model (for each time horizon)
        linear_mod_1m.fit(dates[-20:],prices[-20:]) 
        linear_mod_3m.fit(dates[-60:],prices[-60:])
        linear_mod_6m.fit(dates[-120:],prices[-120:])
        linear_mod_1y.fit(dates[-252:],prices[-252:])
        linear_mod_3y.fit(dates[-756:],prices[-756:])
        linear_mod_5y.fit(dates[-1260:],prices[-1260:])

        #All data is plotted on a scatter
        plt.scatter(dates,prices,color='red') 

        #Plot each of the linear regressions
        plt.plot(dates[-20:], linear_mod_1m.predict(dates[-20:]), label="1 month")
        plt.plot(dates[-60:], linear_mod_3m.predict(dates[-60:]), label="3 month")
        plt.plot(dates[-120:], linear_mod_6m.predict(dates[-120:]), color='green', linewidth=3, label="6 month")
        plt.plot(dates[-252:], linear_mod_1y.predict(dates[-252:]), color='blue', linewidth=3, label="1 year")
        plt.plot(dates[-756:], linear_mod_3y.predict(dates[-756:]), color='indigo', linewidth=3, label="3 year")
        plt.plot(dates[-1260:], linear_mod_5y.predict(dates[-1260:]), color='violet', linewidth=3, label="5 year")

        plt.legend(loc="upper left")
        plt.show()
        return

    # WIP
    # def predict_price(self, dates: list, prices: list):
    #     linear_mod = LinearRegression() #defining the linear regression model
    #     dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    #     prices = np.reshape(prices,(len(prices),1))
    #     linear_mod.fit(dates,prices) #fitting the data points in the model
    #     predicted_price = linear_mod.predict(x)
        
    #     return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]

    # View the candle charts of the given stock(s)
    def see_candle(self, stocks):
        if type(stocks) is not list: 
            stocks = [ stocks ]

        for stock in stocks:
            if path.exists('./db/'+stock+'.csv'):
                candle_csv = pd.read_csv('./db/'+stock+'.csv')
                candle_data = [go.Candlestick(x=candle_csv['Date'],
                    open=candle_csv['Open'],
                    high=candle_csv['High'],
                    low=candle_csv['Low'],
                    close=candle_csv['Close'])]
            
                figSignal = go.Figure(data=candle_data)
                figSignal.show()

class AutoInvestBot:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, API_SECRET_KEY, ALPACA_BASE_ENDPOINT)
        self.csv = CSV_Handler()

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

    # Holds the information for the given stocks
    # - stocks arg is a string of stocks separated with spaces
    def tickers(self, stocks: str):
        return yf.Tickers(stocks)

if __name__ == "__main__":
    bot = AutoInvestBot()

    # bot.update_sp500()

    # bot.csv.see_candle(['TSLA','AAPL'])

    ZTS_data = bot.csv.get_data('./db/ZTS.csv', False)
    
    bot.csv.show_LR_plot(ZTS_data[0], ZTS_data[1])
    
    bot.account_info()

    # bot.worker_thread()

    