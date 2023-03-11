"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718
"""

"""
Implement Part 1: Theoretically Optimal Strategy
"""

import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals

def author():
    return 'vsanjeev6'


def testPolicy(symbol="JPM",  sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
    dates = pd.date_range(sd, ed)
    df_prices = get_data([symbol], dates)
    prices = df_prices[symbol]
    prices = prices / prices[0]

    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df1['Order'] = prices < prices.shift(-1)

    df1['Order'].replace(True, 'BUY', inplace=True)
    df1['Order'].replace(False, 'SELL', inplace=True)
    print(df1)

    df2['Order'] = df1['Order'].append(
        df1['Order'].shift(1).replace('BUY', 'TMP').replace('SELL', 'BUY').replace('TMP', 'SELL').dropna())
    print(df2)

    df2['Symbol'] = symbol
    df2['Shares'] = 1000
    df2.sort_index(inplace=True)

    print(df2)
    return df2

def test_code():
    test_sd = dt.datetime(2008, 1, 1)
    test_ed = dt.datetime(2009,12,31)
    sv = 100000
    symbol = 'JPM'

    dates = pd.date_range(test_sd, test_ed)
    prices_all = get_data([symbol], dates)

    prices = prices_all[symbol]
    prices = prices / prices[0]


    df3 = testPolicy(symbol="JPM", sd=test_sd, ed=test_ed, sv=100000)
    port_vals = compute_portvals(df3, test_sd, test_ed, sv, 0, 0)
    # port_vals

    df3 = pd.DataFrame(index=prices.index, columns=['Order', 'Symbol', 'Shares'])
    df3['Order'] = 'BUY'
    df3['Symbol'] = 'JPM'
    df3['Shares'] = 1000
    df4 = df3[:1]
    # df4
    df5 = df3.copy().tail(1)
    df5['Order'] = 'BUY'
    df5['Symbol'] = 'JPM'
    df5['Shares'] = 0
    df4 = df4.append(df5)
    # df4
    bench_vals = compute_portvals(df4, test_sd, test_ed, sv, 0, 0)

    # normalize
    bench_vals = bench_vals / bench_vals[0]
    port_vals = port_vals / port_vals[0]

    # bench_vals
    plt.figure(figsize=(14, 8))
    plt.title("TheoreticallyOptimalStrategy")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(bench_vals, label="benchmark", color="purple")
    plt.plot(port_vals, label="theoretical", color="red")
    plt.legend()
    plt.savefig("theoretical.png", bbox_inches='tight')
    plt.show()
    plt.clf()


if __name__ == "__main__":
    test_code()
