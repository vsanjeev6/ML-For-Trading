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
def sma(sd, ed, symbol, prices_df,window):
    prices = prices_df[symbol]
    prices = prices / prices[0]

    df_indicators = pd.DataFrame(index=prices.index)
    # Remove the dates before the start_date
    df_indicators = df_indicators.truncate(before=sd)

    df_indicators['price'] = prices
    df_indicators['rolling mean'] = prices.rolling(window=window, center=False).mean()
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
def bb(sd, ed, symbol, prices_df,window):
    prices = prices_df[symbol]
    prices = prices / prices[0]
    # Empty Dataframe
    df_indicators = pd.DataFrame(index=prices.index)

    rm = prices.rolling(window=window, center=False).mean()
    sd = prices.rolling(window=window, center=False).std()
    upband = rm + (2 * sd)
    dnband = rm - (2 * sd)
    df_indicators['upper band'] = upband
    df_indicators['lower band'] = dnband
    df_indicators['rolling mean'] = prices.rolling(window=window, center=False).mean()

    # BBP
    df_indicators['bbp'] = (prices - dnband) / (upband - dnband)

    df_indicators['Position'] = None
    position = None

    # Loop through the prices
    for i in range(window, len(prices)):
        # If the price crosses from outside of the lower band to inside, buy
        if prices[i] > dnband[i] and prices[i-1] <= dnband[i-1]:
            if position != 'BUY':
                df_indicators.loc[prices.index[i], 'Position'] = 'BUY'
                position = 'BUY'
        # If the price crosses from outside of the upper band to inside, sell
        elif prices[i] < upband[i] and prices[i-1] >= upband[i-1]:
            if position != 'SELL':
                df_indicators.loc[prices.index[i], 'Position'] = 'SELL'
                position = 'SELL'

    # Plot
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1)
    plt.plot(prices, label="JPM price (normalized)", color="grey")
    plt.plot(df_indicators['rolling mean'], label="SMA", color="red")
    plt.plot(df_indicators['upper band'], label="Upper Band", color="green")
    plt.plot(df_indicators['lower band'], label="Lower Band", color="purple")


    # Add BUY and SELL signals to the chart
    ax.plot(df_indicators[df_indicators['Position'] == 'BUY'].index, prices[df_indicators['Position'] == 'BUY'], '^', markersize=8, color='g', label='BUY')
    ax.plot(df_indicators[df_indicators['Position'] == 'SELL'].index, prices[df_indicators['Position'] == 'SELL'], 'v', markersize=8, color='r', label='SELL')

    # Add chart labels and legend
    plt.xlabel('Date')
    plt.xticks(rotation=10)
    plt.ylabel('Price (normalized)')
    plt.title('Bollinger Band Crossover Trading Strategy')
    plt.grid()
    plt.legend()
    plt.savefig("Bollinger_Band.png")
    plt.clf()

    fig2 = plt.figure(figsize=(10, 5))
    plt.plot(df_indicators['bbp'], label="BB%", color="blue")
    # Add chart labels and legend
    plt.xlabel('Date')
    plt.xticks(rotation=10)
    plt.ylabel('Price (normalized)')
    plt.title('Bollinger Band Percent')
    plt.grid()
    plt.legend()
    plt.savefig("Bollinger_Band_Percent.png")
    plt.clf()

"""
Indicator 4:  Commodity Channel Index
"""
def cci(sd, ed, symbol, prices_df,window=20):

    dates = pd.date_range(sd, ed)

    adjusted_close = get_data([symbol], dates, colname="Adj Close")
    adjusted_close = adjusted_close.rename(columns={symbol: "Adj Close"})

    Close = get_data([symbol], dates, addSPY=False, colname="Close")
    Close = Close.rename(columns={symbol: "Close"})

    closes_df = adjusted_close.join(Close)
    closes_df['adjustment_factor'] = closes_df['Adj Close']/closes_df['Close']
    #print("Closes DF", closes_df)

    High = get_data([symbol], dates, addSPY=False, colname="High")
    High = High.rename(columns={symbol: "High"})

    Low = get_data([symbol], dates, addSPY=False, colname="Low")
    Low = Low.rename(columns={symbol: "Low"})

    prices_df_tmp = closes_df.join(High)
    prices_df = prices_df_tmp.join(Low)
    #print("Before Adj\n", prices_df)
    prices_df['High'] = prices_df['High'] * prices_df['adjustment_factor']
    prices_df['Low'] = prices_df['Low'] * prices_df['adjustment_factor']
    prices_df = prices_df.ffill().bfill()
    print("Final Prices\n", prices_df)

    typical_price = (prices_df['High'] + prices_df['Low'] + prices_df['Adj Close']) / 3
    mean_deviation = abs(typical_price - typical_price.rolling(window).mean()).mean()
    cci = (typical_price - typical_price.rolling(window).mean()) / (0.015 * mean_deviation)

    # Plot the CCI values
    fig = plt.plot(figsize=(10, 5))
    plt.plot(cci, label="CCI", color="blue")
    plt.xlabel('Date')
    plt.ylabel('CCI')
    plt.title('Commodity Channel Index')
    plt.grid()
    plt.legend()
    plt.xticks(rotation=10)
    plt.axhline(y=100, color='r', linestyle='-')
    plt.axhline(y=-100, color='g', linestyle='-')
    plt.savefig("CCI.png")
    plt.clf()


def momentum(sd, ed, symbol, prices_df, window=20):
    prices = prices_df[symbol]
    prices = prices / prices[0]
    # Empty Dataframe
    df_indicators = pd.DataFrame(index=prices.index)

    momentum = (prices / prices.shift(window)) - 1

    df_indicators['Momentum'] = momentum

    fig = plt.figure(figsize=(10, 5))
    plt.plot(df_indicators['Momentum'], label="Momentum", color="blue")
    plt.xlabel('Date')
    plt.xticks(rotation=10)
    plt.ylabel('Price (normalized)')
    plt.title('Momentum')
    plt.axhline(y=0, color='grey', linestyle='-')
    plt.axhline(y=0.05, color='green', linestyle='-')
    plt.axhline(y=-0.05, color='red', linestyle='-')
    plt.grid()
    plt.legend()
    plt.savefig("Momentum.png")
    plt.clf()


def report():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbol = 'JPM'

    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    prices_df = prices_df.ffill().bfill()

    #df_ema = ema(sd, ed, symbol)
    #sma(sd, ed, symbol, prices_df,window=20)
    #bb(sd, ed, symbol, prices_df,window=20)
    cci(sd, ed, symbol, prices_df, window=20)
    momentum(sd, ed, symbol, prices_df, window=20)


def author():
    return 'vsanjeev6'

if __name__ == "__main__":
    report()
