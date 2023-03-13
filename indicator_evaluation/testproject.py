"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718
"""

from util import get_data, plot_data
import datetime as dt
import pandas as pd
import TheoreticallyOptimalStrategy as tos

df_trades = tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)

if __name__ == "__main__":
    pass
