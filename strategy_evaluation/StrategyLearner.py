""""""

import numpy as np

"""  		  	   		  		 			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""

import datetime as dt
import random

import pandas as pd
import util as ut
import QLearner as ql
import indicators as ind


class StrategyLearner(object):
    """
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output.
    :type verbose: bool
    :param impact: The market impact of each transaction, defaults to 0.0
    :type impact: float
    :param commission: The commission amount charged, defaults to 0.0
    :type commission: float
    """
    def author(self):
        return "pcometti3"  # replace tb34 with your Georgia Tech username
    # constructor
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """
        Constructor method
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.ql = ql.QLearner(num_states=1000, num_actions=3, alpha=0.2, gamma=0.9, rar=0.5, radr=0.99, dyna=0, verbose=False)

        # this method should create a QLearner, and train it for trading

    def add_evidence(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 1, 1),
            sv=10000,
    ):
        """
        Trains your strategy learner over a given time frame.

        :param symbol: The stock symbol to train on
        :type symbol: str
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008
        :type sd: datetime
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009
        :type ed: datetime
        :param sv: The starting value of the portfolio
        :type sv: int
        """

        # add your code to do learning here
        # example usage of the old backward compatible util function
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

        bbp, CCI, _, ROC, _ = ind.get_indicators(symbol, sd, ed)
        bbp = discretize(bbp).rename({symbol:'BBP'}, axis=1)
        CCI = discretize(CCI).rename({symbol:'CCI'}, axis=1)
        ROC = discretize(ROC).rename({symbol:'ROC'}, axis=1)

        indicators = pd.concat([bbp, CCI, ROC], axis=1)
        indicators = indicators.loc[sd:]
        indicators['state'] = indicators['BBP'].astype(str) + indicators['CCI'].astype(str) + \
                              indicators['ROC'].astype(str)
        initial_state = indicators.iloc[0]['state']

        self.ql.querysetstate(int(float(initial_state)))

        df_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])

        daily_price_change = get_daily_returns(prices)

        df_trades_copy = df_trades.copy()
        i = 0

        while i < 100: #30 iteration limit
            i += 1
            holdings = 0

            if i>5 and df_trades.equals(df_trades_copy):
                # convergence
                break

            df_trades_copy = df_trades.copy()

            for index in range(len(prices)):
                reward = holdings * daily_price_change.loc[prices.index[index]] * (1 - self.impact)
                a = self.ql.query(int(float(indicators.loc[prices.index[index]]['state'])), reward)
                if (a == 1) and (holdings < 1000):
                    #BUY
                    if holdings == 0:
                        df_trades.loc[prices.index[index]] = 1000
                    elif holdings == -1000:
                        df_trades.loc[prices.index[index]] = 2000
                    holdings += df_trades.loc[prices.index[index]].values[0]

                elif (a == 2) and (holdings > -1000):
                    #SELL
                    if holdings == 0:
                        df_trades.loc[prices.index[index]] = -1000
                    elif holdings == 1000:
                        df_trades.loc[prices.index[index]] = -2000
                    holdings += df_trades.loc[prices.index[index]].values[0]

            # this method should use the existing policy and test it against new data

    def testPolicy(
            self,
            symbol="IBM",
            sd=dt.datetime(2009, 1, 1),
            ed=dt.datetime(2010, 1, 1),
            sv=10000,
    ):
        """
        Tests your learner using data outside of the training data

        :param symbol: The stock symbol that you trained on on
        :type symbol: str
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008
        :type sd: datetime
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009
        :type ed: datetime
        :param sv: The starting value of the portfolio
        :type sv: int
        :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating
            a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.
            Values of +2000 and -2000 for trades are also legal when switching from long to short or short to
            long so long as net holdings are constrained to -1000, 0, and 1000.
        :rtype: pandas.DataFrame
        """

        # here we build a fake set of trades
        # your code should return the same sort of data
        # add your code to do learning here
        # example usage of the old backward compatible util function
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

        bbp, CCI, _, ROC, _ = ind.get_indicators(symbol, sd, ed)

        bbp = discretize(bbp).rename({symbol: 'BBP'}, axis=1)
        CCI = discretize(CCI).rename({symbol: 'CCI'}, axis=1)
        ROC = discretize(ROC).rename({symbol: 'ROC'}, axis=1)

        indicators = pd.concat([bbp, CCI, ROC], axis=1)
        indicators = indicators.loc[sd:]
        indicators['state'] = indicators['BBP'].astype(str) + indicators['CCI'].astype(str) + \
                              indicators['ROC'].astype(str)
        initial_state = indicators.iloc[0]['state']


        self.ql.querysetstate(int(float(initial_state)))

        df_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])

        holdings = 0

        for index in range(len(prices)):
            a = self.ql.querysetstate(int(float(indicators.loc[prices.index[index]]['state'])))
            if (a == 1) and (holdings < 1000):
                # BUY
                if holdings == 0:
                    df_trades.loc[prices.index[index]] = 1000
                elif holdings == -1000:
                    df_trades.loc[prices.index[index]] = 2000
                holdings += df_trades.loc[prices.index[index]].values[0]

            elif (a == 2) and (holdings > -1000):
                # SELL
                if holdings == 0:
                    df_trades.loc[prices.index[index]] = -1000
                elif holdings == 1000:
                    df_trades.loc[prices.index[index]] = -2000
                holdings += df_trades.loc[prices.index[index]].values[0]

        return df_trades

def get_daily_returns(port_val):
    daily_returns = port_val.copy()
    daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
    return daily_returns

def discretize(data, steps=10):
    stepsize = round(len(data) / steps)
    data1 = data.sort_values()
    treshold = np.zeros(steps - 1)
    for i in range(steps - 1):
        treshold[i] = data1.iloc[(i + 1) * stepsize]

    for i in range(len(data)):
        if data.iloc[i] <= treshold[0]:
            data.iloc[i] = 0
        elif treshold[0] < data.iloc[i] <= treshold[1]:
            data.iloc[i] = 1
        elif treshold[1] < data.iloc[i] <= treshold[2]:
            data.iloc[i] = 2
        elif treshold[2] < data.iloc[i] <= treshold[3]:
            data.iloc[i] = 3
        elif treshold[3] < data.iloc[i] <= treshold[4]:
            data.iloc[i] = 4
        elif treshold[4] < data.iloc[i] <= treshold[5]:
            data.iloc[i] = 5
        elif treshold[5] < data.iloc[i] <= treshold[6]:
            data.iloc[i] = 6
        elif treshold[6] < data.iloc[i] <= treshold[7]:
            data.iloc[i] = 7
        elif treshold[7] < data.iloc[i] <= treshold[8]:
            data.iloc[i] = 8
        else:
            data.iloc[i] = 9

    return (data.astype(int)).to_frame()


if __name__ == "__main__":
    print("One does not simply think up a strategy")
