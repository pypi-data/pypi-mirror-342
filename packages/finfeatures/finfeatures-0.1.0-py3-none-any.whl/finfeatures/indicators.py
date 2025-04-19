import pandas as pd
from .utils import validate_inputs

def simple_moving_average(df, column: str, window: int) -> pd.DataFrame:
    validate_inputs(df, column)
    df[f'{column}_SMA_{window}'] = df[column].rolling(window=window).mean()
    return df

def exponential_moving_average(df, column: str, window: int) -> pd.DataFrame:
    validate_inputs(df, column)
    df[f'{column}_EMA_{window}'] = df[column].ewm(span=window, adjust=False).mean()
    return df

def relative_strength_index(df, column: str, window: int = 14) -> pd.DataFrame:
    validate_inputs(df, column)
    delta = df[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df[f'{column}_RSI_{window}'] = 100 - (100 / (1 + rs))
    return df

def macd(df, column: str, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    validate_inputs(df, column)
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    return df

def bollinger_bands(df, column: str, window: int = 20, num_std: int = 2) -> pd.DataFrame:
    validate_inputs(df, column)
    rolling_mean = df[column].rolling(window).mean()
    rolling_std = df[column].rolling(window).std()
    df[f'{column}_BB_upper'] = rolling_mean + (rolling_std * num_std)
    df[f'{column}_BB_lower'] = rolling_mean - (rolling_std * num_std)
    return df

def average_true_range(df, high_col: str, low_col: str, close_col: str, window: int = 14) -> pd.DataFrame:
    validate_inputs(df, high_col)
    validate_inputs(df, low_col)
    validate_inputs(df, close_col)
    high_low = df[high_col] - df[low_col]
    high_close = (df[high_col] - df[close_col].shift()).abs()
    low_close = (df[low_col] - df[close_col].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df[f'ATR_{window}'] = tr.rolling(window=window).mean()
    return df

def stochastic_oscillator(df, high_col: str, low_col: str, close_col: str, window: int = 14) -> pd.DataFrame:
    validate_inputs(df, high_col)
    validate_inputs(df, low_col)
    validate_inputs(df, close_col)
    lowest_low = df[low_col].rolling(window=window).min()
    highest_high = df[high_col].rolling(window=window).max()
    df[f'Stoch_{window}'] = 100 * ((df[close_col] - lowest_low) / (highest_high - lowest_low))
    return df

def basic_feature_set(df, column: str = 'Close') -> pd.DataFrame:
    df = simple_moving_average(df, column, window=20)
    df = exponential_moving_average(df, column, window=20)
    df = relative_strength_index(df, column)
    df = macd(df, column)
    df = bollinger_bands(df, column)
    return df

def premium_feature_set(df, close_col: str = 'Close', high_col: str = 'High', low_col: str = 'Low') -> pd.DataFrame:
    df = basic_feature_set(df, column=close_col)
    df = average_true_range(df, high_col=high_col, low_col=low_col, close_col=close_col)
    df = stochastic_oscillator(df, high_col=high_col, low_col=low_col, close_col=close_col)
    return df