"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718

Code implementing Experiment 1
"""

import datetime as dt
import pandas as pd
from StrategyLearner import StrategyLearner
from ManualStrategy import ManualStrategy
import marketsimcode as mktsim
import matplotlib.pyplot as plt
from util import get_data

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
    # Create objects of Manual Strategy and Strategy Learner
    ms = ManualStrategy()
    sl = StrategyLearner(verbose = False, impact = 0.005, commission=9.95)

    # Train Strategy Learner on In-Sample Data
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv = 100000)
    # Query Strategy Learner on In-Sample Data
    in_sample_trades = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    # Query Strategy Learner on Out-Sample Data
    out_sample_trades = sl.testPolicy(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv = 100000)

    """
    In-Sample
    """
    # Query Manual Strategy on In-Sample Data
    df_trades, _, _ = ms.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    benchmark = get_benchmark(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    in_sample_portval = mktsim.compute_portvals(in_sample_trades, start_val=100000, commission=9.95, impact=0.005)
    # Portfolio Value for Manual Strategy trades
    portvals = mktsim.compute_portvals(df_trades, start_val=100000, commission=9.95, impact=0.005)
    plotting_utility_function(benchmark, portvals, in_sample_portval, "Manual Strategy Vs. Strategy Learner Vs. Benchmark (In-Sample JPM)", "Date",
                              "Normalized Portfolio Value", "images/Exp1_In_Sample.png")

    """
    Out-Sample
    """
    # Query Manual Strategy on Out-Sample Data
    df_trades, _, _ = ms.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    benchmark = get_benchmark(sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    out_sample_portval = mktsim.compute_portvals(out_sample_trades, start_val=100000, commission=9.95, impact=0.005)
    # Portfolio Value for Manual Strategy trades
    portvals = mktsim.compute_portvals(df_trades, start_val=100000, commission=9.95, impact=0.005)
    plotting_utility_function(benchmark, portvals, out_sample_portval, "Manual Strategy Vs. Strategy Learner Vs. Benchmark (Out-of-Sample JPM)", "Date",
                              "Normalized Portfolio Value", "images/Exp1_Out_Sample.png")

"""
Benchmark is the performance of a portfolio starting with $100,000 cash, 
investing in 1000 shares of JPM on the first trading day and
holding that position
"""
def get_benchmark(sd, ed, sv):
    df_trades = get_data(['SPY'], pd.date_range(sd, ed))
    df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
    df_trades[:] = 0
    df_trades.loc[df_trades.index[0]] = 1000
    portvals = mktsim.compute_portvals(df_trades, sv, commission=9.95, impact=0.005)
    return portvals

def plotting_utility_function(benchmark, portvals, in_or_out_sample, title,xlabel,ylabel,fig_name):
    # Normalize values first
    portvals /= portvals.values[0]
    benchmark /= benchmark.values[0]
    in_or_out_sample /= in_or_out_sample.values[0]

    plt.title(title)
    plt.xticks(rotation=30)
    plt.plot(portvals, label="Manual Strategy", color="red")
    plt.plot(benchmark, label="JPM Benchmark", color="purple")
    plt.plot(in_or_out_sample, label="Strategy Learner", color="blue")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend()
    plt.savefig(fig_name, dpi=300, bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
    pass
    #print("Experiment 1")