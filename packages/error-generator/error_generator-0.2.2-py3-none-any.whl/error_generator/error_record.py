import pandas as pd
from typing import List, Union

class ErrorRecord:
    """Class to store information about errors introduced into the dataset."""
    def __init__(self):
        self.id: List[int] = []
        self.field: List[str] = []
        self.error: List[str] = []
        self.before: List[str] = []
        self.after: List[str] = []

    def add_error(self, id_: int, field: str, error: str, before: str, after: str):
        """Add a new error record."""
        self.id.append(id_)
        self.field.append(field)
        self.error.append(error)
        self.before.append(str(before))
        self.after.append(str(after))

    def to_dataframe(self) -> pd.DataFrame:
        """Convert error records to a pandas DataFrame."""
        return pd.DataFrame({
            'id': self.id,
            'field': self.field,
            'error': self.error,
            'before': self.before,
            'after': self.after
        })

class DataFramePair:
    """Class to hold original and secondary dataframes with error tracking."""
    def __init__(self, df_original: pd.DataFrame, df_secondary: pd.DataFrame):
        self.df_original = df_original
        self.df_secondary = df_secondary
        self.error_record = ErrorRecord()

def update_error_record(df: Union[pd.DataFrame, DataFramePair], ids: List[int], field: str, 
                       error: str, before: Union[str, List[str]], after: Union[str, List[str]]) -> None:
    """
    Update the error record with new errors.
    
    Args:
        df: DataFrame or DataFramePair object containing the data and error records
        ids: List of IDs where errors were introduced
        field: Name of the field where errors were introduced
        error: Type of error introduced
        before: Original value(s) before error
        after: Value(s) after error was introduced
    """
    if not isinstance(before, list):
        before = [before] * len(ids)
    if not isinstance(after, list):
        after = [after] * len(ids)
        
    # Initialize error record if not present
    if isinstance(df, pd.DataFrame) and not hasattr(df, 'error_record'):
        df.error_record = ErrorRecord()
        
    for id_, b, a in zip(ids, before, after):
        if isinstance(df, DataFramePair):
            df.error_record.add_error(id_, field, error, b, a)
        else:
            df.error_record.add_error(id_, field, error, b, a) 