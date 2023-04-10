import pandas as pd
import numpy as np
from util import get_data

def author():
  return 'pcometti3' # replace tb34 with your Georgia Tech username.

def compute_portvals(orders, start_val=100000):
    """
    Compute the value of the portfolio for the given orders.

    Parameters
    ----------
    orders : pandas.DataFrame
        A single column data frame, indexed by date, whose values represent
        trades for each trading day.
    start_val : int, optional
        the start value of the portfolio. The default is 100000.

    Returns
    -------
    df_portvals : pandas.DataFrame
        A single-column dataframe, indexed by date, whose values represent
        the portfolio value for each trading day.

    """
    symbol = orders.columns[0]

    # Create the prices dataframe
    df_prices = get_data([symbol], orders.index)
    
    # Remove the SPY column
    df_prices = df_prices.drop('SPY', axis=1)
    
    # Fill the Cash column with ones
    df_prices['Cash'] = np.ones(len(df_prices))

    # Init the trades & holdings DFs
    df_trades = orders.copy()
    df_trades['Cash'] = - orders[symbol] * df_prices[symbol]

    # Init the cash value of holdings to the start value
    df_holdings = df_trades.copy()
    df_holdings[symbol] = np.zeros(len(df_holdings))
    df_holdings['Cash'] = np.ones(len(df_prices)) * start_val

    # Loop over the trades to get the full holdings
    inds = list(df_holdings.index)
    for k, idx in enumerate(inds):
        df_holdings.loc[idx] = df_holdings.loc[inds[k-1]] + df_trades.loc[idx]

    # Compute the value of each stock
    df_value = df_holdings.copy()
    df_value *= df_prices

    # Compute the value of the full portfolio
    df_portvals = pd.DataFrame(df_value.sum(axis=1), columns=['Cash'])

    return df_portvals


if __name__ == "__main__":
    print("Check testproject.py")