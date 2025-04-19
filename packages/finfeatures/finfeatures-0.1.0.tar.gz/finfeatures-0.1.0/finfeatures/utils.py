# ---- FILE: finfeatures/utils.py ----
def validate_inputs(df, column: str):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")