import pandas as pd
import numpy as np
from typing import List, Union, Optional
import re
from .base import update_error_record
from .error_record import ErrorRecord

def first_letter_abbreviate(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Abbreviate strings to their first letter.
    
    Args:
        df: DataFrame to modify
        n_errors: Number of errors to introduce
        col_names: List of column names to apply errors to
        
    Returns:
        Modified DataFrame with introduced errors
    """
    df = df.copy()
    n = len(df)
    p = len(col_names)
    errors_per_col = n_errors // p
    
    # Create error record if not present
    if not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
    
    if (n_errors < n * p) and (errors_per_col > 0):
        for col_name in col_names:
            # Get eligible rows
            eligible_mask = df[col_name].astype(str).str.len() > 1
            eligible_ids = df.loc[eligible_mask, 'id'].values
            
            if len(eligible_ids) == 0:
                continue
                
            # Sample rows to modify
            candidate_ids = np.random.choice(eligible_ids, 
                                          size=min(errors_per_col, len(eligible_ids)), 
                                          replace=False)
            
            # Apply errors
            mask = df['id'].isin(candidate_ids)
            before_values = df.loc[mask, col_name].astype(str).values
            after_values = [val[0] for val in before_values]
            
            df.loc[mask, col_name] = after_values
            
            # Update error record
            for id_, before, after in zip(df.loc[mask, 'id'].tolist(), 
                                        before_values.tolist(), 
                                        after_values):
                df.error_record.add_error(id_, col_name, 'first_letter_abbreviate', before, after)
    else:
        for _ in range(n_errors):
            row_idx = np.random.randint(0, n)
            col_name = np.random.choice(col_names)
            
            before_value = str(df.iloc[row_idx][col_name])
            if len(before_value) <= 1:
                continue
                
            after_value = before_value[0]
            df.iloc[row_idx][col_name] = after_value
            
            # Update error record
            df.error_record.add_error(df.iloc[row_idx]['id'], 
                                    col_name, 
                                    'first_letter_abbreviate', 
                                    before_value, 
                                    after_value)
            
    return df

def ch1_to_ch2(df: pd.DataFrame, n_errors: int, col_names: List[str], 
               ch1: str, ch2: str, all_occurrences: bool = True) -> pd.DataFrame:
    """
    Replace character ch1 with character ch2 in strings.
    
    Args:
        df: DataFrame containing strings to modify
        n_errors: Number of strings to modify
        col_names: List of column names containing strings to modify
        ch1: Character to replace
        ch2: Character to replace with
        all_occurrences: Whether to replace all occurrences or just the first one
        
    Returns:
        DataFrame with modified strings
    """
    df = df.copy()
    errors_per_col = n_errors // len(col_names)
    
    for col_name in col_names:
        # Find records containing ch1
        pattern = f'\\w{ch1}\\w'
        mask = df[col_name].str.contains(pattern, regex=True, na=False)
        feasible_records = df[mask]
        
        if len(feasible_records) == 0:
            print(f"Warning: No records with '{ch1}' found in column {col_name}")
            continue
            
        # Sample records to modify
        n_modify = min(errors_per_col, len(feasible_records))
        candidate_ids = feasible_records['id'].sample(n=n_modify).values
        
        # Get current values
        mask = df['id'].isin(candidate_ids)
        old_names = df.loc[mask, col_name].copy()
        
        # Replace characters
        if all_occurrences:
            new_names = old_names.str.replace(ch1, ch2, regex=False)
        else:
            new_names = old_names.str.replace(ch1, ch2, n=1, regex=False)
            
        # Update values
        df.loc[mask, col_name] = new_names
        
        # Record changes
        update_error_record(df,
                          candidate_ids.tolist(),
                          col_name,
                          f'{ch1}to{ch2}',
                          old_names.tolist(),
                          new_names.tolist())
    
    return df

def blanks_to_hyphens(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Replace spaces with hyphens.
    
    Args:
        df: DataFrame to modify
        n_errors: Number of errors to introduce
        col_names: List of column names to apply errors to
        
    Returns:
        Modified DataFrame with introduced errors
    """
    df = df.copy()
    n = len(df)
    p = len(col_names)
    errors_per_col = n_errors // p
    
    # Create error record if not present
    if not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
    
    if (n_errors < n * p) and (errors_per_col > 0):
        for col_name in col_names:
            # Get eligible rows
            eligible_mask = df[col_name].astype(str).str.contains(' ')
            eligible_ids = df.loc[eligible_mask, 'id'].values
            
            if len(eligible_ids) == 0:
                continue
                
            # Sample rows to modify
            candidate_ids = np.random.choice(eligible_ids, 
                                          size=min(errors_per_col, len(eligible_ids)), 
                                          replace=False)
            
            # Apply errors
            mask = df['id'].isin(candidate_ids)
            before_values = df.loc[mask, col_name].astype(str).values
            after_values = [val.replace(' ', '-') for val in before_values]
            
            df.loc[mask, col_name] = after_values
            
            # Update error record
            for id_, before, after in zip(df.loc[mask, 'id'].tolist(), 
                                        before_values.tolist(), 
                                        after_values):
                df.error_record.add_error(id_, col_name, 'blanks_to_hyphens', before, after)
    else:
        for _ in range(n_errors):
            row_idx = np.random.randint(0, n)
            col_name = np.random.choice(col_names)
            
            before_value = str(df.iloc[row_idx][col_name])
            if ' ' not in before_value:
                continue
                
            after_value = before_value.replace(' ', '-')
            df.iloc[row_idx][col_name] = after_value
            
            # Update error record
            df.error_record.add_error(df.iloc[row_idx]['id'], 
                                    col_name, 
                                    'blanks_to_hyphens', 
                                    before_value, 
                                    after_value)
            
    return df

def hyphens_to_blanks(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Replace hyphens with spaces.
    
    Args:
        df: DataFrame to modify
        n_errors: Number of errors to introduce
        col_names: List of column names to apply errors to
        
    Returns:
        Modified DataFrame with introduced errors
    """
    df = df.copy()
    n = len(df)
    p = len(col_names)
    errors_per_col = n_errors // p
    
    # Create error record if not present
    if not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
    
    if (n_errors < n * p) and (errors_per_col > 0):
        for col_name in col_names:
            # Get eligible rows
            eligible_mask = df[col_name].astype(str).str.contains('-')
            eligible_ids = df.loc[eligible_mask, 'id'].values
            
            if len(eligible_ids) == 0:
                continue
                
            # Sample rows to modify
            candidate_ids = np.random.choice(eligible_ids, 
                                          size=min(errors_per_col, len(eligible_ids)), 
                                          replace=False)
            
            # Apply errors
            mask = df['id'].isin(candidate_ids)
            before_values = df.loc[mask, col_name].astype(str).values
            after_values = [val.replace('-', ' ') for val in before_values]
            
            df.loc[mask, col_name] = after_values
            
            # Update error record
            for id_, before, after in zip(df.loc[mask, 'id'].tolist(), 
                                        before_values.tolist(), 
                                        after_values):
                df.error_record.add_error(id_, col_name, 'hyphens_to_blanks', before, after)
    else:
        for _ in range(n_errors):
            row_idx = np.random.randint(0, n)
            col_name = np.random.choice(col_names)
            
            before_value = str(df.iloc[row_idx][col_name])
            if '-' not in before_value:
                continue
                
            after_value = before_value.replace('-', ' ')
            df.iloc[row_idx][col_name] = after_value
            
            # Update error record
            df.error_record.add_error(df.iloc[row_idx]['id'], 
                                    col_name, 
                                    'hyphens_to_blanks', 
                                    before_value, 
                                    after_value)
            
    return df

def make_missing(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Set random values to NaN in specified columns.
    
    Args:
        df: DataFrame to modify
        n_errors: Number of errors to introduce
        col_names: List of column names to apply errors to
        
    Returns:
        Modified DataFrame with introduced errors
    """
    df = df.copy()
    n = len(df)
    p = len(col_names)
    errors_per_col = n_errors // p
    
    # Create error record if not present
    if not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
    
    if (n_errors < n * p) and (errors_per_col > 0):
        for col_name in col_names:
            # Get eligible rows (where the column value is not already NaN)
            eligible_mask = df[col_name].notna().values  # Convert to numpy array
            if not any(eligible_mask):
                continue
                
            # Get eligible indices and their corresponding IDs
            eligible_indices = np.where(eligible_mask)[0]
            eligible_ids = df.iloc[eligible_indices]['id'].values
            
            if len(eligible_ids) == 0:
                continue
                
            # Sample rows to modify
            n_samples = min(errors_per_col, len(eligible_ids))
            selected_indices = np.random.choice(range(len(eligible_ids)), 
                                             size=n_samples,
                                             replace=False)
            candidate_ids = eligible_ids[selected_indices]
            
            # Apply errors
            mask = df['id'].isin(candidate_ids)
            before_values = df.loc[mask, col_name].astype(str).values  # Convert to numpy array first
            
            # Store before values and IDs before modification
            id_values = df.loc[mask, 'id'].tolist()
            
            # Set values to NaN
            df.loc[mask, col_name] = np.nan
            
            # Update error record
            for id_, before in zip(id_values, before_values):
                df.error_record.add_error(id_, col_name, 'missing', before, 'NA')
    else:
        attempts = 0
        errors_added = 0
        max_attempts = n_errors * 3  # Prevent infinite loops
        
        while errors_added < n_errors and attempts < max_attempts:
            row_idx = np.random.randint(0, n)
            col_name = np.random.choice(col_names)
            
            value = df.iloc[row_idx][col_name]
            if pd.isna(value):
                attempts += 1
                continue
                
            before_value = str(value)
            df.iloc[row_idx, df.columns.get_loc(col_name)] = np.nan
            
            # Update error record
            df.error_record.add_error(df.iloc[row_idx]['id'], 
                                    col_name, 
                                    'missing', 
                                    before_value, 
                                    'NA')
            errors_added += 1
            
    return df 