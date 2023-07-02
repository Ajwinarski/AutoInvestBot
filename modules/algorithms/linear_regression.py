# Libraries
from matplotlib import pyplot as plt
import numpy as np
from sklearn import linear_model as lm


class LinearRegression():
    def __init__(self):
        pass

    def show_LR_plot(self, dates, prices):
        # Do for roughly the following date ranges (3 month, 6 month, 1 year, 3 year, 5 year)
        # roughly because we'll use 20 trading days to signify a month
        # converting to matrix of n X 1
        dates = np.reshape(dates, (len(dates), 1))
        prices = np.reshape(prices, (len(prices), 1))

        # set up the lm models we'll use (for each time horizon)
        linear_mod_1m = lm.LinearRegression()
        linear_mod_3m = lm.LinearRegression()
        linear_mod_6m = lm.LinearRegression()
        linear_mod_1y = lm.LinearRegression()
        linear_mod_3y = lm.LinearRegression()
        linear_mod_5y = lm.LinearRegression()

        # Fitting the data points in the model (for each time horizon)
        linear_mod_1m.fit(dates[-20:], prices[-20:])
        linear_mod_3m.fit(dates[-60:], prices[-60:])
        linear_mod_6m.fit(dates[-120:], prices[-120:])
        linear_mod_1y.fit(dates[-252:], prices[-252:])
        linear_mod_3y.fit(dates[-756:], prices[-756:])
        linear_mod_5y.fit(dates[-1260:], prices[-1260:])

        # All data is plotted on a scatter
        plt.scatter(dates, prices, color='red')

        # Plot each of the linear regressions
        plt.plot(dates[-20:], linear_mod_1m.predict(dates[-20:]),
                 label="1 month")
        plt.plot(dates[-60:], linear_mod_3m.predict(dates[-60:]),
                 label="3 month")
        plt.plot(dates[-120:], linear_mod_6m.predict(dates[-120:]),
                 color='green', linewidth=3, label="6 month")
        plt.plot(dates[-252:], linear_mod_1y.predict(dates[-252:]),
                 color='blue', linewidth=3, label="1 year")
        plt.plot(dates[-756:], linear_mod_3y.predict(dates[-756:]),
                 color='indigo', linewidth=3, label="3 year")
        plt.plot(dates[-1260:], linear_mod_5y.predict(dates[-1260:]),
                 color='violet', linewidth=3, label="5 year")

        plt.legend(loc="upper left")
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
