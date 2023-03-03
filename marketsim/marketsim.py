""""""  		  	   		  		 			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data

def author():
    return 'vsanjeev6'

def compute_portvals(  		  	   		  		 			  		 			     			  	 
    orders_file="./orders/orders.csv",  		  	   		  		 			  		 			     			  	 
    start_val=1000000,  		  	   		  		 			  		 			     			  	 
    commission=9.95,  		  	   		  		 			  		 			     			  	 
    impact=0.005,  		  	   		  		 			  		 			     			  	 
):
    """  		  	   		  		 			  		 			     			  	 
    Computes the portfolio values.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		  		 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		  		 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
    :type start_val: int  		  	   		  		 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		  		 			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		  		 			  		 			     			  	 
    # code should work correctly with either input

    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    #print(orders_df)
    orders_df.sort_index(inplace = True)
    #print(orders_df)
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]

    symbols = list(set(orders_df['Symbol'].values))
    dates = pd.date_range(start_date, end_date)
    #print("Dates:", dates)
    #print("Symbols:", symbols)

    """  		  	   		  		 			  		 			     			  	 
    Prices Dataframe  		  	   		  		 			  		 			     			  	 
    """
    prices_df = get_data(symbols, dates)
    # Handling incomplete data by filling forward first and then backward
    prices_df.fillna(method="ffill",inplace=True)
    prices_df.fillna(method="bfill", inplace=True)

    # An additional column "Cash", with values 1
    prices_df['Cash'] = np.ones(prices_df.shape[0])
    #print(prices_df)

    """  		  	   		  		 			  		 			     			  	 
    Trades Dataframe  		  	   		  		 			  		 			     			  	 
    """
    trades_df = prices_df.copy()
    trades_df.ix[:, :] = 0

    # Loop over orders index
    for date in prices_df.index:
        if date in orders_df.index:
            sub_order = orders_df.ix[date:date]
            #print(sub_order)
            for i in range(0, sub_order.shape[0]):
                sym = sub_order.ix[i, 'Symbol']
                order = sub_order.ix[i, 'Order']
                shares = sub_order.ix[i, 'Shares']
                # impact = no. of orders in transaction * price of each share * impact. deduct impact for every transaction
                impact_deduction = shares * prices_df.ix[date, sym] * impact

                if order == 'SELL':
                    trades_df.ix[date, sym] += shares * (-1)
                    trades_df.ix[date, 'Cash'] += prices_df.ix[date, sym] * shares
                    # Deduction from cash balance for EACH TRADE
                    trades_df.ix[date, 'Cash'] = trades_df.ix[date, 'Cash'] - commission - impact_deduction
                if order == 'BUY':
                    trades_df.ix[date, sym] += shares
                    trades_df.ix[date, 'Cash'] += prices_df.ix[date, sym] * shares * (-1)
                    # Deduction from cash balance for EACH TRADE
                    trades_df.ix[date, 'Cash'] = trades_df.ix[date, 'Cash'] - commission - impact_deduction
    #print(trades_df)

    """  		  	   		  		 			  		 			     			  	 
    Holdings Dataframe  		  	   		  		 			  		 			     			  	 
    """
    holdings_df = trades_df.copy()
    holdings_df.ix[:, :] = 0
    #On first day, all you got is cash (no stock holdings)
    holdings_df.ix[0, 'Cash'] = start_val

    # special handling of 1st row
    holdings_df.ix[0, :] += trades_df.ix[0, :]

    for i in range(1, holdings_df.shape[0]):
        holdings_df.ix[i, :] = holdings_df.ix[i - 1, :] + trades_df.ix[i, :]
    #print(holdings_df)

    """  		  	   		  		 			  		 			     			  	 
    Values Dataframe  		  	   		  		 			  		 			     			  	 
    """
    values_df = holdings_df.copy()
    values_df = prices_df * holdings_df
    #print(values_df)

    portvals = values_df.sum(axis=1)
    print(portvals)

    return portvals  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Helper function to test code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		  		 			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		  		 			  		 			     			  	 
    # Define input parameters  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    of = "./orders/additional_orders/orders-short.csv"
    sv = 1000000  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Process orders  		  	   		  		 			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)  		  	   		  		 			  		 			     			  	 
    if isinstance(portvals, pd.DataFrame):  		  	   		  		 			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  		 			  		 			     			  	 
    else:  		  	   		  		 			  		 			     			  	 
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    start_date = portvals.index.min()
    end_date = portvals.index.max()
    """  		  	   		  		 			  		 			     			  	 
    From Project 2 - optimization.py  		  	   		  		 			  		 			     			  	 
    """
    # Cumulative Return
    cr = (portvals[-1]/portvals[0]) -1
    # Daily Return
    daily_returns = (portvals/portvals.shift(1)) -1
    daily_returns = daily_returns[1:] # Remove first row
    # Average Daily Return
    adr = daily_returns.mean()
    # StDev of Daily Returns (Sample standard deviation)
    sddr = daily_returns.std(ddof=1)
    # Sharpe Ratio
    sr = np.sqrt(252) * (adr / sddr)
    # Compare portfolio against $SPX
   
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sr}")
    #print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cr}")
    #print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of Fund: {sddr}")
    #print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of Fund: {adr}")
    #print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
