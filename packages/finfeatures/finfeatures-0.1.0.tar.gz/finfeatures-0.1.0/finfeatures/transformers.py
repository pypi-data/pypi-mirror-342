import pandas as pd
from .utils import validate_inputs

def rolling_volatility(df, column: str, window: int) -> pd.DataFrame:
    validate_inputs(df, column)
    df[f'{column}_RollingVol_{window}'] = df[column].rolling(window=window).std()
    return df

def percent_change(df, column: str, periods: int = 1) -> pd.DataFrame:
    validate_inputs(df, column)
    df[f'{column}_PctChange_{periods}'] = df[column].pct_change(periods=periods)
    return df


