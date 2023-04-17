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
import marketsimcode as mktsim
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

    learner1 = StrategyLearner(verbose=False, impact=0.0, commission=0.0)
    learner1.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    df_trades1 = learner1.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    portvals1 = mktsim.compute_portvals(df_trades1, start_val=100000, commission=0.0, impact=0.0)
    portvals1 /= portvals1.values[0]
    print_stats(portvals1)

    learner2 = StrategyLearner(verbose=False, impact=0.005, commission=0.0)
    learner2.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    df_trades2 = learner2.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    portvals2 = mktsim.compute_portvals(df_trades2, start_val=100000, commission=0.0, impact=0.005)
    portvals2 /= portvals2.values[0]
    print_stats(portvals2)

    learner3 = StrategyLearner(verbose=False, impact=0.01, commission=0.0)
    learner3.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    df_trades3 = learner3.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    portvals3 = mktsim.compute_portvals(df_trades3, start_val=100000, commission=0.0, impact=0.01)
    portvals3 /= portvals3.values[0]
    print_stats(portvals3)

    """
    Plot Graphs
    """
    plt.title('Effect of Impact on In-Sample Trading Behaviour')
    plt.xticks(rotation=30)
    plt.plot(portvals1, label="Impact = 0.0", color="red")
    plt.plot(portvals2, label="Impact = 0.005", color="purple")
    plt.plot(portvals3, label="Impact = 0.01", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.grid()
    plt.legend()
    plt.savefig("images/Exp2", dpi=300, bbox_inches='tight')
    plt.clf()

def print_stats(portvals):
  portfolio_value = portvals['value']

  # Cumulative Return
  cr = portfolio_value[-1] / portfolio_value[0] - 1

  # Daily Return
  dr = (portfolio_value / portfolio_value.shift(1) - 1).iloc[1:]

  # Stdev of daily returns
  sddr = portfolio_value.std(ddof=1)

  # Mean of daily returns
  adr = portfolio_value.mean()

  # Sharpe Ratio
  sr = np.sqrt(252) * (adr / sddr)

  """
  print("~~~~~~~~~~Experiment 2~~~~~~~~~~")
  print("Cumulative Return: " + str(cr))
  print("Stdev of daily returns: " + str(sddr))
  print("Mean of daily returns: " + str(adr))
  print("Sharpe Ratio: " + str(sr))
  """

if __name__ == "__main__":
    pass
    #print("Experiment 2")