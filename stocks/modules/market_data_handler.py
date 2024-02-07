# Common Imports
import csv
import datetime
import holidays
import pytz
import os.path
from os import path
import schedule
import threading
import time

# Absolute Imports
from modules.csv_handler import CSV_Handler

# Libraries
import yfinance as yf


class MarketDataHandler():
    def __init__(self):
        # self._api = api
        # TODO: Allow custom TZ selection or auto detection
        self._tz = pytz.timezone('US/Eastern')
        self._date = datetime.date.today().strftime("%Y-%m-%d")
        self._commenting = False

        # TODO: Use threading for the scheduler functions calls
        # self.start_scheduler()

        pass

    def start_scheduler(self):
        # Get the market open and close times everyday at 1am
        schedule.every().day.at("01:00:00").do(self.update_market_times)
        # Update the market data csvs with todays data
        schedule.every().day.at(self._market_close).do(self.update_market_data)

        while True:
            schedule.run_pending()
            time.sleep(1)

        pass

    # Get the market times for the day
    def update_market_times(self):
        self._today = datetime.date.today().strftime("%Y-%m-%d")
        pass

    # Update the necessary csvs with todays data
    def update_market_data(self):
        csv_handler = CSV_Handler()
        csv_handler.update_sp500()

    # Return true if market is open, false otherwise
    def is_market_open(self, now=None):
        # If no time is given, get time
        if not now:
            now = datetime.datetime.now(self._tz)

        is_open = True
        openTime = datetime.time(hour=9, minute=30, second=0)
        closeTime = datetime.time(hour=16, minute=0, second=0)
        us_holidays = holidays.US()

        # If it's a weekend
        if now.date().weekday() > 4:
            is_open = False

        # If before 0930 or after 1600
        elif (now.time() < openTime) or (now.time() > closeTime):
            is_open = False

        # If a holiday
        elif now.strftime('%Y-%m-%d') in us_holidays:
            is_open = False

        if self._commenting:
            print('The market is {}'.format(
                'open.' if is_open else 'closed.'))

        return is_open

    def get_market_open_close(self):
        return self._market_open, self._market_close

    # TODO: Get market data based on the list of stocks you want

    # TODO: When the market closes, get the days data and wait for market open

    # TODO: Used for getting live data as the markets are open
