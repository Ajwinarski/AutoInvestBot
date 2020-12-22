# Common Imports
import csv
import time
# import threading                          # Incorporate async processes in this application
# from multiprocessing import Process
from enum import Enum, unique
import os.path
from os import path
from datetime import datetime

# Absolute Imports
from modules.csv_handler import CSV_Handler
from modules.market_data_handler import MarketDataHandler

# Alpaca imports
import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
from config import *

# Libraries
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import plotly.graph_objs as go
import numpy as np
from sklearn import linear_model as lm

# GUI Import
from gui import *

@unique
class Action(Enum):
    Buy = 1
    Sell = 2
    
def main():
    # bot = AutoInvestBot()
    market = MarketDataHandler()    # TODO: Move this to AutoInvestBot
    
    # bot.update_sp500()
    # bot.csv.see_candle(['TSLA','AAPL'])

    # ZTS_data = bot.csv.get_data('./db/ZTS.csv', False)
    # bot.csv.show_LR_plot(ZTS_data[0], ZTS_data[1])
    
    # bot.account_info()
    # bot.worker_thread()

    # print(market._market_close)
    # print(market.update_market_times())
    

    # GUI
    # app = QApplication(sys.argv)

    # window = MainWindow()
    # window.show()

    # app.exec_()

if __name__ == "__main__":
    main()

    

    
