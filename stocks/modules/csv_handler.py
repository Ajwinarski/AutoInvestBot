# Common Imports
import csv
from datetime import date
import os
import ssl

# Absolute Imports
from modules.algorithms.linear_regression import LinearRegression as lr

# Libraries
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pandas_market_calendars as pmc
# from pandas_datareader import data
# from pandas_datareader._utils import RemoteDataError
import plotly.graph_objs as go
from sklearn import linear_model as lm
import yfinance as yf
from fmp_python.fmp import FMP

class CSV_Handler:
    """
    Create, remove, modify, and read CSV file data.

    Args:
        None.

    Returns:
        None.
    """

    def __init__(self):
        self.update_watchlist()
        # self.symbols: list = self.get_symbols()

    def update_watchlist(self):
        """
        Update the stock data for relevant tickers from Yahoo! Finance.

        Args:
            self: parent class data passing.

        Returns:
            None.
        """    
        directory = "./db/watchlist/"
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".csv"): 
                print(os.path.join(directory, filename))
                print(file.split(sep='.')[0])
                continue
            else:
                continue
        pass

    # Get list of symbols from a csv file
    def get_symbols(self) -> list:
        symbols = []

        csv_data = pd.read_csv('Symbols')

        # Check if Symbols file is empty
        if not csv_data.empty:
            next(csv_data)  # skip first row
            for row in csv_data:
                symbols.append(str(row[0]))

        return symbols

    def get_csv_data(self, filename: str):
        try:
            csv_file = open('./db/'+filename+'.csv', 'r')
            return csv.reader(csv_file)
        except FileNotFoundError:
            # Create an empty csv file for the filename given
            with open('./db/'+filename+'.csv', 'w') as file:
                return file

    def get_sp500(self):
        # Get the list of S&P 500 tickers
        sp500_tickers = yf.Tickers('^GSPC').tickers
        print("S&P500: ", sp500_tickers)

        # Create an empty DataFrame to store the stock data
        sp500_data = pd.DataFrame()

        # Retrieve stock data for each ticker
        for ticker in sp500_tickers:
            symbol = yf.Ticker(ticker)
            data = symbol.history(period="1d")
            # Add a 'Symbol' column with the ticker symbol
            data['Symbol'] = symbol.ticker
            sp500_data = pd.concat([sp500_data, data])

        # Save the stock data to CSV
        sp500_data.to_csv('db/S&P500.csv')
        pass

    def download_stock_data(self, stock: str, location: str):
        try:
            os.listdir(location)

            if stock not in os.listdir(location):
                try:
                    data = yf.download(stock)
                    data.to_csv('./db/'+stock+'.csv')
                    self.symbols.append(stock)
                except:
                    print("Stock symbol not found")
        except:
            pass
        
        pass

    # def add_stock_to_watchlist(self):


    # Pulls the current S&P 500 companies
    def update_sp500(self, update_all_files: bool = False):
        try:
            table = pd.read_html(
                io='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        except:
            ssl._create_default_https_context = ssl._create_unverified_context
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
        new_stocks = []

        for stock in stocks:
            if stock is not self.symbols:
                new_stocks.append(stock)

        for stock in new_stocks:
            print("Stock: " + stock)
            # data = yf.download(stock, start, end)
            # data.to_csv('./db/'+stock+'.csv')

    def read_csvs(self, symbols):
        # for symbol in symbols:

        pass

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
