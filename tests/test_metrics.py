import pandas as pd
from src.metrics import annualized_volatility, cagr, max_drawdown

def test_max_drawdown():
    prices=pd.Series([100.0,120.0,90.0,110.0])
    assert round(max_drawdown(prices),4)==-0.25

def test_annualized_volatility_is_non_negative():
    returns=pd.Series([0.01,-0.02,0.015,-0.005])
    assert annualized_volatility(returns)>=0

def test_cagr_positive_when_end_value_is_higher():
    assert cagr(100.0,200.0,365)>0
