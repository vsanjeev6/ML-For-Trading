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
    df_price.dropna()
    #print(df_price)

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

"""
Indicator 2: Simple Moving Average and Price/SMA
"""
def sma(sd, ed, symbol, prices_df):
    print(prices_df)
    prices = prices_df[symbol]
    prices = prices / prices[0]

    df_indicators = pd.DataFrame(index=prices.index)
    # Remove the dates before the start_date
    df_indicators = df_indicators.truncate(before=sd)

    df_indicators['price'] = prices
    df_indicators['rolling mean'] = prices.rolling(window=20, center=False).mean()
    df_indicators['pricebySMA'] = df_indicators['price'] / df_indicators['rolling mean']

    # Plot
    fig = plt.subplots(figsize=(10, 5))
    plt.plot(prices, label="JPM price (normalized)", color="blue")
    plt.plot(df_indicators['rolling mean'], label="SMA", color="red")
    plt.xlabel('Date')
    plt.ylabel('Price (normalized)')
    plt.title('SMA')
    plt.xticks(rotation=10)
    plt.grid()
    plt.legend()
    plt.savefig("SMA.png")
    plt.clf()

    fig2 = plt.plot(figsize=(10, 5))
    plt.plot(df_indicators['pricebySMA'], label="P/SMA", color="blue")
    plt.xlabel('Date')
    plt.ylabel('Price (normalized)')
    plt.title('P/SMA')
    plt.grid()
    plt.legend()
    plt.xticks(rotation=10)
    plt.axhline(y=1.1, linestyle='--', color="green")
    plt.axhline(y=0.9, linestyle='--',color= "red")
    plt.savefig("Price_By_SMA.png")
    plt.clf()

"""
Indicator 3: Bollinger Band Percent
"""
def bb(sd, ed, symbol, prices_df):
    prices = prices_df[symbol]
    prices = prices / prices[0]

    df_indicators = pd.DataFrame(index=prices.index)
    # 2] bollinger bands
    rm = prices.rolling(window=10, center=False).mean()
    sd = prices.rolling(window=10, center=False).std()
    upband = rm + (2 * sd)
    dnband = rm - (2 * sd)
    df_indicators['upper band'] = upband
    df_indicators['lower band'] = dnband

    # BB value
    bb_value = (prices - rm) / (25 * sd)
    df_indicators['bb value'] = bb_value

    # 3] Commodity channel index
    cci = (prices - rm) / (2.5 * prices.std())
    df_indicators['Commodity Channel Index'] = cci

    # 4] Volatility
    volatility = prices.rolling(window=7, center=False).std()
    df_indicators['Volatility'] = volatility * 3.5

    # Plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    #plt.plot(prices, label="JPM price (normalized)", color="blue")
    #plt.plot(df_indicators['rolling mean'], label="SMA", color="red")
    plt.plot(df_indicators['upper band'], label="SMA", color="green")
    plt.plot(df_indicators['lower band'], label="SMA", color="purple")
    plt.plot(df_indicators['bb value'], label="SMA", color="orange")

    # Add BUY and SELL signals to the chart
    #ax.plot(df_price.loc[df_price.Position == 1.0].index, normalized_df_ema_20[df_price.Position == 1.0], '^',
     #       markersize=10, color='g', label='BUY')
    #ax.plot(df_price.loc[df_price.Position == -1.0].index, normalized_df_ema_20[df_price.Position == -1.0], 'v',
       #     markersize=10, color='r', label='SELL')

    # Add chart labels and legend
    plt.xlabel('Date')
    plt.xticks(rotation=30)
    plt.ylabel('Price (normalized)')
    plt.title('SMA Crossover Trading Strategy')
    plt.grid()
    plt.legend()
    plt.savefig("BB.png")
    plt.clf()

# MACD: Moving Average Convergence Divergence
def macd(sd, ed, symbol):
    # look up history to calculate the ema for the 28 days
    # since the max ema windows size is 26, we can say 52 is safe
    delta = dt.timedelta(52)

    df_price = get_data([symbol], pd.date_range((sd - delta), ed))
    #print(df_price)

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
    histogram = macd_raw - macd_signal

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


def report():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = 'JPM'

    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    prices_df = prices_df.ffill().bfill()

    # plot ema
    df_ema = ema(sd, ed, symbol)

    # SMA
    sma(sd, ed, symbol, prices_df)
    bb(sd, ed, symbol, prices_df)

    # Bollinger
    #sma(sd, ed, symbol, prices_df)[['upper band', 'lower band', 'bb value', 'rolling mean']].plot(figsize=(20, 7))
    # CCI
    #sma(sd, ed, symbol, prices_df)[['Commodity Channel Index']].plot(figsize=(20, 7))

    # Volatility
    #sma(sd, ed, symbol, prices_df)[['Volatility']].plot(figsize=(20, 7))

   # plt.axhline(y=0, linestyle=':')
   # plt.axhline(y=0.04, linestyle='--')
   # plt.axhline(y=-0.04, linestyle='--')


def author():
    return 'vsanjeev6'


if __name__ == "__main__":
    report()
