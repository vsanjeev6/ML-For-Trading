"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

def author():
    return 'vsanjeev6'

def compute_portvals(orders_df, start_val = 1000000, commission=9.95, impact=0.005):
    print("Strategy Evaluation:: Market Sim Code")
    orders_dates = orders_df.index
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]

    portvals = get_data(['SPY'], pd.date_range(start_date, end_date), addSPY=True, colname = 'Adj Close')
    portvals = portvals.rename(columns={'SPY': 'value'})
    dates = portvals.index

    symbol = orders_df.columns[0]
    current_cash = start_val
    shares_owned = {}
    symbol_table = {}
    #print(orders_df)

    for date in dates:
        trade = orders_df.loc[date].loc[symbol]
        if trade != 0:
            if trade < 0:
                order = 'SELL'
                shares = abs(trade)
            else:
                order = 'BUY'
                shares = trade

            if symbol not in symbol_table:
                symbol_df = get_data([symbol], pd.date_range(date, end_date), addSPY=True, colname='Adj Close')
                symbol_df = symbol_df.ffill().bfill()
                symbol_table[symbol] = symbol_df

            if order == 'BUY':
                share_change = shares
                cash_change = -symbol_table[symbol].loc[date].loc[symbol] * (1 + impact) * shares
            elif order == 'SELL':
                share_change = -shares
                cash_change = symbol_table[symbol].loc[date].loc[symbol] * (1 - impact) * shares

            shares_owned[symbol] = shares_owned.get(symbol, 0) + share_change
            current_cash += cash_change - commission

        # Current Portfolio Value
        portvals.loc[date].loc['value'] = compute_daily_portval(date, current_cash, shares_owned, symbol_table)
    return portvals

# Computing portfolio value for a day
def compute_daily_portval(curr_date, current_cash, shares_owned, symbol_table):
    shares_worth = 0
    for symbol in shares_owned:
        shares_worth += symbol_table[symbol].loc[curr_date].loc[symbol] * shares_owned[symbol]
    return current_cash + shares_worth

if __name__ == "__main__":
    pass
