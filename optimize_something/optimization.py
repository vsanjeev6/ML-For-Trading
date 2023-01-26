""""""  		  	   		  		 			  		 			     			  	 
"""MC1-P2: Optimize a portfolio.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import matplotlib.pyplot as plt  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data
from scipy.optimize import minimize
  		  	   		  		 			  		 			     			  	 
# This is the function that will be tested by the autograder  		  	   		  		 			  		 			     			  	 
# The student must update this code to properly implement the functionality  		  	   		  		 			  		 			     			  	 
def optimize_portfolio(  		  	   		  		 			  		 			     			  	 
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 1, 1),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    gen_plot=False,  		  	   		  		 			  		 			     			  	 
):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		  		 			  		 			     			  	 
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		  		 			  		 			     			  	 
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		  		 			  		 			     			  	 
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		  		 			  		 			     			  	 
    statistics.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
    :type sd: datetime  		  	   		  		 			  		 			     			  	 
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
    :type ed: datetime  		  	   		  		 			  		 			     			  	 
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		  		 			  		 			     			  	 
        symbol in the data directory)  		  	   		  		 			  		 			     			  	 
    :type syms: list  		  	   		  		 			  		 			     			  	 
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		  		 			  		 			     			  	 
        code with gen_plot = False.  		  	   		  		 			  		 			     			  	 
    :type gen_plot: bool  		  	   		  		 			  		 			     			  	 
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		  		 			  		 			     			  	 
        standard deviation of daily returns, and Sharpe ratio  		  	   		  		 			  		 			     			  	 
    :rtype: tuple  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Read in adjusted closing prices for given symbols, date range  		  	   		  		 			  		 			     			  	 
    dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			     			  	 
    prices_all = get_data(syms, dates)  # automatically adds SPY

    # Handling possible incomplete data by filling forward first and then backward
    prices_all.fillna(method="ffill",inplace=True)
    prices_all.fillna(method="bfill", inplace=True)

    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    no_of_assets = len(syms)
    init_guess_alloc_array = np.full(no_of_assets,(1.0/no_of_assets))
    #print(no_of_assets,init_guess_alloc_array)

    bnds = tuple((0, 1) for _ in range(no_of_assets))
    cons = ({'type': 'eq', 'fun': lambda inputs: sum(inputs)-1})
    #Minimize function optimizes just a single scalar. So ensure that the function passed as an arg returns just one value
    min_result = minimize(calc_SR,init_guess_alloc_array, args=(prices), method='SLSQP', constraints= cons, bounds = bnds)
    #print("X={}. Y={}".format(min_result.x, min_result.fun))

    optimal_allocation = min_result.x
    daily_port_val, cr, adr, sddr = portfolio_calculations(optimal_allocation, prices)
    #Don't need to reverse sign of SR except when calling the minimize() function
    sr = -calc_SR(optimal_allocation, prices)
    #print(bnds, cons, optimal_allocation)
    #print(optimal_allocation, sum(optimal_allocation))

    # Get daily portfolio value  		  	   		  		 			  		 			     			  	 
    port_val = daily_port_val  # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot  		  	   		  		 			  		 			     			  	 
    if gen_plot:  		  	   		  		 			  		 			     			  	 
        # add code to plot here  		  	   		  		 			  		 			     			  	 
        df_temp = pd.concat([port_val, (prices_SPY/prices_SPY[0])], keys=["Portfolio with [IBM, X, GLD, JPM]", "SPY"], axis=1)
        graph = df_temp.plot(title = "Comparing Optimal Normalized Portfolio Value and SPY", grid = True)
        graph.set_xlabel("Date from 2008-06-01 to 2009-06-01")
        graph.set_ylabel("Normalized Price")
        plt.savefig('./images/Figure1.png')
        plt.clf()
        pass  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    return optimal_allocation, cr, adr, sddr, sr
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This function WILL NOT be called by the auto grader.  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]
  		  	   		  		 			  		 			     			  	 
    # Assess the portfolio  		  	   		  		 			  		 			     			  	 
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		  		 			  		 			     			  	 
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Print statistics  		  	   		  		 			  		 			     			  	 
    #print(f"Start Date: {start_date}")
    #print(f"End Date: {end_date}")
    #print(f"Symbols: {symbols}")
    #print(f"Allocations:{allocations}")
    #print(f"Sharpe Ratio: {sr}")
    #print(f"Volatility (stdev of daily returns): {sddr}")
    #print(f"Average Daily Return: {adr}")
    #print(f"Cumulative Return: {cr}")

def portfolio_calculations(allocs, prices):

    normed_prices = prices.divide(prices.iloc[0])
    alloced_prices = normed_prices * allocs

    #Assuming an initial investment of $1
    pos_value = 1 * alloced_prices
    daily_port_val = pos_value.sum(axis=1)

    # Cumulative Return
    cr = (daily_port_val[-1] / daily_port_val[0]) - 1

    # Average Daily Return
    daily_returns = (daily_port_val / daily_port_val.shift(1)) - 1
    daily_returns = daily_returns[1:]
    adr = daily_returns.mean()

    # StDev of Daily Returns (Sample standard deviation)
    sddr = daily_returns.std(ddof=1)
    return daily_port_val, cr, adr, sddr

def calc_SR(allocs, prices):
    daily_port_val, cr, adr, sddr = portfolio_calculations(allocs, prices)
    # Sharpe Ratio (daily sampling)
    sr = np.sqrt(252) * (adr / sddr)
    #We want to minimize allocations to maximize Sharpe Ratio. But with only minimize function available,
    return -sr
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    # This code WILL NOT be called by the auto grader  		  	   		  		 			  		 			     			  	 
    # Do not assume that it will be called  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
