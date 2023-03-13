"""
Student Name: Vaishnavi Sanjeev
GT User ID: vsanjeev6
GT ID: 903797718
"""

def author():
    return 'vsanjeev6'

import datetime as dt
import TheoreticallyOptimalStrategy as tos
import indicators as ti

# Theoretically Optimal Strategy
df_trades = tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
# Technical Indicators
ti.run(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31))

if __name__ == "__main__":
    pass
