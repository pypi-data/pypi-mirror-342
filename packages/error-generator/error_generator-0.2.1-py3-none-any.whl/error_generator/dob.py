import pandas as pd
import numpy as np
from typing import List, Union, Optional
from datetime import datetime, date, timedelta
import calendar
from .base import update_error_record
from .edit_distance import repl, tpose

def gen_birthday_from_age(df: pd.DataFrame, age_col: str, 
                         as_of_year_end: Union[str, int] = "most_recent_year_end") -> pd.DataFrame:
    """
    Generate birthdays based on age.
    
    Args:
        df: DataFrame containing age information
        age_col: Column name containing ages
        as_of_year_end: Year end to calculate birthdays from
        
    Returns:
        DataFrame with added birthday column
    """
    df = df.copy()
    ages = df[age_col].values
    
    # Determine reference year
    today = date.today()
    if as_of_year_end == "most_recent_year_end":
        if today.month == 12 and today.day == 31:
            ref_year = today.year
        else:
            ref_year = today.year - 1
    else:
        ref_year = int(as_of_year_end)
        
    # Generate random dates in reference year
    start_date = date(ref_year - 3, 1, 1)
    end_date = date(ref_year, 12, 31)
    days_range = (end_date - start_date).days
    
    # Generate random birthdays
    random_days = np.random.randint(0, days_range + 1, size=len(ages))
    birthdays = [start_date + timedelta(days=days) for days in random_days]
    
    # Adjust years based on ages
    birthdays = [date(ref_year - age, bday.month, bday.day) 
                for age, bday in zip(ages, birthdays)]
    
    df['bday'] = birthdays
    return df

def valid_days(month: int, year: int) -> List[int]:
    """Get valid days for a given month and year."""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return list(range(1, 32))
    elif month == 2 and calendar.isleap(year):
        return list(range(1, 30))
    elif month == 2:
        return list(range(1, 29))
    else:
        return list(range(1, 31))

def valid_months(day: int, year: int) -> List[int]:
    """Get valid months for a given day and year."""
    if day <= 29 and calendar.isleap(year):
        return list(range(1, 13))
    elif day <= 28:
        return list(range(1, 13))
    elif day <= 30:
        return [1] + list(range(3, 13))
    else:
        return [1, 3, 5, 7, 8, 10, 12]

def date_swap(df: pd.DataFrame, n_errors: int, date_col: str) -> pd.DataFrame:
    """
    Swap day and month in dates.
    
    Args:
        df: DataFrame containing dates
        n_errors: Number of dates to modify
        date_col: Column name containing dates
        
    Returns:
        DataFrame with swapped dates
    """
    df = df.copy()
    
    if len(df) == 1:
        date_val = pd.to_datetime(df[date_col].iloc[0])
        if not pd.isna(date_val) and date_val.day > 12:
            print("Warning: Not enough candidate dates found")
            return df
            
        old_date = date_val
        new_date = date(old_date.year, old_date.day, old_date.month)
        df.loc[0, date_col] = new_date
        
        update_error_record(df,
                          [df['id'].iloc[0]],
                          date_col,
                          'date_month_swap',
                          [old_date],
                          [new_date])
    else:
        dates = pd.to_datetime(df[date_col])
        mask = (dates.dt.day < 13) & (dates.dt.month != dates.dt.day)
        potential_candidates = df[mask]
        
        if len(potential_candidates) < n_errors:
            print(f"Warning: Not enough candidate dates found. Using {len(potential_candidates)} dates.")
            n_errors = len(potential_candidates)
            
        candidate_ids = np.random.choice(potential_candidates['id'].values, size=n_errors, replace=False)
        mask = df['id'].isin(candidate_ids)
        
        old_dates = pd.to_datetime(df.loc[mask, date_col])
        new_dates = [date(d.year, d.day, d.month) for d in old_dates]
        df.loc[mask, date_col] = new_dates
        
        update_error_record(df,
                          candidate_ids.tolist(),
                          date_col,
                          'date_month_swap',
                          old_dates.tolist(),
                          new_dates)
        
    return df

def date_transpose(df: pd.DataFrame, n_errors: int, date_col: str, token: str = "year") -> pd.DataFrame:
    """
    Transpose digits in dates.
    
    Args:
        df: DataFrame containing dates
        n_errors: Number of dates to modify
        date_col: Column name containing dates
        token: Part of date to transpose ('year', 'month', or 'day')
        
    Returns:
        DataFrame with transposed dates
    """
    df = df.copy()
    dates = pd.to_datetime(df[date_col])
    
    if token == "year":
        # Transpose last two digits of year
        years = dates.dt.year.astype(str)
        mask = years.str[2] != years.str[3]
        candidates = df[mask]
        
        if len(candidates) < n_errors:
            print(f"Warning: Not enough candidate dates found. Using {len(candidates)} dates.")
            n_errors = len(candidates)
            
        candidate_ids = np.random.choice(candidates['id'].values, size=n_errors, replace=False)
        mask = df['id'].isin(candidate_ids)
        
        old_dates = dates[mask]
        new_years = [int(f"{y[:2]}{y[3]}{y[2]}{y[4]}") for y in old_dates.dt.year.astype(str)]
        new_dates = [date(y, d.month, d.day) for y, d in zip(new_years, old_dates)]
        
        df.loc[mask, date_col] = new_dates
        
        update_error_record(df,
                          candidate_ids.tolist(),
                          date_col,
                          'date_transpose_year',
                          old_dates.tolist(),
                          new_dates)
                          
    elif token == "day":
        # Transpose digits in day
        transposable_days = [1, 2, 10, 12, 20, 21, 30, 31]
        mask = (dates.dt.day.isin(transposable_days) |
               ((dates.dt.month != 2) & dates.dt.day.isin([3] + transposable_days)) |
               (dates.dt.month.isin([1, 3, 5, 7, 8, 10, 12]) & 
                dates.dt.day.isin([13] + transposable_days)))
                
        candidates = df[mask]
        
        if len(candidates) < n_errors:
            print(f"Warning: Not enough transposable dates found. Using {len(candidates)} dates.")
            n_errors = len(candidates)
            
        candidate_ids = np.random.choice(candidates['id'].values, size=n_errors, replace=False)
        mask = df['id'].isin(candidate_ids)
        
        old_dates = dates[mask]
        new_days = [int(tpose(f"{d:02d}")) for d in old_dates.dt.day]
        new_dates = [date(d.year, d.month, nd) for d, nd in zip(old_dates, new_days)]
        
        df.loc[mask, date_col] = new_dates
        
        update_error_record(df,
                          candidate_ids.tolist(),
                          date_col,
                          'date_transpose_day',
                          old_dates.tolist(),
                          new_dates)
                          
    return df

def date_replace(df: pd.DataFrame, n_errors: int, date_col: str, token: str = "year") -> pd.DataFrame:
    """
    Replace digits in dates.
    
    Args:
        df: DataFrame containing dates
        n_errors: Number of dates to modify
        date_col: Column name containing dates
        token: Part of date to replace ('year', 'month', or 'day')
        
    Returns:
        DataFrame with replaced dates
    """
    df = df.copy()
    
    if len(df) < n_errors:
        print(f"Warning: Not enough candidates for date replaces found. Using {len(df)} dates.")
        n_errors = len(df)
        
    candidate_ids = np.random.choice(df['id'].values, size=n_errors, replace=False)
    mask = df['id'].isin(candidate_ids)
    dates = pd.to_datetime(df.loc[mask, date_col])
    
    if token == "year":
        # Replace last two digits of year
        old_dates = dates.copy()
        years = dates.dt.year.astype(str)
        new_years = [int(f"{y[:2]}{repl(y[2:], list('0123456789'))}") for y in years]
        new_dates = [date(y, d.month, d.day) for y, d in zip(new_years, dates)]
        
    elif token == "month":
        # Replace month with valid alternative
        old_dates = dates.copy()
        new_dates = []
        for d in dates:
            valid_months_list = valid_months(d.day, d.year)
            new_month = np.random.choice([m for m in valid_months_list if m != d.month])
            new_dates.append(date(d.year, new_month, d.day))
            
    else:  # token == "day"
        # Replace day with valid alternative
        old_dates = dates.copy()
        new_dates = []
        for d in dates:
            valid_days_list = valid_days(d.month, d.year)
            day_str = f"{d.day:02d}"
            new_day = int(repl(day_str, list('0123456789')))
            new_day = min(max(valid_days_list), new_day)
            new_dates.append(date(d.year, d.month, new_day))
            
    df.loc[mask, date_col] = new_dates
    
    update_error_record(df,
                       candidate_ids.tolist(),
                       date_col,
                       f'date_replace_{token}',
                       old_dates.tolist(),
                       new_dates)
    
    return df 