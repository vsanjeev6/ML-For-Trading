import datetime as dt
import pandas as pd
from StrategyLearner import StrategyLearner
import marketsimcode as ms
import matplotlib.pyplot as plt

def author():
    return 'vsanjeev6'

def test_code():
    sl = StrategyLearner(verbose = False, impact = 0)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    df_es1 = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))

    sl = StrategyLearner(verbose=False, impact=0.005)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    df_es2 = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))

    sl = StrategyLearner(verbose=False, impact=0.01)
    sl.add_evidence(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000)
    df_es3 = sl.testPolicy(symbol='JPM', sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31))

    es1 = ms.compute_portvals(df_es1)
    es2 = ms.compute_portvals(df_es2)
    es3 = ms.compute_portvals(df_es3)

    es1 /= es1.values[0]
    es2 /= es2.values[0]
    es3 /= es3.values[0]


    pd.plotting.register_matplotlib_converters()
    plt.title('How impact affects in-sample results')
    plt.xticks(rotation=45)
    plt.plot(es1, label="impact = 0.0", color="red")
    plt.plot(es2, label="impact = 0.005", color="purple")
    plt.plot(es3, label="impact = 0.01", color="blue")
    plt.grid()
    plt.legend()
    plt.savefig("images/exp2", dpi=300, bbox_inches='tight')
    plt.clf()

if __name__ == "__main__":
    print("Experiment 2")