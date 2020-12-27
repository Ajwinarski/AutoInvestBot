# Common Imports
import csv
import time
# import threading                          # Incorporate async processes in this application
# from multiprocessing import Process
import os.path
from os import path

# Absolute Imports
from modules.csv_handler import CSV_Handler
from modules.market_data_handler import MarketDataHandler

# GUI Import
from gui import *


def main():
    # aib = AutoInvestBot()
    market = MarketDataHandler()    # TODO: Move this to AutoInvestBot

    # aib.csv.see_candle(['TSLA','AAPL'])

    ZTS_data = aib.csv.get_data('./db/ZTS.csv', False)
    aib.csv.show_LR_plot(ZTS_data[0], ZTS_data[1])

    # aib.account_info()
    # aib.worker_thread()

    # GUI
    # app = QApplication(sys.argv)

    # window = MainWindow()
    # window.show()

    # app.exec_()


if __name__ == "__main__":
    main()
