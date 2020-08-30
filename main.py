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
    def get_data(self, filename: str, show_plot: bool):
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
        linear_mod = lm.LinearRegression()
        dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
        prices = np.reshape(prices,(len(prices),1))
        linear_mod.fit(dates,prices) #fitting the data points in the model
        plt.scatter(dates,prices,color='red') #plotting the initial datapoints 
        plt.plot(dates,linear_mod.predict(dates),color='blue',linewidth=3) #plotting the line made by linear regression
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

    # Holds the information for the given stocks
    # - stocks arg is a string of stocks separated with spaces
    def tickers(self, stocks: str):
        return yf.Tickers(stocks)

if __name__ == "__main__":
    bot = AutoInvestBot()
    csv_handler = CSV_Handler()

    # bot.update_sp500()

    # csv_handler.see_candle(['TSLA','AAPL'])

    csv_handler.get_data('./db/ZTS.csv', True)
    
    bot.account_info()

    # bot.worker_thread()

    