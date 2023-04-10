"""
Code implementing your indicators as functions that operate on DataFrames. There is no defined API for indicators.py, but
when it runs, the main method should generate the charts that will illustrate your indicators in the report.
"""

import numpy as np
import datetime as dt
import pandas as pd
from util import get_data
import matplotlib.pyplot as plt

def author():
  return 'pcometti3'


def get_bbp(rate, prices):
  SMA = prices.rolling(rate).mean()
  std = prices.rolling(rate).std()
  bollinger_up = SMA + std * 2  # Calculate top band
  bollinger_down = SMA - std * 2  # Calculate bottom band
  bbp = (prices - bollinger_down) / (bollinger_up - bollinger_down)
  return bbp


def get_CCI(symbol, sd, ed, rate, prices):
  dates = pd.date_range(sd, ed)
  high = get_data([symbol], dates, colname="High")[symbol]
  low = get_data([symbol], dates, colname="Low")[symbol]
  close = prices
  TP = (high + low + close) / 3
  SMA = TP.rolling(rate).mean()
  MD = TP.rolling(rate).apply(lambda x: pd.Series(x).mad(), raw=False)
  CCI = (TP - SMA) / (0.015 * MD)
  return CCI

"""
Indicator 5:  Momentum
"""
def get_momentum(prices_df, window=20):
    momentum = (prices_df / prices_df.shift(window)) - 1
    return momentum


def get_ROC(prices, rate):
  SMA = prices.rolling(rate).mean()
  close = prices
  ROC = ((close - close.shift(periods=rate-1))/close.shift(periods=rate-1))*100
  return ROC

def get_indicators(symbol="JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):
  sd1 = sd-dt.timedelta(days=40)
  dates = pd.date_range(sd1, ed)
  prices_all = get_data([symbol], dates)
  prices = prices_all[symbol]
  prices /= prices[0]

  rate = len(prices.loc[sd1:sd+dt.timedelta(days=1)])

  # %B
  bbp = get_bbp(rate, prices).loc[sd:]

  # CCI
  CCI = get_CCI(symbol, sd1, ed, rate, prices).loc[sd:]

  #ROC
  ROC = get_ROC(prices, rate).loc[sd:]

  return bbp, CCI, ROC

if __name__ == "__main__":
    get_indicators()