"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718

Code implementing the ManualStrategy object
"""

import datetime as dt
import pandas as pd
from util import get_data
import marketsimcode as mktsim
import matplotlib.pyplot as plt
import indicators as ind

"""
Register datetime converter
To avoid warings: 
FutureWarning: Using an implicitly registered datetime converter for a matplotlib plotting method. 
The converter was registered by pandas on import.
Future versions of pandas will require you to explicitly register matplotlib converters.
"""
pd.plotting.register_matplotlib_converters()

def author():
  return 'vsanjeev6'

class ManualStrategy:
  def testPolicy(self, symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
    dates = pd.date_range(sd, ed)
    prices_all = get_data([symbol], dates)
    prices = prices_all[symbol]
    lookback = 20
    df_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])

    # Get the indicator values
    BBP = ind.get_BBP(lookback, prices)
    CCI = ind.get_CCI(symbol, sd, ed, lookback, prices)
    MOM = ind.get_MOM(prices, lookback)

    holding = 0
    trade = 1000
    short = []
    long = []
    """
    Simple Logic for Manual Strategy
    """
    for i in range(len(prices)):
      # SELL/SHORT
      if (BBP[i] >= 0.8 or CCI[i] >= 100 and MOM[i] <= -0.05) and holding >= 0:
        if holding==0:
          df_trades.loc[prices.index[i]] = -trade
        elif holding==1000:
          df_trades.loc[prices.index[i]] = -trade*2
        short.append(prices.index[i])
        holding += df_trades.loc[prices.index[i]].values[0]
      # BUY/LONG
      elif (BBP[i] <= 0.2 or CCI[i] <= -100 and MOM[i] >= 0.05) and holding <= 0:
        if holding==0:
          df_trades.loc[prices.index[i]] = trade
        elif holding==-1000:
          df_trades.loc[prices.index[i]] = trade*2
        long.append(prices.index[i])
        holding += df_trades.loc[prices.index[i]].values[0]
    return df_trades, short, long


def test_code(symbol="JPM", sv = 100000):
  ms = ManualStrategy()

  """
  In-Sample
  """
  sd = dt.datetime(2008, 1, 1)
  ed = dt.datetime(2009, 12, 31)
  df_trades, short, long = ms.testPolicy(symbol, sd, ed, sv)

  portvals = mktsim.compute_portvals(df_trades, sv,commission=9.95, impact=0.005)
  benchmark = get_benchmark(sd, ed, sv)

  portvals /= portvals.values[0]
  benchmark /= benchmark.values[0]

  print_stats(portvals, benchmark)
  plotting_utility_function(benchmark, portvals, short, long,"Manual Strategy Vs. JPM Benchmark for In-Sample Period", "Date",
                            "Normalized Portfolio Value", "images/ManualStrategy1.png")

  """
  Out-Sample
  """
  sd = dt.datetime(2010, 1, 1)
  ed = dt.datetime(2011, 12, 31)
  df_trades, short, long = ms.testPolicy(symbol, sd, ed, sv)

  portvals = mktsim.compute_portvals(df_trades, sv,commission=9.95, impact=0.005)
  benchmark = get_benchmark(sd, ed, sv)

  portvals /= portvals.values[0]
  benchmark /= benchmark.values[0]

  print_stats(portvals, benchmark)
  plotting_utility_function(benchmark, portvals, short, long,"Manual Strategy Vs. JPM Benchmark for Out-Sample Period", "Date",
                            "Normalized Portfolio Value", "images/ManualStrategy2.png")


def get_benchmark(sd, ed, sv):
  df_trades = get_data(['SPY'], pd.date_range(sd, ed))
  df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
  df_trades[:] = 0
  df_trades.loc[df_trades.index[0]] = 1000
  portvals = mktsim.compute_portvals(df_trades, sv, commission=9.95, impact=0.005)
  return portvals


def print_stats(portvals, benchmark):
  benchmark, theoretical = benchmark['value'], portvals['value']

  # Cumulative Return
  cr_ben = benchmark[-1] / benchmark[0] - 1
  cr_the = theoretical[-1] / theoretical[0] - 1

  # Daily Return
  dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
  dr_the = (theoretical / theoretical.shift(1) - 1).iloc[1:]

  # Stdev of daily returns
  sddr_ben = dr_ben.std()
  sddr_the = dr_the.std()

  # Mean of daily returns
  adr_ben = dr_ben.mean()
  adr_the = dr_the.mean()

  print("======Manual Strategy======")
  print("Cumulative Return: " + str(cr_the))
  print("Stdev of daily returns: " + str(sddr_the))
  print("Mean of daily returns: " + str(adr_the))
  print("")
  print("======Benchmark======")
  print("Cumulative Return: " + str(cr_ben))
  print("Stdev of daily returns: " + str(sddr_ben))
  print("Mean of daily returns: " + str(adr_ben))

def plotting_utility_function(benchmark, portvals, short, long,title,xlabel,ylabel,fig_name):

  # Ensures the verical lines drawn fall within the range of y-values of the graph and does not extend infinitely
  ymin=min([portvals.min().values[0], benchmark.min().values[0]])
  ymax=max([portvals.max().values[0], benchmark.max().values[0]])

  plt.title(title)
  plt.xticks(rotation=30)
  plt.plot(portvals, label="Manual Strategy", color="red")
  plt.plot(benchmark, label="JPM Benchmark", color="purple")
  plt.vlines(x=short, ymin=ymin, ymax=ymax, color='black', linewidth=1, label='Short')
  plt.vlines(x=long, ymin=ymin, ymax=ymax, color='blue', linewidth=1, label='Long')
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.grid()
  plt.legend()
  plt.savefig(fig_name, dpi=300, bbox_inches='tight')
  plt.clf()

if __name__ == "__main__":
  pass
  #print("Manual Strategy")
