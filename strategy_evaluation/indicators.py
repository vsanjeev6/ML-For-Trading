"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718
"""
import datetime as dt
import pandas as pd
from util import get_data

def author():
  return 'vsanjeev6'

"""
Indicator 1: Bollinger Band Percent
"""
def get_BBP(window, prices):
  prices = prices.ffill().bfill()
  rm = prices.rolling(window=window, center=False).mean()
  sd = prices.rolling(window=window, center=False).std()
  upband = rm + (2 * sd)
  dnband = rm - (2 * sd)
  BBP = (prices - dnband) / (upband - dnband)
  return BBP

"""
Indicator 2:  Commodity Channel Index
"""
def get_CCI(symbol, sd, ed, window, prices):
  dates = pd.date_range(sd, ed)

  high = get_data([symbol], dates, colname="High")[symbol]
  low = get_data([symbol], dates, colname="Low")[symbol]
  close = get_data([symbol], dates, colname="Close")[symbol]
  adj_close = prices

  adjustment_factor = adj_close / close
  high = high * adjustment_factor
  low = low * adjustment_factor

  typical_price = (high + low + adj_close) / 3
  mean_deviation = abs(typical_price - typical_price.rolling(window).mean()).mean()
  CCI = (typical_price - typical_price.rolling(window).mean()) / (0.015 * mean_deviation)
  return CCI

"""
Indicator 3:  Momentum
"""
def get_MOM(prices, window):
  MOM = (prices / prices.shift(window)) - 1
  return MOM

def get_indicators(symbol="JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):
  sd = sd
  ed = ed
  symbol = symbol

  dates = pd.date_range(sd, ed)
  prices_all = get_data([symbol], dates)
  prices = prices_all[symbol]
  prices = prices.ffill().bfill()
  prices /= prices[0]
  window = 20

  # BBP
  BBP = get_BBP(window, prices).loc[sd:]

  # CCI
  CCI = get_CCI(symbol, sd, ed, window, prices).loc[sd:]

  # Momentum
  MOM = get_MOM(prices, window).loc[sd:]

  return BBP, CCI, MOM

if __name__ == "__main__":
  # get_indicators()
  pass
