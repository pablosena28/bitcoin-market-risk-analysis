"""Métricas de risco e retorno para séries diárias de Bitcoin."""
from __future__ import annotations
import numpy as np
import pandas as pd

def add_market_metrics(df: pd.DataFrame) -> pd.DataFrame:
    data=df.copy()
    data["Date"]=pd.to_datetime(data["Date"])
    data=data.sort_values("Date").reset_index(drop=True)
    data["daily_return"]=data["Adj Close"].pct_change()
    data["cumulative_return"]=data["Adj Close"]/data["Adj Close"].iloc[0]-1
    peak=data["Adj Close"].cummax()
    data["drawdown"]=data["Adj Close"]/peak-1
    data["rolling_vol_30"]=data["daily_return"].rolling(30).std()*np.sqrt(365)
    return data

def annualized_volatility(returns: pd.Series, periods: int=365) -> float:
    return float(returns.dropna().std()*np.sqrt(periods))

def max_drawdown(price: pd.Series) -> float:
    peak=price.cummax()
    return float((price/peak-1).min())

def cagr(start_value: float, end_value: float, calendar_days: int) -> float:
    years=calendar_days/365.25
    return float((end_value/start_value)**(1/years)-1)
