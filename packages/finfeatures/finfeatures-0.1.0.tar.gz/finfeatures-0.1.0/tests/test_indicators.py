import pandas as pd
import pytest
import finfeatures as ff

def test_simple_moving_average():
    data = {'Close': [1,2,3,4,5,6,7,8,9,10]}
    df = pd.DataFrame(data)
    df = ff.simple_moving_average(df, column='Close', window=3)
    assert 'Close_SMA_3' in df.columns

def test_exponential_moving_average():
    data = {'Close': [1,2,3,4,5,6,7,8,9,10]}
    df = pd.DataFrame(data)
    df = ff.exponential_moving_average(df, column='Close', window=3)
    assert 'Close_EMA_3' in df.columns

def test_relative_strength_index():
    data = {'Close': [1,2,3,4,5,6,7,8,9,10]}
    df = pd.DataFrame(data)
    df = ff.relative_strength_index(df, column='Close')
    assert 'Close_RSI_14' in df.columns

def test_macd():
    data = {'Close': [1,2,3,4,5,6,7,8,9,10]}
    df = pd.DataFrame(data)
    df = ff.macd(df, column='Close')
    assert 'MACD' in df.columns
    assert 'MACD_Signal' in df.columns

def test_bollinger_bands():
    data = {'Close': [1,2,3,4,5,6,7,8,9,10]}
    df = pd.DataFrame(data)
    df = ff.bollinger_bands(df, column='Close')
    assert 'Close_BB_upper' in df.columns
    assert 'Close_BB_lower' in df.columns

def test_average_true_range():
    data = {'High': [2,3,4,5,6,7,8,9,10,11], 'Low': [1,2,3,4,5,6,7,8,9,10], 'Close': [1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]}
    df = pd.DataFrame(data)
    df = ff.average_true_range(df, high_col='High', low_col='Low', close_col='Close')
    assert 'ATR_14' in df.columns

def test_stochastic_oscillator():
    data = {'High': [2,3,4,5,6,7,8,9,10,11], 'Low': [1,2,3,4,5,6,7,8,9,10], 'Close': [1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]}
    df = pd.DataFrame(data)
    df = ff.stochastic_oscillator(df, high_col='High', low_col='Low', close_col='Close')
    assert 'Stoch_14' in df.columns

def test_premium_feature_set():
    data = {'High': [2,3,4,5,6,7,8,9,10,11], 'Low': [1,2,3,4,5,6,7,8,9,10], 'Close': [1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5]}
    df = pd.DataFrame(data)
    df = ff.premium_feature_set(df, close_col='Close', high_col='High', low_col='Low')
    assert 'ATR_14' in df.columns
    assert 'Stoch_14' in df.columns