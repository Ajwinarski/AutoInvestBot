# Common Imports
import csv
import time
# import threading                          # Incorporate async processes in this application
# from multiprocessing import Process
import os.path
from os import path

# Absolute Imports
from auto_invest_bot import AutoInvestBot
from modules.csv_handler import CSV_Handler
from modules.market_data_handler import MarketDataHandler
from modules.fmp_handler import FMP_Handler

# GUI Import
from gui import *
from gui_gpt import *

# TODO: Rename this project to METF/MeTF/MEtf (My ETF)
def main():
    # aib = AutoInvestBot()
    # market = MarketDataHandler()   # TODO: Move this to AutoInvestBot

    # aib.csv.create_csvs(['TSLA', 'AAPL'])
    # aib.csv.see_candle(['AAPL'])

    # ZTS_data = aib.csv.get_data('./db/ZTS.csv', False)
    # aib.csv.show_LR_plot(ZTS_data[0], ZTS_data[1])

    # aib.account_info()
    # aib.worker_thread()

    # csv_handler = CSV_Handler()

    fmp = FMP_Handler()

    # # GUI
    # app = QApplication(sys.argv)

    # # Window setup
    # window = MainWindow(csv_handler)
    # window.show()

    # # App execution
    # # app.exec_()
    # sys.exit(app.exec_())


if __name__ == "__main__":
    main()
