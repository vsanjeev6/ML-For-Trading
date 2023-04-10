import datetime as dt
import pandas as pd
import time
from StrategyLearner import StrategyLearner
import ManualStrategy
import marketsimcode as ms
import matplotlib.pyplot as plt


def author():
    return "pcometti3"  # replace tb34 with your Georgia Tech username

def test_code():
    sl = StrategyLearner(verbose = False, impact = 0.005, commission=0.0)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))
    df_out_trades = sl.testPolicy(symbol='JPM', sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31))
    df_in_trades = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))

    df_trades, _, _ = ManualStrategy.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),sv=100000)
    df_benchmark = pd.DataFrame(0, index=df_trades.index, columns=["JPM"])
    df_benchmark.loc[df_benchmark.index[0]] = 1000
    df_benchmark.loc[df_benchmark.index[len(df_benchmark.index) - 1]] = -1000

    in_sample = ms.compute_portvals(df_in_trades)
    out_sample = ms.compute_portvals(df_out_trades)
    portvals = ms.compute_portvals(df_trades, start_val=100000)
    benchmark = ms.compute_portvals(df_benchmark, start_val=100000)


    portvals /= portvals.values[0]
    benchmark /= benchmark.values[0]
    in_sample /= in_sample.values[0]
    out_sample /= out_sample.values[0]


    pd.plotting.register_matplotlib_converters()
    plt.title('Strategy Learner vs. Manual Strategy for in-sample trading JPM')
    plt.xticks(rotation=45)
    plt.plot(portvals, label="Manual Strategy", color="red")
    plt.plot(benchmark, label="JPM Benchmark", color="purple")
    plt.plot(in_sample, label="Strategy Learner", color="blue")
    plt.grid()
    plt.legend()
    plt.savefig("images/exp1_a", dpi=300, bbox_inches='tight')
    plt.clf()

    df_trades, _, _ = ManualStrategy.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000)
    df_benchmark = pd.DataFrame(0, index=df_trades.index, columns=["JPM"])
    df_benchmark.loc[df_benchmark.index[0]] = 1000
    df_benchmark.loc[df_benchmark.index[len(df_benchmark.index) - 1]] = -1000

    portvals = ms.compute_portvals(df_trades, start_val=100000)
    benchmark = ms.compute_portvals(df_benchmark, start_val=100000)

    portvals /= portvals.values[0]
    benchmark /= benchmark.values[0]

    pd.plotting.register_matplotlib_converters()
    plt.title('Strategy Learner vs. Manual Strategy for out-sample trading JPM')
    plt.xticks(rotation=45)
    plt.plot(portvals, label="Manual Strategy", color="red")
    plt.plot(benchmark, label="JPM Benchmark", color="purple")
    plt.plot(out_sample, label="Strategy Learner", color="blue")
    plt.grid()
    plt.legend()
    plt.savefig("images/exp1_b", dpi=300, bbox_inches='tight')
    plt.clf()
if __name__ == "__main__":
    print("Experiment 1")