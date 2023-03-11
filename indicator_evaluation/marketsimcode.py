"""
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


def compute_portvals(orders_df, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), start_val = 1000000, commission=9.95, impact=0.005):
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
    orders_dates = orders_df.index
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]

    symbols = list(set(orders_df['Symbol'].values))
    dates = pd.date_range(start_date, end_date)
    print("Dates:", dates)
    print("Symbols:", symbols)

    """  		  	   		  		 			  		 			     			  	 
    Prices Dataframe  		  	   		  		 			  		 			     			  	 
    """
    prices_df = get_data(symbols, dates)
    # Handling incomplete data by filling forward first and then backward
    prices_df.fillna(method="ffill",inplace=True)
    prices_df.fillna(method="bfill", inplace=True)

    # An additional column "Cash", with values 1
    prices_df['Cash'] = np.ones(prices_df.shape[0])
    # print(prices_df)

    """  		  	   		  		 			  		 			     			  	 
    Trades Dataframe  		  	   		  		 			  		 			     			  	 
    """
    trades_df = prices_df.copy()
    trades_df.ix[:, :] = 0

    # Loop over the prices dataframe index
    # Update the trades dataframe only during dates an order was placed
    for date in prices_df.index:
        if date in orders_df.index:
            orders_on_same_day = orders_df.ix[date:date]
            # print(orders_on_same_day)
            for i in range(0, orders_on_same_day.shape[0]):
                sym = orders_on_same_day.ix[i, 'Symbol']
                order = orders_on_same_day.ix[i, 'Order']
                shares = orders_on_same_day.ix[i, 'Shares']
                # impact = f(no. of shares * share price * impact %)
                # Deduct impact for every transaction from cash
                impact_deduction = shares * prices_df.ix[date, sym] * impact

                if order == 'SELL':
                    trades_df.ix[date, sym] = trades_df.ix[date, sym] + (shares * (-1))
                    trades_df.ix[date, 'Cash'] = trades_df.ix[date, 'Cash'] + (prices_df.ix[date, sym] * shares)
                    # Deduction from cash balance for EACH TRADE
                    trades_df.ix[date, 'Cash'] = trades_df.ix[date, 'Cash'] - commission - impact_deduction
                if order == 'BUY':
                    trades_df.ix[date, sym] = trades_df.ix[date, sym] + shares
                    trades_df.ix[date, 'Cash'] = trades_df.ix[date, 'Cash'] + (prices_df.ix[date, sym] * shares * (-1))
                    # Deduction from cash balance for EACH TRADE
                    trades_df.ix[date, 'Cash'] = trades_df.ix[date, 'Cash'] - commission - impact_deduction
    # print(trades_df)

    """  		  	   		  		 			  		 			     			  	 
    Holdings Dataframe  		  	   		  		 			  		 			     			  	 
    """
    holdings_df = trades_df.copy()
    # Initialize all entries to 0's
    holdings_df.ix[:, :] = 0
    # On first day, all you got is cash (no stock holdings)
    holdings_df.ix[0, 'Cash'] = start_val

    # 1st row
    holdings_df.ix[0, :] += trades_df.ix[0, :]

    for i in range(1, holdings_df.shape[0]):
        holdings_df.ix[i, :] = holdings_df.ix[i - 1, :] + trades_df.ix[i, :]
    # print(holdings_df)

    """  		  	   		  		 			  		 			     			  	 
    Values Dataframe  		  	   		  		 			  		 			     			  	 
    """
    values_df = holdings_df.copy()
    values_df = prices_df * holdings_df
    # print(values_df)

    portvals = values_df.sum(axis=1)
    # print(portvals)

    return portvals

if __name__ == "__main__":
    pass
