""""""
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
  		  	   		  		 			  		 			     			  	 
Student Name: Vaishnavi Sanjeev  		  	   		  		 			  		 			     			  	 
GT User ID: vsanjeev6  		  	   		  		 			  		 			     			  	 
GT ID: 903797718   		  	   		  		 			  		 			     			  	 
"""

import datetime as dt
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
        return 'vsanjeev6'

    # constructor
    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """
        Constructor method
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.ql = ql.QLearner(num_states=1000, num_actions=3, alpha=0.1, gamma=0.15, rar=0.2, radr=0.99, dyna=0, verbose=False)

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

        bbp, CCI, MOM = ind.get_indicators(symbol, sd, ed)
        bbp = discretize(bbp, prices, symbol).rename({symbol:'BBP'}, axis=1)
        CCI = discretize(CCI, prices, symbol).rename({symbol:'CCI'}, axis=1)
        MOM = discretize(MOM, prices, symbol).rename({symbol:'MOM'}, axis=1)

        indicators = pd.concat([bbp, CCI, MOM], axis=1)
        indicators = indicators.loc[sd:]
        indicators['state'] = indicators['BBP'].astype(str) + indicators['CCI'].astype(str) + indicators['MOM'].astype(str)
        #print(indicators)
        initial_state = indicators.iloc[0]['state']

        self.ql.querysetstate(int(float(initial_state)))
        df_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])
        daily_price_change = get_daily_returns(prices)
        df_trades_copy = df_trades.copy()
        i = 0

        # Run through the training data several times to learn
        while i < 100:
            i += 1
            holdings = 0
            # Check for Convergence
            if i>5 and df_trades.equals(df_trades_copy):
                break
            df_trades_copy = df_trades.copy()

            for index in range(len(prices)):
                # Impact is part of rewards computation
                reward = holdings * daily_price_change.loc[prices.index[index]] * (1 - self.impact)
                # Query function updates Q-Table
                a = self.ql.query(int(float(indicators.loc[prices.index[index]]['state'])), reward)
                # Net holdings are constrained to -1000, 0, 1000
                if (a == 1) and (holdings < 1000):
                    #BUY
                    if holdings == 0: # A long trade = +1000
                        df_trades.loc[prices.index[index]] = 1000
                    elif holdings == -1000: # If current holdings = -1000, a long trade = 2000 (switching from short to long)
                        df_trades.loc[prices.index[index]] = 2000
                    holdings += df_trades.loc[prices.index[index]].values[0]

                elif (a == 2) and (holdings > -1000):
                    #SELL
                    if holdings == 0: # A short trade = -1000
                        df_trades.loc[prices.index[index]] = -1000
                    elif holdings == 1000: # If current holdings = 1000, a short trade = -2000 (switching from long to short)
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

        bbp, CCI, MOM = ind.get_indicators(symbol, sd, ed)
        bbp = discretize(bbp, prices, symbol).rename({symbol: 'BBP'}, axis=1)
        CCI = discretize(CCI, prices, symbol).rename({symbol: 'CCI'}, axis=1)
        MOM = discretize(MOM, prices, symbol).rename({symbol: 'MOM'}, axis=1)

        indicators = pd.concat([bbp, CCI, MOM], axis=1)
        indicators = indicators.loc[sd:]
        indicators['state'] = indicators['BBP'].astype(str) + indicators['CCI'].astype(str) + indicators['MOM'].astype(str)
        initial_state = indicators.iloc[0]['state']

        self.ql.querysetstate(int(float(initial_state)))
        df_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])
        holdings = 0

        for index in range(len(prices)):
            # Querysetstate function does not update the Q-Table
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

def discretize(data, prices, symbol, steps=10):
    labels = range(steps)
    discret_data = pd.DataFrame(0, index=prices.index,columns=[symbol])
    # In-built pandas function for discretization
    discret_data[symbol] = pd.qcut(data, q=steps, labels=labels, precision=0, duplicates='drop')
    discret_data.fillna(0, inplace=True)
    #print("Discretized Data",discret_data)
    return discret_data

if __name__ == "__main__":
    print("One does not simply think up a strategy")
