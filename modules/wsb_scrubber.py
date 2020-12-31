import praw
import re
import requests
import yfinance as yf

reddit = praw.Reddit(
     client_id="Un4P70QgUZ_b_w",
     client_secret="DYPRCJrvaNM7gfcPJbZ8Hl2lIkO7ow",
     user_agent="my user agent"
)

# for submission in reddit.subreddit("wallstreetbets").new():
#   x = re.findall("[$][A-Z]+|[A-Z]+[A-Z]+", str(submission.title))
  
#   print(submission.title)
#   print(x)
  
def check_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            # return x['name']
            return True
        return False


result = check_symbol("YOLO")
print(result)

checker = yf.Ticker("MSFT")
print(checker.info['longname'])