from fmp_python.fmp import FMP
from datetime import date

"""
Use https://site.financialmodelingprep.com/ for data
"""

class FMP_Handler():

    def __init__(self):
        self.api_key = "zOWo5NgWst2Ill1VXevneIirrvWYgO3h"
        self.fmp = FMP(api_key=self.api_key, output_format='pandas', write_to_file=True)
    
    def get_api_key(self):
        try:
            fmp = FMP(api_key=self.api_key)
        except:
            print("API Key is invalid")
            return None
        return fmp
    
    def get_hist_data(self, stock: str, start: str = "2000-01-01", end: str = date.today()):
        # self.fmp.get_historical_chart(stock, start, end, self.api_key)