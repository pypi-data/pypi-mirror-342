import pandas as pd
import numpy as np
from typing import List, Dict, Union, Optional
from copy import deepcopy
from .error_record import ErrorRecord, update_error_record, DataFramePair

# Import error functions
from .edit_distance import indel, repl, tpose
from .nicknames import (introduce_nickname_errors,
                    real_to_nicknames as to_nickname,
                    nick_to_realnames as to_realname, 
                    invert_real_and_nicknames, add_name_suffix)
from .abbreviations import (first_letter_abbreviate, blanks_to_hyphens,
                          hyphens_to_blanks, make_missing)
from .swaps import swap_fields
from .file_based import married_name_change, add_duplicates, twins_generate
from .dob import (gen_birthday_from_age, date_swap, date_transpose, date_replace)

# Create function registry
ERROR_FUNCTIONS = {
    'indel': indel,
    'repl': repl,
    'tpose': tpose,
    'to_nickname': to_nickname,
    'to_realname': to_realname,
    'invert_nick_realnames': invert_real_and_nicknames,
    'name_suffix': add_name_suffix,
    'first_letter_abbreviate': first_letter_abbreviate,
    'blanks_to_hyphens': blanks_to_hyphens,
    'hyphens_to_blanks': hyphens_to_blanks,
    'missing': make_missing,
    'swap': swap_fields,
    'married_name_change': married_name_change,
    'duplicate': add_duplicates,
    'twins': twins_generate,
    'date_month_swap': date_swap,
    'date_transpose': date_transpose,
    'date_replace': date_replace
}

def prep_data(df_original: pd.DataFrame) -> DataFramePair:
    """
    Prepare data by creating original (file = A) and secondary (file = B) versions.
    
    Args:
        df_original: Input DataFrame to be prepared
        
    Returns:
        DataFramePair object containing original and secondary DataFrames
    """
    # Create a copy to avoid modifying the input
    df = df_original.copy()
    
    # Add file and id columns
    df['file'] = 'A'
    if 'id' not in df.columns:
        df['id'] = range(1, len(df) + 1)
    
    # Reorder columns to put file and id first
    cols = ['file', 'id'] + [col for col in df.columns if col not in ['file', 'id']]
    df = df[cols]
    
    # Convert string columns to lowercase
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.lower()
    
    # Create secondary DataFrame
    df_secondary = df.copy()
    df_secondary['file'] = 'B'
    
    # Initialize error record
    df_secondary.error_record = ErrorRecord()
    
    return DataFramePair(df, df_secondary)

def mess_data(data: Union[pd.DataFrame, DataFramePair], error_lookup: pd.DataFrame, 
              add_counting_dups: bool = False, verbose: bool = True) -> Union[pd.DataFrame, DataFramePair]:
    """
    Introduce errors into the data based on the error lookup table.
    
    Args:
        data: DataFrame or DataFramePair to introduce errors into
        error_lookup: DataFrame containing error specifications
        add_counting_dups: Whether to add counting duplicates
        verbose: Whether to print progress messages
        
    Returns:
        Data with introduced errors
    """
    if isinstance(data, DataFramePair):
        return _mess_data_pair(data, error_lookup, add_counting_dups, verbose)
    else:
        return _mess_data_frame(data, error_lookup, add_counting_dups, verbose)

def _mess_data_frame(df: pd.DataFrame, error_lookup: pd.DataFrame, 
                    add_counting_dups: bool = False, verbose: bool = True) -> pd.DataFrame:
    """Implementation of mess_data for single DataFrames."""
    n = len(df) if not add_counting_dups else add_counting_dups
    df = df.copy()
    
    # Initialize error record if not present
    if not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
    
    for _, row in error_lookup.iterrows():
        error_function = row['error']
        if verbose:
            print(f"\nApplying error function: {error_function}")
        
        # Calculate number of errors
        e = row['amount']
        if e < 1:
            e = int(np.ceil(e * n))
            
        # Get column names
        col_names = row['columns']
        if isinstance(col_names, str):
            col_names = [col.strip() for col in col_names.split(',') if col.strip()]
        
        # Prepare arguments
        args = {
            'df': df,
            'n_errors': e,
            'col_names': col_names
        }
            
        # Add additional arguments if specified
        if pd.notna(row.get('args')):
            args.update(row['args'])
            
        # Apply error function
        if error_function in ERROR_FUNCTIONS:
            df = ERROR_FUNCTIONS[error_function](**args)
            
        if verbose and hasattr(df, 'error_record'):
            print(df.error_record.to_dataframe().tail())
            
    return df

def _mess_data_pair(df_pair: DataFramePair, error_lookup: pd.DataFrame,
                    add_counting_dups: bool = False, verbose: bool = True) -> DataFramePair:
    """Implementation of mess_data for DataFramePair objects."""
    n = len(df_pair.df_original)
    
    # Handle duplicates separately
    dup_specs = error_lookup[error_lookup['error'] == 'add_duplicates']
    if not dup_specs.empty:
        e = dup_specs.iloc[0]['amount']
        if e < 1:
            e = int(np.ceil(e * n))
        counting_dups = n + e if add_counting_dups else False
    else:
        counting_dups = add_counting_dups
        
    # Process secondary DataFrame
    df_pair.df_secondary = _mess_data_frame(
        df_pair.df_secondary,
        error_lookup[error_lookup['error'] != 'add_duplicates'],
        add_counting_dups=counting_dups,
        verbose=verbose
    )
    
    # Handle duplicates if specified
    if not dup_specs.empty:
        # Note: add_duplicates function needs to be implemented
        df_pair = add_duplicates(df_pair, e)
        
    return df_pair

def convert_cols(df: pd.DataFrame, types: Dict[str, str]) -> pd.DataFrame:
    """
    Convert DataFrame columns to specified types.
    
    Args:
        df: DataFrame to convert
        types: Dictionary mapping column names to their desired types
        
    Returns:
        DataFrame with converted column types
    """
    df = df.copy()
    for col, type_ in types.items():
        if type_ == 'character':
            df[col] = df[col].astype(str)
        elif type_ == 'numeric':
            df[col] = pd.to_numeric(df[col], errors='coerce')
        elif type_ == 'factor':
            df[col] = df[col].astype('category')
    return df 

class ErrorGenerator:
    """Class for managing error generation in datasets."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the error generator.
        
        Args:
            df: Input DataFrame to introduce errors into
        """
        self.original_df = df.copy()
        self.modified_df = df.copy()
        self.error_record = ErrorRecord()
        
        # Add error record to modified DataFrame
        self.modified_df.error_record = self.error_record
        
        # Ensure id column exists
        if 'id' not in self.modified_df.columns:
            self.modified_df['id'] = range(1, len(self.modified_df) + 1)
            self.original_df['id'] = self.modified_df['id'].copy()
    
    def add_errors(self, error_specs: pd.DataFrame, verbose: bool = True) -> None:
        """
        Add errors based on specifications.
        
        Args:
            error_specs: DataFrame containing error specifications
            verbose: Whether to print progress messages
        """
        self.modified_df = mess_data(self.modified_df, error_specs, verbose=verbose)
        self.error_record = self.modified_df.error_record
    
    def get_original(self) -> pd.DataFrame:
        """Get the original DataFrame."""
        return self.original_df.copy()
    
    def get_modified(self) -> pd.DataFrame:
        """Get the modified DataFrame."""
        return self.modified_df.copy()
    
    def get_error_record(self) -> pd.DataFrame:
        """Get the error record as a DataFrame."""
        return self.error_record.to_dataframe()
    
    @staticmethod
    def list_error_types() -> Dict[str, str]:
        """
        List available error types and their descriptions.
        
        Returns:
            Dictionary mapping error types to their descriptions
        """
        return {
            'indel': 'Character-level insertions/deletions',
            'repl': 'Character-level replacements',
            'tpose': 'Character-level transpositions',
            'to_nickname': 'Convert names to nicknames',
            'to_realname': 'Convert nicknames to real names',
            'invert_nick_realnames': 'Invert nickname/real name pairs',
            'name_suffix': 'Add name suffixes',
            'first_letter_abbreviate': 'Abbreviate to first letter',
            'blanks_to_hyphens': 'Replace spaces with hyphens',
            'hyphens_to_blanks': 'Replace hyphens with spaces',
            'missing': 'Set values to missing',
            'swap': 'Swap values between fields',
            'married_name_change': 'Simulate married name changes',
            'duplicate': 'Add duplicate records',
            'twins': 'Generate twin records',
            'date_month_swap': 'Swap date components',
            'date_transpose': 'Transpose date components',
            'date_replace': 'Replace date components'
        }

def generate_errors(df: pd.DataFrame, error_specs: pd.DataFrame, verbose: bool = True) -> tuple[pd.DataFrame, ErrorRecord]:
    """
    Convenience function to generate errors in a DataFrame.
    
    Args:
        df: Input DataFrame
        error_specs: DataFrame containing error specifications
        verbose: Whether to print progress messages
        
    Returns:
        Tuple of (modified DataFrame, error record)
    """
    generator = ErrorGenerator(df)
    generator.add_errors(error_specs, verbose=verbose)
    return generator.get_modified(), generator.error_record 