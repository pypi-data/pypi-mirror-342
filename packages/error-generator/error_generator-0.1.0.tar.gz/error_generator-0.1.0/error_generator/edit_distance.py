import random
import string
from typing import List, Union, Optional
import pandas as pd
import numpy as np
from .error_record import update_error_record, ErrorRecord

def indel_string(edit_string: str, error_chars: List[str] = None) -> str:
    """
    Insert or delete a character in the given string.
    
    Args:
        edit_string: String to modify
        error_chars: List of characters to use for insertion
        
    Returns:
        Modified string with one character inserted or deleted
    """
    if error_chars is None:
        error_chars = list(string.ascii_lowercase)
        
    length = len(edit_string)
    
    if random.random() > 0.5:  # insert
        add_letter = random.choice(error_chars)
        cut = random.randint(0, length)
        
        if cut == 0:
            return add_letter + edit_string
        elif cut == length:
            return edit_string + add_letter
        else:
            return edit_string[:cut] + add_letter + edit_string[cut:]
    else:  # delete
        if length <= 1:  # prevent empty strings
            return edit_string
            
        rem = random.randint(1, length)
        if rem == 1:
            return edit_string[1:]
        elif rem == length:
            return edit_string[:-1]
        else:
            return edit_string[:rem-1] + edit_string[rem:]

def repl_string(edit_string: str, error_chars: List[str] = None) -> str:
    """
    Replace a character in the given string with another character.
    
    Args:
        edit_string: String to modify
        error_chars: List of characters to use for replacement
        
    Returns:
        Modified string with one character replaced
    """
    if error_chars is None:
        error_chars = list(string.ascii_lowercase)
        
    if not edit_string:
        return edit_string
        
    repl_index = random.randint(0, len(edit_string) - 1)
    chars = list(edit_string)
    
    subs = random.choice(error_chars)
    while chars[repl_index] == subs:
        subs = random.choice(error_chars)
        
    chars[repl_index] = subs
    return ''.join(chars)

def tpose_eligible(items: Union[str, List[str]]) -> Union[bool, List[bool]]:
    """
    Check if string(s) are eligible for transposition.
    
    Args:
        items: String or list of strings to check
        
    Returns:
        Boolean or list of booleans indicating eligibility
    """
    if isinstance(items, str):
        items = [items]
        
    count_chars = list(string.ascii_letters + ' ')
    return [sum(c in item for c in count_chars) > 1 for item in items]

def tpose_string(edit_string: str) -> str:
    """
    Transpose two adjacent characters in the string.
    
    Args:
        edit_string: String to modify
        
    Returns:
        Modified string with two adjacent characters transposed
    """
    if len(edit_string) <= 1:
        return edit_string
        
    chars = list(edit_string)
    unique_chars = set(chars)
    
    if len(unique_chars) <= 1:
        return edit_string
        
    tpose_index = random.randint(1, len(chars)-1)
    tpose_index_l = tpose_index - 1
    
    # Find positions where adjacent characters are different
    while chars[tpose_index] == chars[tpose_index_l]:
        tpose_index = random.randint(1, len(chars)-1)
        tpose_index_l = tpose_index - 1
        
    # Swap characters
    chars[tpose_index], chars[tpose_index_l] = chars[tpose_index_l], chars[tpose_index]
    return ''.join(chars)

def apply_edit_distance_error(df: pd.DataFrame, n_errors: int, col_names: List[str], 
                            error_type: str) -> pd.DataFrame:
    """
    Apply edit distance errors to specified columns in the DataFrame.
    
    Args:
        df: DataFrame to modify
        n_errors: Number of errors to introduce
        col_names: List of column names to apply errors to
        error_type: Type of error to apply ('indel', 'repl', or 'tpose')
        
    Returns:
        Modified DataFrame with introduced errors
    """
    df = df.copy()
    n = len(df)
    p = len(col_names)
    errors_per_col = n_errors // p
    
    error_funcs = {
        'indel': indel_string,
        'repl': repl_string,
        'tpose': tpose_string
    }
    
    if error_type not in error_funcs:
        raise ValueError(f"Unknown error type: {error_type}")
        
    error_func = error_funcs[error_type]
    
    # Create error record if not present
    if not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
    
    if (n_errors < n * p) and (errors_per_col > 0):
        for col_name in col_names:
            # Get eligible rows
            if error_type == 'tpose':
                eligible_mask = tpose_eligible(df[col_name].astype(str))
                eligible_ids = df.loc[eligible_mask, 'id'].values
            else:
                eligible_ids = df.loc[df[col_name].astype(str).str.len() > 0, 'id'].values
                
            if len(eligible_ids) == 0:
                continue
                
            # Sample rows to modify
            candidate_ids = np.random.choice(eligible_ids, 
                                          size=min(errors_per_col, len(eligible_ids)), 
                                          replace=False)
            
            # Apply errors
            mask = df['id'].isin(candidate_ids)
            before_values = df.loc[mask, col_name].astype(str).values
            
            # Handle numeric columns
            is_numeric = pd.api.types.is_numeric_dtype(df[col_name])
            error_chars = list('0123456789') if is_numeric else None
            
            after_values = [error_func(val, error_chars) if error_type != 'tpose' else error_func(val) 
                          for val in before_values]
            
            # Convert back to numeric if needed
            if is_numeric:
                after_values = pd.to_numeric(after_values, errors='coerce')
                
            df.loc[mask, col_name] = after_values
            
            # Update error record
            for id_, before, after in zip(df.loc[mask, 'id'].tolist(), 
                                        before_values.tolist(), 
                                        [str(x) for x in after_values]):
                df.error_record.add_error(id_, col_name, error_type, before, after)
    else:
        for _ in range(n_errors):
            row_idx = random.randint(0, n-1)
            col_name = random.choice(col_names)
            
            before_value = str(df.iloc[row_idx][col_name])
            if not before_value:
                continue
                
            is_numeric = pd.api.types.is_numeric_dtype(df[col_name])
            error_chars = list('0123456789') if is_numeric else None
            
            after_value = error_func(before_value, error_chars) if error_type != 'tpose' else error_func(before_value)
            
            if is_numeric:
                after_value = pd.to_numeric(after_value, errors='coerce')
                
            df.iloc[row_idx][col_name] = after_value
            
            # Update error record
            df.error_record.add_error(df.iloc[row_idx]['id'], 
                                    col_name, 
                                    error_type, 
                                    before_value, 
                                    str(after_value))
            
    return df

def indel(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """Apply insertion/deletion errors."""
    return apply_edit_distance_error(df, n_errors, col_names, 'indel')

def repl(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """Apply replacement errors."""
    return apply_edit_distance_error(df, n_errors, col_names, 'repl')

def tpose(df: pd.DataFrame, n_errors: int, col_names: List[str]) -> pd.DataFrame:
    """Apply transposition errors."""
    return apply_edit_distance_error(df, n_errors, col_names, 'tpose') 