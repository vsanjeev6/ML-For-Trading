"""
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
    print(prices)
    BBP = ind.get_BBP(lookback, prices)
    CCI = ind.get_CCI(symbol, sd, ed, lookback, prices)
    ROC = ind.get_MOM(prices, lookback)

    holding = 0
    delta = 1000
    short = []
    long = []

    for i in range(len(prices)):
      if ((BBP[i] >= 0.75 and CCI[i] >= 100) or ROC[i] >= 0.2) and holding >= 0:
        #sell
        if holding==0:
          df_trades.loc[prices.index[i]] = -delta
        elif holding==1000:
          df_trades.loc[prices.index[i]] = -delta*2
        short.append(prices.index[i])
        holding += df_trades.loc[prices.index[i]].values[0]

      elif ((BBP[i] <= 0.25 and CCI[i] <= -100) or ROC[i] <= -0.2) and holding <= 0:
        #buy
        if holding==0:
          df_trades.loc[prices.index[i]] = delta
        elif holding==-1000:
          df_trades.loc[prices.index[i]] = delta*2
        long.append(prices.index[i])
        holding += df_trades.loc[prices.index[i]].values[0]


    return df_trades, short, long


def test_code(symbol="JPM", sv = 100000):
  sd = dt.datetime(2008, 1, 1)
  ed = dt.datetime(2009, 12, 31)
  ms = ManualStrategy()
  df_trades, short, long = ms.testPolicy(symbol, sd, ed, sv)
  df_benchmark = pd.DataFrame(0, index=df_trades.index, columns=[symbol])
  df_benchmark.loc[df_benchmark.index[0]] = 1000
  df_benchmark.loc[df_benchmark.index[len(df_benchmark.index)-1]] = -1000

  portvals = mktsim.compute_portvals(df_trades, sv,commission=9.95, impact=0.005)
  benchmark = mktsim.compute_portvals(df_benchmark, sv, commission=9.95, impact=0.005)

  portvals /= portvals.values[0]
  benchmark /= benchmark.values[0]

  compute_stats(portvals, benchmark, title="IN-SAMPLE")

  ymin=min([portvals.min().values[0], benchmark.min().values[0]])
  ymax=max([portvals.max().values[0], benchmark.max().values[0]])

  plt.title('Manual Strategy vs. JPM Benchmark for in-sample period')
  plt.xticks(rotation=45)
  plt.plot(portvals, label="Manual Strategy", color="red")
  plt.plot(benchmark, label="JPM Benchmark", color="purple")
  plt.vlines(x=short, ymin=ymin, ymax=ymax, color='black', linewidth=1, label='short entry')
  plt.vlines(x=long, ymin=ymin, ymax=ymax, color='b', linewidth=1, label='long entry')
  plt.grid()
  plt.legend()
  plt.savefig("images/ManualStrategy1", dpi=300, bbox_inches='tight')
  plt.clf()

  sd = dt.datetime(2010, 1, 1)
  ed = dt.datetime(2011, 12, 31)
  df_trades, short, long = ms.testPolicy(symbol, sd, ed, sv)
  df_benchmark = pd.DataFrame(0, index=df_trades.index, columns=[symbol])
  df_benchmark.loc[df_benchmark.index[0]] = 1000
  df_benchmark.loc[df_benchmark.index[len(df_benchmark.index) - 1]] = -1000

  portvals = mktsim.compute_portvals(df_trades, sv,commission=9.95, impact=0.005)
  benchmark = mktsim.compute_portvals(df_benchmark, sv,commission=9.95, impact=0.005)

  portvals /= portvals.values[0]
  benchmark /= benchmark.values[0]

  compute_stats(portvals, benchmark, title="OUT-SAMPLE")

  ymin = min([portvals.min().values[0], benchmark.min().values[0]])
  ymax = max([portvals.max().values[0], benchmark.max().values[0]])

  plt.title('Manual Strategy vs. JPM Benchmark for out-samples period')
  plt.xticks(rotation=45)
  plt.plot(portvals, label="Manual Strategy", color="red")
  plt.plot(benchmark, label="JPM Benchmark", color="purple")
  plt.vlines(x=short, ymin=ymin, ymax=ymax, color='black', linewidth=1, label='short entry')
  plt.vlines(x=long, ymin=ymin, ymax=ymax, color='b', linewidth=1, label='long entry')
  plt.grid()
  plt.legend()
  plt.savefig("images/ManualStrategy2", dpi=300, bbox_inches='tight')
  plt.clf()

def compute_stats(portvals, benchmark, title):
  d_returns1 = portvals.copy()
  for i in range(1, len(d_returns1)):
    d_returns1.loc[d_returns1.index[i]] = (portvals.values[i - 1][0] - portvals.values[i][0]) / portvals.values[i - 1][0]
  d_returns1 = d_returns1[1:]

  # Below are desired output values

  # Cumulative return (final - initial) - 1
  cum_ret1 = (portvals.values[-1][0] / portvals.values[0][0]) - 1
  # Average daily return
  avg_daily_ret1 = d_returns1.mean()
  # Standard deviation of daily return
  std_daily_ret1 = d_returns1.std()

  d_returns2 = benchmark.copy()
  for i in range(1, len(d_returns2)):
    d_returns2.loc[d_returns2.index[i]] = (benchmark.values[i - 1][0] - benchmark.values[i][0]) / benchmark.values[i - 1][0]
  d_returns2 = d_returns2[1:]

  # Cumulative return (final - initial) - 1
  cum_ret2 = (benchmark.values[-1][0] / benchmark.values[0][0]) - 1
  # Average daily return
  avg_daily_ret2 = d_returns2.mean()
  # Standard deviation of daily return
  std_daily_ret2 = d_returns2.std()

  print(title)
  print()
  print("Cumulative Return of Portfolio: %.6f" % cum_ret1)
  print("Cumulative Return of Benchmark: %.6f" % cum_ret2)
  print()
  print("Standard Deviation of Portfolio: %.6f" % std_daily_ret1)
  print("Standard Deviation of Benchmark: %.6f" % std_daily_ret2)
  print()
  print("Average Daily Return of Portfolio: %.6f" % -avg_daily_ret1)
  print("Average Daily Return of Benchmark: %.6f" % -avg_daily_ret2)
  print()

if __name__ == "__main__":
  print("Manual Strategy")
