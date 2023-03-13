"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718
"""
from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt

"""
Register datetime converter
To avoid warings: 
FutureWarning: Using an implicitly registered datetime converter for a matplotlib plotting method. 
The converter was registered by pandas on import.
Future versions of pandas will require you to explicitly register matplotlib converters.
"""
pd.plotting.register_matplotlib_converters()

def testPolicy(symbol, sd, ed, sv):
    symbol = symbol[0]
    df = get_data([symbol], pd.date_range(sd, ed))
    price_df = df[[symbol]]
    price_df = price_df.ffill().bfill()

    df_trades = df[['SPY']]
    df_trades = df_trades.rename(columns={'SPY': symbol}).astype({symbol: 'int32'})
    df_trades[:] = 0
    dates = df_trades.index
    current_position = 0

    # making trades
    for i in range(len(dates) - 1):
        if price_df.loc[dates[i + 1]].loc[symbol] > price_df.loc[dates[i]].loc[symbol]:
            action = 1000 - current_position
        else:
            action = -1000 - current_position
        df_trades.loc[dates[i]].loc[symbol] = action
        current_position += action
    #print(df_trades)
    return df_trades

def author():
    return 'vsanjeev6'

def get_benchmark(sd, ed, sv):
    df_trades = get_data(['SPY'], pd.date_range(sd, ed))
    df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
    df_trades[:] = 0
    df_trades.loc[df_trades.index[0]] = 1000
    portvals = compute_portvals(df_trades, sv, commission=0.00, impact=0.00)
    return portvals

def print_stats(benchmark, theoretical):
    benchmark, theoretical = benchmark['value'], theoretical['value']

    # Cumulative Return
    cr_ben = benchmark[-1] / benchmark[0] - 1
    cr_the = theoretical[-1] / theoretical[0] - 1

    # daily return in percentage
    dr_ben = (benchmark / benchmark.shift(1) - 1).iloc[1:]
    dr_the = (theoretical / theoretical.shift(1) - 1).iloc[1:]

    # [Stdev of daily returns]
    sddr_ben = dr_ben.std()
    sddr_the = dr_the.std()

    # [Mean of daily returns]
    adr_ben = dr_ben.mean()
    adr_the = dr_the.mean()

    print("======TheoreticallyOptimalStrategy======")
    print("Cumulative Return: " + str(cr_the))
    print("Stdev of daily returns: " + str(sddr_the))
    print("Mean of daily returns: " + str(adr_the))
    print("")
    print("======Benchmark======")
    print("Cumulative Return: " + str(cr_ben))
    print("Stdev of daily returns: " + str(sddr_ben))
    print("Mean of daily returns: " + str(adr_ben))

def plotting_utility_function(benchmark_portvals, theoretical_portvals):
    # normalize
    benchmark_portvals['value'] = benchmark_portvals['value'] / benchmark_portvals['value'][0]
    theoretical_portvals['value'] = theoretical_portvals['value'] / theoretical_portvals['value'][0]

    plt.figure(figsize=(10, 5))
    plt.title("Theoretically Optimal Strategy")
    plt.xlabel("Date")
    plt.ylabel("Normalized Prices")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(benchmark_portvals, label="Benchmark", color="purple")
    plt.plot(theoretical_portvals, label="Theoretically Optimal Strategy", color="red")
    plt.legend()
    plt.savefig("TOS.png", bbox_inches='tight')
    plt.clf()

def report():
    # testing conditions
    sv = 100000
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)

    # get theoretical performance
    df_trades = testPolicy(['JPM'], sd=sd, ed=ed, sv=sv)
    theoretical_portvals = compute_portvals(df_trades, sv, commission=0.00, impact=0.00)
    # print(theoretical_portvals)

    # get benchmark performance
    benchmark_portvals = get_benchmark(sd, ed, sv)
    # print(benchmark_portvals)

    # get stats
    print_stats(benchmark_portvals, theoretical_portvals)

    # plot graph
    plotting_utility_function(benchmark_portvals, theoretical_portvals)


if __name__ == "__main__":
    report()
