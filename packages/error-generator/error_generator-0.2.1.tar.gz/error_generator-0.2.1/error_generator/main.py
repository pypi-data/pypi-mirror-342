"""
Main module for the error generator package.
"""

import pandas as pd
from typing import List, Dict, Tuple, Union, Any

from .base import DataFramePair, ErrorRecord, prep_data, update_error_record, mess_data
from . import edit_distance
from . import nicknames
from . import abbreviations
from . import swaps
from . import file_based
from . import dob

class ErrorGenerator:
    """
    A class to manage the error generation process for a DataFrame.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the ErrorGenerator with a DataFrame.
        
        Args:
            df (pd.DataFrame): The input DataFrame to introduce errors into.
                             Must contain an 'id' column.
        """
        self.df_pair = prep_data(df)
        
    def add_errors(self, error_specs: pd.DataFrame) -> None:
        """
        Add errors to the DataFrame based on specifications.
        
        Args:
            error_specs (pd.DataFrame): DataFrame containing error specifications.
                Required columns:
                - 'error': The type of error to introduce
                - 'amount': Number of errors to introduce
                - 'columns': List of column names to apply errors to
                - 'args': Dictionary of additional arguments for the error function
        """
        self.df_pair = mess_data(self.df_pair, error_specs)
    
    def get_original_df(self) -> pd.DataFrame:
        """Get the original DataFrame."""
        return self.df_pair.df_original
    
    def get_modified_df(self) -> pd.DataFrame:
        """Get the modified DataFrame with introduced errors."""
        return self.df_pair.df_secondary
    
    def get_error_records(self) -> List[Dict[str, Any]]:
        """Get the list of error records."""
        return self.df_pair.df_secondary.error_record.to_dataframe()
    
    @staticmethod
    def list_error_types() -> Dict[str, str]:
        """
        Get a dictionary of available error types and their descriptions.
        
        Returns:
            Dict[str, str]: Dictionary mapping error types to descriptions.
        """
        return {
            'indel': 'Character insertion or deletion errors',
            'repl': 'Character replacement errors',
            'tpose': 'Character transposition errors',
            'nickname': 'Replace names with common nicknames',
            'first_letter_abbreviate': 'Abbreviate to first letter',
            'ch1_to_ch2': 'Replace one character with another',
            'blanks_to_hyphens': 'Replace spaces with hyphens',
            'hyphens_to_blanks': 'Replace hyphens with spaces',
            'swap': 'Swap values between columns',
            'file_based': 'Replace values based on lookup file',
            'dob': 'Date of birth format variations',
            'missing': 'Introduce missing values'
        }

def generate_errors(df: pd.DataFrame, error_specs: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience function to generate errors in one step.
    
    Args:
        df (pd.DataFrame): Input DataFrame to introduce errors into.
        error_specs (pd.DataFrame): Error specifications DataFrame.
    
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Modified DataFrame and error records DataFrame.
    """
    generator = ErrorGenerator(df)
    generator.add_errors(error_specs)
    return generator.get_modified_df(), generator.get_error_records() 