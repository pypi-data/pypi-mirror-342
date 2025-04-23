import pandas as pd
import numpy as np
from typing import List
from .base import update_error_record

def swap_fields(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Swap values between pairs of columns.
    
    Args:
        df: DataFrame containing fields to swap
        n_errors: Number of rows to apply swaps to
        col_names: List of column names in pairs (must be even length)
        
    Returns:
        DataFrame with swapped values
    """
    if len(col_names) % 2 != 0:
        raise ValueError("col_names must contain pairs of columns (even length)")
        
    df = df.copy()
    n = len(df)
    p = len(col_names) // 2
    errors_per_col = n_errors // p
    
    for i in range(0, len(col_names), 2):
        col_1 = col_names[i]
        col_2 = col_names[i + 1]
        
        # Sample rows to modify
        rows = np.random.choice(n, size=n_errors, replace=False)
        
        # Get current values
        c1 = df.iloc[rows][col_1].copy()
        c2 = df.iloc[rows][col_2].copy()
        
        # Swap values
        df.iloc[rows, df.columns.get_loc(col_1)] = c2
        df.iloc[rows, df.columns.get_loc(col_2)] = c1
        
        # Create before/after strings for error record
        before_values = [f"{x}, {y}" for x, y in zip(c1, c2)]
        after_values = [f"{y}, {x}" for x, y in zip(c1, c2)]
        
        # Record changes
        update_error_record(df,
                          df.iloc[rows]['id'].tolist(),
                          f"{col_1}, {col_2}",
                          'swap',
                          before_values,
                          after_values)
    
    return df 