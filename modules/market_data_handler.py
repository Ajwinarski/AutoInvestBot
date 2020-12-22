# Common Imports
import csv
from datetime import date
import pytz
import os.path
from os import path
import schedule
import threading
import time

# Absolute Imports
from modules.csv_handler import CSV_Handler

# Alpaca Imports
import alpaca_trade_api as tradeapi
from config import *
 
# Libraries

class MarketDataHandler():
  def __init__(self):
    self._api = tradeapi.REST(API_KEY, API_SECRET_KEY, ALPACA_BASE_ENDPOINT)
    
    self._today = date.today().strftime("%Y-%m-%d")
    self._market_today = self._api.get_calendar(start=self._today, end=self._today)[0]
    self._market_open = self._market_today.open.strftime("%H:%M:%S")
    self._market_close = self._market_today.close.strftime("%H:%M:%S")
    self._commenting = False
    
    # print(type(self._market_close))
    
    # TODO: Use threading for the scheduler functions calls
    self.start_scheduler()
      
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
    self._today = date.today().strftime("%Y-%m-%d")
    self._market_today = self._api.get_calendar(start=self._today, end=self._today)[0]
    self._market_open = self._market_today.open
    self._market_close = self._market_today.close
    pass
  
  # Update the necessary csvs with todays data
  def update_market_data(self):
    csv_handler = CSV_Handler()
    csv_handler.update_sp500()
  
  # Return true if market is open, false otherwise
  def is_market_open(self):
    clock = _api.get_clock()
    if self._commenting: 
      print('The market is {}'.format('open.' if clock.is_open else 'closed.'))
    return(clock.is_open)
  
  def get_market_open_close(self):
    return self._market_open, self._market_close
  
  # TODO: Get market data based on the list of stocks you want
  
  # TODO: When the market closes, get the days data and wait for market open
  
  # TODO: Used for getting live data as the markets are open
  