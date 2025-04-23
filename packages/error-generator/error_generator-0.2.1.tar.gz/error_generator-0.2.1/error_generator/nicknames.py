import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional, Tuple, Any
from .base import update_error_record

# Initialize variables as None - will be loaded on demand
nick_real_lookup = None
names_lookup = None

def _load_nick_real_lookup():
    """Load nickname lookup table if needed and available"""
    global nick_real_lookup
    try:
        nick_real_lookup = pd.read_csv('data/nick_real_lookup.csv')
    except FileNotFoundError:
        raise RuntimeError("nick_real_lookup.csv not found. Nickname error types require this file to be present in the data directory.")

def _load_names_lookup():
    """Load names lookup table if needed and available"""
    global names_lookup
    try:
        names_lookup = pd.read_csv('data/names_lookup.csv')
    except FileNotFoundError:
        raise RuntimeError("names_lookup.csv not found. Nickname error types require this file to be present in the data directory.")

def real_to_nicknames(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Convert real names to nicknames.
    
    Args:
        df: DataFrame containing names
        n_errors: Number of names to convert
        col_names: List of column names containing names to convert
        
    Returns:
        DataFrame with converted names
    """
    if names_lookup is None:
        _load_names_lookup()
        
    df = df.copy()
    errors_per_col = n_errors // len(col_names)
    
    for col_name in col_names:
        # Get lookup data for nicknames
        lookup = (names_lookup[names_lookup['lookup_type'] == 'to_nick']
                 .merge(df, left_on='lookup_name', right_on=col_name))
        
        # Group by lookup name and sample one nickname per name
        lookup = (lookup.groupby('lookup_name')
                 .apply(lambda x: x.sample(n=1))
                 .reset_index(drop=True))
        
        # Sample the required number of names to convert
        n_available = len(lookup)
        n_convert = min(errors_per_col, n_available)
        if n_convert < errors_per_col:
            print(f"Not enough matches found for nicknames. Using all available matches ({n_convert}).")
            
        lookup = lookup.sample(n=n_convert)
        
        # Update names in the DataFrame
        df = df.merge(lookup[['id', 'lookup_alternate']], on='id', how='left')
        old_names = df[col_name].copy()
        df[col_name] = df['lookup_alternate'].fillna(df[col_name])
        
        # Record the changes
        mask = df['lookup_alternate'].notna()
        if mask.any():
            update_error_record(df,
                              df.loc[mask, 'id'].tolist(),
                              col_name,
                              'to_nickname',
                              old_names[mask].tolist(),
                              df.loc[mask, col_name].tolist())
        
        # Clean up temporary columns
        df = df.drop('lookup_alternate', axis=1)
        
    return df

def nick_to_realnames(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Convert nicknames to real names.
    
    Args:
        df: DataFrame containing names
        n_errors: Number of names to convert
        col_names: List of column names containing names to convert
        
    Returns:
        DataFrame with converted names
    """
    if names_lookup is None:
        _load_names_lookup()
        
    df = df.copy()
    errors_per_col = n_errors // len(col_names)
    
    for col_name in col_names:
        # Get lookup data for real names
        lookup = (names_lookup[names_lookup['lookup_type'] == 'to_proper']
                 .merge(df, left_on='lookup_name', right_on=col_name))
        
        # Group by lookup name and sample one real name per nickname
        lookup = (lookup.groupby('lookup_name')
                 .apply(lambda x: x.sample(n=1))
                 .reset_index(drop=True))
        
        # Sample the required number of names to convert
        n_available = len(lookup)
        n_convert = min(errors_per_col, n_available)
        if n_convert < errors_per_col:
            print(f"Not enough matches found for realnames. Using all available matches ({n_convert}).")
            
        lookup = lookup.sample(n=n_convert)
        
        # Update names in the DataFrame
        df = df.merge(lookup[['id', 'lookup_alternate']], on='id', how='left')
        old_names = df[col_name].copy()
        df[col_name] = df['lookup_alternate'].fillna(df[col_name])
        
        # Record the changes
        mask = df['lookup_alternate'].notna()
        if mask.any():
            update_error_record(df,
                              df.loc[mask, 'id'].tolist(),
                              col_name,
                              'to_realname',
                              old_names[mask].tolist(),
                              df.loc[mask, col_name].tolist())
        
        # Clean up temporary columns
        df = df.drop('lookup_alternate', axis=1)
        
    return df

def invert_real_and_nicknames(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """
    Invert real names and nicknames.
    
    Args:
        df: DataFrame containing names
        n_errors: Number of names to invert
        col_names: List of column names containing names to invert
        
    Returns:
        DataFrame with inverted names
    """
    if nick_real_lookup is None:
        _load_nick_real_lookup()
        
    df = df.copy()
    errors_per_col = n_errors // len(col_names)
    
    for col_name in col_names:
        # Get lookup data for name pairs
        lookup = nick_real_lookup.merge(df, left_on='key', right_on=col_name)
        
        # Group by key and sample one alternate name per name
        lookup = (lookup.groupby('key')
                 .apply(lambda x: x.sample(n=1))
                 .reset_index(drop=True))
        
        # Sample the required number of names to convert
        n_available = len(lookup)
        n_convert = min(errors_per_col, n_available)
        if n_convert < errors_per_col:
            print(f"Not enough matches found for nick or realnames. Using all available matches ({n_convert}).")
            
        lookup = lookup.sample(n=n_convert)
        
        # Update names in the DataFrame
        df = df.merge(lookup[['id', 'lookup']], on='id', how='left')
        old_names = df[col_name].copy()
        df[col_name] = df['lookup'].fillna(df[col_name])
        
        # Record the changes
        mask = df['lookup'].notna()
        if mask.any():
            update_error_record(df,
                              df.loc[mask, 'id'].tolist(),
                              col_name,
                              'invert_nick_realnames',
                              old_names[mask].tolist(),
                              df.loc[mask, col_name].tolist())
        
        # Clean up temporary columns
        df = df.drop('lookup', axis=1)
        
    return df

def add_name_suffix(df: pd.DataFrame, 
                   n_errors: int, 
                   lname: str, 
                   sex: str, 
                   suffix_list: List[str] = None, 
                   suffix_weights: List[float] = None) -> pd.DataFrame:
    """
    Add suffixes to last names for male individuals.
    
    Args:
        df: DataFrame containing names
        n_errors: Number of names to add suffixes to
        lname: Column name containing last names
        sex: Column name containing sex information
        suffix_list: List of suffixes to use
        suffix_weights: Weights for sampling suffixes
        
    Returns:
        DataFrame with added name suffixes
    """
    if suffix_list is None:
        suffix_list = ["JR", "III", "II", "SR", "IV", "I", "V"]
    if suffix_weights is None:
        suffix_weights = [300, 40, 40, 40, 10, 10, 10]
        
    df = df.copy()
    
    # Get male IDs
    male_mask = df[sex].str.lower() == 'm'
    male_ids = df.loc[male_mask, 'id'].values
    
    if len(male_ids) < n_errors:
        n_errors = len(male_ids)
        print("Warning: Not enough candidates for suffixes found.")
        
    # Sample IDs to modify
    candidate_ids = np.random.choice(male_ids, size=n_errors, replace=False)
    
    # Get current last names
    mask = df['id'].isin(candidate_ids)
    old_names = df.loc[mask, lname].copy()
    
    # Sample suffixes
    suffixes = np.random.choice(suffix_list, size=len(candidate_ids), p=np.array(suffix_weights)/sum(suffix_weights))
    
    # Create new names with suffixes
    new_names = old_names + ' ' + suffixes
    
    # Update names in the DataFrame
    df.loc[mask, lname] = new_names
    
    # Record the changes
    update_error_record(df,
                       candidate_ids.tolist(),
                       lname,
                       'name_suffix',
                       old_names.tolist(),
                       new_names.tolist())
    
    return df 

def introduce_nickname_errors(df: pd.DataFrame, n_errors: int, col_names: List[str], **kwargs) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """
    Introduce nickname errors into specified columns
    """
    if names_lookup is None:
        _load_names_lookup()
    # ... rest of function implementation ...
    return df.copy(), []  # Placeholder implementation 