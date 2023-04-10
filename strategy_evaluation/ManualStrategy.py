"""
Implementing Manual Rule Based Strategy using all the indicators from indicators.py

@Name : Nidhi Nirmal Menon
@UserID : nmenon34

"""


import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import *
import matplotlib.pyplot as plt

def author(self):
    """
    @summary Returning the author user ID
    """
    return 'nmenon34'

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
	print([symbol])
	dates = pd.date_range(sd, ed)
	prices_all = get_data([symbol], dates)
	prices = prices_all[[symbol]]
	flag = 0 # flag=1: have shares, flag=0 no shares, flag=-1 shorted
	lookback=20
	sym=symbol
	print(sym)
	#trades = pd.DataFrame(columns=['Symbol', 'Order', 'Shares'], index=prices.index)

	df_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])
	print("What trades looks like now", df_trades)

	sma = getSMA(prices,lookback,[symbol])
	bollinger = getBollinger(prices,[symbol],lookback,sma)
	psma = priceBySMA(prices, lookback, sma, [symbol])
	volatility = getVolatility(prices,lookback,[symbol])

	#index=0
	current_position = 0
	buydate =[]
	selldate=[]

	for i in range(len(prices)):
		if flag == 0:
			if bollinger.ix[i,sym] < 0.2 or psma.ix[i,sym] < 0.6 or volatility.ix[i,sym] < -0.1:
				flag = 1
				action = 1000 - current_position
				df_trades.loc[prices.index[i]]  = action
				current_position += action
				buydate.append(prices.index[i].date())
			elif bollinger.ix[i,sym] > 0.8 or psma.ix[i,sym] > 1.1 or volatility.ix[i,sym] > 0.1:
				flag=-1
				action = -1000 - current_position
				df_trades.loc[prices.index[i]]  = action
				current_position += action
				selldate.append(prices.index[i].date())
		elif flag == -1:
			if bollinger.ix[i,sym] < 0.1 or psma.ix[i,sym] < 0.65 or volatility.ix[i,sym] < -0.2:
				flag = 1
				action = 1000 - current_position
				df_trades.loc[prices.index[i]]  = action
				current_position += action
				buydate.append(prices.index[i].date())
			elif bollinger.ix[i,sym] < 0.2 or psma.ix[i,sym] < 0.6 or volatility.ix[i,sym] < -0.1:
				flag = 0
		elif flag == 1:
			if bollinger.ix[i,sym] > 0.9 or psma.ix[i,sym] > 1.5 or volatility.ix[i,sym] > 0.2:
				flag = -1
				action = -1000 - current_position
				df_trades.loc[prices.index[i]]  = action
				current_position += action
				selldate.append(prices.index[i].date())
			elif bollinger.ix[i,sym] > 0.8 or psma.ix[i,sym] > 1.1 or volatility.ix[i,sym]>0.1:
				#trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','SELL',1000]
				flag = 0
				#index +=1

	print(df_trades)

#	if flag==1:
#		trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','SELL',1000]
#	if flag == -1:
#		trades.loc[index] = [prices.index[i].strftime('%Y-%m-%d'),'JPM','BUY',1000]
	return df_trades, buydate, selldate

def get_benchmark(sd, ed, sv):
    df_trades = get_data(['SPY'], pd.date_range(sd, ed))
    df_trades = df_trades.rename(columns={'SPY': 'JPM'}).astype({'JPM': 'int32'})
    df_trades[:] = 0
    df_trades.loc[df_trades.index[0]] = 1000
    portvals = compute_portvals(df_trades, sv, commission=0.00, impact=0.00)
    return portvals

if __name__ == "__main__":
	sd = dt.datetime(2010,1,1)
	ed = dt.datetime(2011, 12, 31)
	sv = 100000
	symbol = ['JPM']
	dates = pd.date_range(sd, ed)

	# Benchmark
	#bench = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
	#bench.loc[0] = [prices_all.index[0].strftime('%Y-%m-%d'),'JPM','BUY',1000]
	#bench.loc[1] = [prices_all.index[-1].strftime('%Y-%m-%d'),'JPM','SELL',1000]
	#bench_port_val = compute_portvals(bench,100000,9.95,0.005)

	bench_port_val = get_benchmark(sd=sd ,ed=ed, sv=100000)
	print("Benchmark\n",bench_port_val)


	trades,buydate,selldate = testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
	prices_all = get_data(symbol, dates)
	print("Main function")
	#print(prices_all)
	#print(trades)

	# Manual Strategy
	ms_port_val = compute_portvals(trades,100000,9.95,0.005)
	print("MS POrt val",ms_port_val)
	print(trades)

	# Printing Portfolio statistics
	daily_returns = (ms_port_val / ms_port_val.shift(1)) - 1
	daily_returns = daily_returns[1:]
	cr = (ms_port_val.iloc[-1] / ms_port_val.iloc[0]) - 1
	adr = daily_returns.mean()
	sddr = daily_returns.std()
	"""
	print "Manual Strategy Stats"
	print "CR " + str(cr)
	print "Avg of daily returns " + str(adr)
	print "Std deviation of daily returns " + str(sddr)
	"""

	# Printing Benchmark statistics
	bench_dr = (bench_port_val / bench_port_val.shift(1)) - 1
	bench_dr = bench_dr[1:]
	cr = (bench_port_val.iloc[-1] / bench_port_val.iloc[0]) - 1
	adr = bench_dr.mean()
	sddr = bench_dr.std()

	"""
	print "\nBenchmark Stats"
	print "CR " + str(cr)
	print "Avg of daily returns " + str(adr)
	print "Std deviation of daily returns " + str(sddr)
	"""
	# Plotting charts
	ms_port_val = ms_port_val / ms_port_val.iloc[0]
	bench_port_val = bench_port_val / bench_port_val.iloc[0]
	ax = ms_port_val.plot(fontsize=12, color="black", label="Manual Strategy")
	bench_port_val.plot(ax=ax, color="blue", label='Benchmark')
	for date in buydate:
		ax.axvline(date,color="green")
	for date in selldate:
		ax.axvline(date,color="red")
	plt.title(" Manual Strategy - out sample ")
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio Value")
	plt.legend()
	plt.show()
