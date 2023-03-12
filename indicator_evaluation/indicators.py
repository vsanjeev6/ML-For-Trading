"""
Student Name: Vaishnavi Sanjeev  		  	   		  		 			  		 			     			  	 
GT User ID: vsanjeev6  		  	   		  		 			  		 			     			  	 
GT ID: 903797718   		  	   		  		 			  		 			     			  	 
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt

"""
Register datetime converter
To avoid warings: 
FutureWarning: Using an implicitly registered datetime converter for a matplotlib plotting method. 
The converter was registered by pandas on import.
Future versions of pandas will require you to explicitly register matplotlib converters.
"""
pd.plotting.register_matplotlib_converters()

"""
Indicator 1: Exponential Moving Average
"""

def ema(sd, ed, symbol):
    # Window size 20 (Short Term EMA)
    delta = dt.timedelta(20 * 2)
    df_price = get_data([symbol], pd.date_range((sd - delta), ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()
    df_ema_20 = df_price.ewm(span=20, adjust=False).mean()

    # Window size 50 (Long Term EMA)
    delta = dt.timedelta(50 * 2)
    df_price = get_data([symbol], pd.date_range((sd - delta), ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()
    df_ema_50 = df_price.ewm(span=50, adjust=False).mean()

    # Remove the dates before the start_date
    df_ema_20 = df_ema_20.truncate(before=sd)
    df_ema_50 = df_ema_50.truncate(before=sd)
    df_price = df_price.truncate(before=sd)

    # Normalization
    normalized_df_price = df_price[symbol] / df_price[symbol][0]
    normalized_df_ema_20 = df_ema_20[symbol] / df_ema_20[symbol][0]
    normalized_df_ema_50 = df_ema_50[symbol] / df_ema_50[symbol][0]

    # Generate BUY and SELL signals
    df_price['Signal'] = 0.0
    df_price['Signal'] = np.where(df_ema_20 > df_ema_50, 1.0, 0.0)
    df_price['Position'] = df_price['Signal'].diff()
    print(df_price)

    # Plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(normalized_df_price, label="JPM price (normalized)", color="blue")
    plt.plot(normalized_df_ema_20, label="EMA (20)", color="red")
    plt.plot(normalized_df_ema_50, label="EMA (50)", color="purple")

    # Add BUY and SELL signals to the chart
    ax.plot(df_price.loc[df_price.Position == 1.0].index, normalized_df_ema_20[df_price.Position == 1.0], '^', markersize=10, color='g', label='BUY')
    ax.plot(df_price.loc[df_price.Position == -1.0].index, normalized_df_ema_20[df_price.Position == -1.0], 'v', markersize=10, color='r', label='SELL')

    # Add chart labels and legend
    plt.xlabel('Date')
    plt.xticks(rotation=30)
    plt.ylabel('Price')
    plt.title('EMA Crossover Trading Strategy')
    plt.grid()
    plt.legend()
    plt.savefig("EMA.png")
    plt.clf()






    return normalized_df_ema_20, normalized_df_ema_50


# MACD: Moving Average Convergence Divergence
# macd_signal > macd_raw, SELL
# macd_signal < macd_raw, BUY
def macd(sd, ed, symbol, plot=False):
    # look up history to calculate the ema for the 28 days
    # since the max ema windows size is 26, we can say 52 is safe
    delta = dt.timedelta(52)
    extedned_sd = sd - delta

    df_price = get_data([symbol], pd.date_range(extedned_sd, ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()

    ema_12 = df_price.ewm(span=12, adjust=False).mean()
    ema_26 = df_price.ewm(span=26, adjust=False).mean()
    macd_raw = ema_12 - ema_26
    macd_signal = macd_raw.ewm(span=9, adjust=False).mean()

    # remove history price
    df_price = df_price.truncate(before=sd)
    ema_12 = ema_12.truncate(before=sd)
    ema_26 = ema_26.truncate(before=sd)
    macd_raw = macd_raw.truncate(before=sd)
    macd_signal = macd_signal.truncate(before=sd)

    if plot == True:
        fig = plt.figure(figsize=(14, 8))
        plt.suptitle("MACD")
        plt.xlabel("Date")
        plt.ylabel('normalized price')

        # normalizing price and EMA
        normalized_ema_12 = ema_12[symbol] / ema_12[symbol][0]
        normalized_ema_26 = ema_26[symbol] / ema_26[symbol][0]
        normalized_df_price = df_price[symbol] / df_price[symbol][0]

        ax1 = plt.subplot(211)
        ax1.plot(normalized_ema_12, label="12 days EMA", color="orange")
        ax1.plot(normalized_ema_26, label="26 days EMA", color="red")
        ax1.plot(normalized_df_price, label="normalized price", color="blue")
        ax1.legend()
        plt.xlabel("Date")
        plt.ylabel('Normalized price')
        ax1.grid()

        ax2 = plt.subplot(212)
        ax2.plot(macd_raw, label="MACD", color="orange")
        ax2.plot(macd_signal, label="MACD Signal", color="red")
        ax2.grid()
        plt.xlabel("Date")
        ax2.legend()

        fig.autofmt_xdate()

        plt.savefig("part1_macd.png", bbox_inches='tight')
        # plt.show()
        plt.clf()

    return macd_raw, macd_signal


# TSI: True Strength Index
# tsi < 0, SELL
# tsi > 0, BUY
# add a cushion to be more condifent e.g. tsi < -0.05 and tsi > 0.05
def tsi(sd, ed, symbol, plot=False):
    # look up history to calculate the ema for the 24 days
    # since the max ema windows size is 20, we can say 50 is safe
    delta = dt.timedelta(50)
    extedned_sd = sd - delta

    df_price = get_data([symbol], pd.date_range(extedned_sd, ed))
    df_price = df_price[[symbol]]
    df_price = df_price.ffill().bfill()

    # calculate, smoothing and double smoothing price change
    diff = df_price - df_price.shift(1)
    ema_25 = diff.ewm(span=25, adjust=False).mean()
    ema_13 = ema_25.ewm(span=13, adjust=False).mean()

    # calculate, smoothing and double smoothing absolute price change
    abs_diff = abs(diff)
    abs_ema_25 = abs_diff.ewm(span=25, adjust=False).mean()
    abs_ema_13 = abs_ema_25.ewm(span=13, adjust=False).mean()

    df_tsi = ema_13 / abs_ema_13

    # remove history price
    df_tsi = df_tsi.truncate(before=sd)

    if plot == True:
        fig = plt.figure(figsize=(14, 8))
        plt.suptitle("TSI")
        plt.xlabel("Date")
        plt.ylabel('Ratio')

        # normalizing price and EMA
        normalized_df_price = df_price[symbol] / df_price[symbol][0]

        ax1 = plt.subplot(211)
        ax1.plot(normalized_df_price, label="normalized price", color="blue")
        ax1.legend()
        plt.xlabel("Date")
        plt.ylabel('Normalized price')
        ax1.grid()

        ax2 = plt.subplot(212)
        ax2.plot(df_tsi, label="TSI", color="orange")
        ax2.grid()
        plt.xlabel("Date")
        ax2.legend()

        fig.autofmt_xdate()

        plt.savefig("part1_tsi.png", bbox_inches='tight')
        # plt.show()
        plt.clf()

    return df_tsi


def report():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = 'JPM'

    # sd = dt.datetime(2008, 1, 1)
    # ed = dt.datetime(2008, 1, 30)
    # symbol = 'JPM'

    # sd = dt.datetime(2011, 8, 1)
    # ed = dt.datetime(2012, 9, 1)
    # symbol = 'NKE'

    # plot ema
    df_ema = ema(sd, ed, symbol)

    # plot macd
    df_macd = macd(sd, ed, symbol, plot=True)

    # plot tsi
    df_tsi = tsi(sd, ed, symbol, plot=True)


def author():
    return 'jlyu31'


if __name__ == "__main__":
    report()
