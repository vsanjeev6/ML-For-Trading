"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718

Code implementing Experiment 2
"""

import datetime as dt
import pandas as pd
import numpy as np
from StrategyLearner import StrategyLearner
import marketsimcode as ms
import matplotlib.pyplot as plt

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

def test_code():
    sl = StrategyLearner(verbose=False, impact=0.0, commission=0.0)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    df_es1 = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

    sl = StrategyLearner(verbose=False, impact=0.005, commission=0.0)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    df_es2 = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

    sl = StrategyLearner(verbose=False, impact=0.1, commission=0.0)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    df_es3 = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)

    es1 = ms.compute_portvals(df_es1)
    es2 = ms.compute_portvals(df_es2)
    es3 = ms.compute_portvals(df_es3)

    es1 /= es1.values[0]
    es2 /= es2.values[0]
    es3 /= es3.values[0]

    plt.title('Effect of Impact on In-Sample Trading Behaviour')
    plt.xticks(rotation=30)
    plt.plot(es1, label="Impact = 0.0", color="red")
    plt.plot(es2, label="Impact = 0.005", color="purple")
    plt.plot(es3, label="Impact = 0.1", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.grid()
    plt.legend()
    plt.savefig("images/Exp2", dpi=300, bbox_inches='tight')
    plt.clf()

def print_stats(portvals, benchmark):
  benchmark, theoretical = benchmark['value'], portvals['value']

  # Cumulative Return
  cr_ben = benchmark[-1] / benchmark[0] - 1
  cr_the = theoretical[-1] / theoretical[0] - 1

  # Daily Return
  dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
  dr_the = (theoretical / theoretical.shift(1) - 1).iloc[1:]

  # Stdev of daily returns
  sddr_ben = dr_ben.std(ddof=1)
  sddr_the = dr_the.std(ddof=1)

  # Mean of daily returns
  adr_ben = dr_ben.mean()
  adr_the = dr_the.mean()

  # Sharpe Ratio
  sr_ben = np.sqrt(252) * (adr_ben / sddr_ben)
  sr_the = np.sqrt(252) * (adr_the / sddr_the)

  print("~~~~~~~~~~Experiment 2~~~~~~~~~~")
  print("======Manual Strategy======")
  print("Cumulative Return: " + str(cr_the))
  print("Stdev of daily returns: " + str(sddr_the))
  print("Mean of daily returns: " + str(adr_the))
  print("Sharpe Ratio:" + str(sr_the))
  print("")
  print("======Benchmark======")
  print("Cumulative Return: " + str(cr_ben))
  print("Stdev of daily returns: " + str(sddr_ben))
  print("Mean of daily returns: " + str(adr_ben))
  print("Sharpe Ratio:" + str(sr_ben))

if __name__ == "__main__":
    print("Experiment 2")