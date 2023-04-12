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
  return 'pcometti3' # replace tb34 with your Georgia Tech username.


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


def get_PPO(prices):
  EMA12 = prices.ewm(span=12, adjust=False).mean()
  EMA26 = prices.ewm(span=26, adjust=False).mean()
  PPO = ((EMA12 - EMA26) / EMA26) * 100
  EMA9 = PPO.ewm(span=9, adjust=False).mean()
  histo = PPO - EMA9
  idx = np.argwhere(np.diff(np.sign(PPO - EMA9))).flatten()
  green_idx = []
  red_idx = []
  for i in idx:
    if PPO[i]<EMA9[i]:
      green_idx = np.append(green_idx, i)
    else:
      red_idx = np.append(red_idx, i)

  red_idx = red_idx.astype(int)
  green_idx = green_idx.astype(int)

  return red_idx, green_idx


def get_ROC(prices, rate):
  SMA = prices.rolling(rate).mean()
  close = prices
  ROC = (prices / prices.shift(rate)) - 1

  return ROC


def get_RSI(prices, rate):
  close = prices
  change = close - close.shift(1)
  avg_gain = np.empty((close.shape[0]))
  avg_gain[:] = np.nan
  avg_loss = np.copy(avg_gain)
  prev_gain = (change[1:rate][change>0].sum())/(rate-1)
  prev_loss = ((change[1:rate][change<0].sum())/(rate-1))*(-1)


  for i in range(rate,close.shape[0]):
    if change[i] > 0:
      avg_gain[i] = (prev_gain*(rate-1)+change[i])/rate
      avg_loss[i] = (prev_loss*(rate-1))/rate
    else:
      avg_gain[i] = (prev_gain * (rate-1)) / rate
      avg_loss[i] = (prev_loss * (rate-1) + (change[i]*(-1))) / rate
    prev_gain = avg_gain[i]
    prev_loss = avg_loss[i]

  RS = avg_gain/avg_loss
  RSI = 100 - (100/(1+RS))
  RSI = pd.DataFrame(RSI, index=[prices.index.values])
  RSI = RSI[0]

  return RSI

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

  #PPO
  PPO = get_PPO(prices)

  #ROC
  ROC = get_ROC(prices, rate).loc[sd:]

  #RSI
  RSI = get_RSI(prices, rate=14).loc[sd:]

  return bbp, CCI, PPO, ROC, RSI

if __name__ == "__main__":
    get_indicators()