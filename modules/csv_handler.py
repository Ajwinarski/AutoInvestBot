# Common Imports
import csv
from datetime import date
from os import path

# Absolute Imports
from modules.algorithms.linear_regression import LinearRegression as lr

# Libraries
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from sklearn import linear_model as lm
import yfinance as yf


class CSV_Handler:
    def __init__(self):
        pass

    # Pulls the current S&P 500 companies
    def update_sp500(self, update_all_files: bool = False):
        table = pd.read_html(
            io='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        df = table[0]
        df.to_csv("./db/S&P500-Info.csv")
        df.to_csv("./db/S&P500-Symbols.csv", columns=['Symbol'])

        if update_all_files:
            test_stocks = pd.read_csv("./db/S&P500-Symbols.csv", squeeze=True)
            test_stocks_list = test_stocks.Symbol.to_list()

            self.create_csvs(test_stocks_list, start="2020-1-1",
                             end=date.today().strftime("%Y-%m-%d"))

    # Generate CSVs containing all stock data or a portion of the stock data
    def create_csvs(self, stocks, start=None, end=None):
        if type(stocks) is not list:
            stocks = [stocks]

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
                date_time_obj = date.strptime(row[0], '%Y-%m-%d')
                dates.append((int)(date_time_obj.strftime("%Y%m%d")))
                open_prices.append(float(row[1]))
                close_prices.append(float(row[4]))
                high_prices.append(float(row[2]))
                low_prices.append(float(row[3]))
                volume.append(int(row[6]))

        if show_plot:
            LR = lr.show_LR_plot(dates, open_prices)

        return dates, open_prices, close_prices, high_prices, low_prices, volume

    # View the candle charts of the given stock(s)
    def see_candle(self, stocks):
        if type(stocks) is not list:
            stocks = [stocks]

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
