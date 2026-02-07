"""
Data Cleaning Module
Cleans and standardizes data based on validation results
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, List, Dict
from datetime import datetime


class DataCleaner:
    """Cleans and standardizes data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cleaning_log = []
    
    def clean_data(self, df: pd.DataFrame, 
                   drop_duplicates: bool = True,
                   fill_missing: Optional[str] = None,
                   remove_whitespace: bool = True,
                   standardize_columns: bool = True) -> pd.DataFrame:
        """
        Clean DataFrame using specified methods
        
        Args:
            df: DataFrame to clean
            drop_duplicates: Remove duplicate rows
            fill_missing: How to handle missing values ('mean', 'median', 'mode', 'drop', or None)
            remove_whitespace: Strip whitespace from string columns
            standardize_columns: Standardize column names
            
        Returns:
            Cleaned DataFrame
        """
        self.logger.info("Starting data cleaning process")
        
        original_rows = len(df)
        df_clean = df.copy()
        
        # Standardize column names
        if standardize_columns:
            df_clean = self._standardize_column_names(df_clean)
        
        # Remove whitespace
        if remove_whitespace:
            df_clean = self._remove_whitespace(df_clean)
        
        # Remove duplicates
        if drop_duplicates:
            df_clean = self._remove_duplicates(df_clean)
        
        # Handle missing values
        if fill_missing:
            df_clean = self._handle_missing_values(df_clean, method=fill_missing)
        
        # Remove empty columns
        df_clean = self._remove_empty_columns(df_clean)
        
        final_rows = len(df_clean)
        rows_removed = original_rows - final_rows
        
        self.logger.info(f"Cleaning completed: {original_rows} rows → {final_rows} rows ({rows_removed} removed)")
        
        return df_clean
    
    def _standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names: lowercase, replace spaces with underscores
        
        Args:
            df: DataFrame with columns to standardize
            
        Returns:
            DataFrame with standardized column names
        """
        original_cols = df.columns.tolist()
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
        
        changed = [f"{orig} → {new}" for orig, new in zip(original_cols, df.columns) if orig != new]
        if changed:
            self.logger.info(f"Standardized {len(changed)} column names")
            self.cleaning_log.append(f"Standardized column names: {', '.join(changed[:5])}")
        
        return df
    
    def _remove_whitespace(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove leading/trailing whitespace from string columns
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with trimmed strings
        """
        string_cols = df.select_dtypes(include=['object']).columns
        cleaned_count = 0
        
        for col in string_cols:
            original = df[col].copy()
            df[col] = df[col].str.strip()
            
            # Count how many values changed
            if not df[col].equals(original):
                cleaned_count += 1
        
        if cleaned_count > 0:
            self.logger.info(f"Removed whitespace from {cleaned_count} columns")
            self.cleaning_log.append(f"Cleaned whitespace in {cleaned_count} columns")
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame, keep: str = 'first') -> pd.DataFrame:
        """
        Remove duplicate rows
        
        Args:
            df: DataFrame to deduplicate
            keep: Which duplicate to keep ('first', 'last', False for drop all)
            
        Returns:
            DataFrame without duplicates
        """
        original_count = len(df)
        df = df.drop_duplicates(keep=keep)
        removed = original_count - len(df)
        
        if removed > 0:
            self.logger.info(f"Removed {removed} duplicate rows")
            self.cleaning_log.append(f"Removed {removed} duplicate rows (kept '{keep}')")
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame, method: str = 'drop') -> pd.DataFrame:
        """
        Handle missing values in DataFrame
        
        Args:
            df: DataFrame with missing values
            method: How to handle ('mean', 'median', 'mode', 'drop', 'forward_fill', 'backward_fill')
            
        Returns:
            DataFrame with missing values handled
        """
        missing_before = df.isna().sum().sum()
        
        if method == 'drop':
            df = df.dropna()
            self.logger.info(f"Dropped {missing_before} rows with missing values")
            self.cleaning_log.append(f"Dropped rows with missing values: {missing_before} rows removed")
        
        elif method == 'mean':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                mean_val = df[col].mean()
                df[col].fillna(mean_val, inplace=True)
            self.logger.info(f"Filled missing numeric values with mean")
            self.cleaning_log.append(f"Filled {missing_before} missing values with mean")
        
        elif method == 'median':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
            self.logger.info(f"Filled missing numeric values with median")
            self.cleaning_log.append(f"Filled {missing_before} missing values with median")
        
        elif method == 'mode':
            for col in df.columns:
                if df[col].isna().any():
                    mode_val = df[col].mode()
                    if len(mode_val) > 0:
                        df[col].fillna(mode_val[0], inplace=True)
            self.logger.info(f"Filled missing values with mode")
            self.cleaning_log.append(f"Filled {missing_before} missing values with mode")
        
        elif method == 'forward_fill':
            df = df.fillna(method='ffill')
            self.logger.info(f"Forward filled missing values")
            self.cleaning_log.append(f"Forward filled {missing_before} missing values")
        
        elif method == 'backward_fill':
            df = df.fillna(method='bfill')
            self.logger.info(f"Backward filled missing values")
            self.cleaning_log.append(f"Backward filled {missing_before} missing values")
        
        return df
    
    def _remove_empty_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove columns that are completely empty
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame without empty columns
        """
        empty_cols = df.columns[df.isna().all()].tolist()
        
        if empty_cols:
            df = df.drop(columns=empty_cols)
            self.logger.info(f"Removed {len(empty_cols)} empty columns: {', '.join(empty_cols)}")
            self.cleaning_log.append(f"Removed empty columns: {', '.join(empty_cols)}")
        
        return df
    
    def remove_outliers(self, df: pd.DataFrame, columns: Optional[List[str]] = None, 
                       method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove statistical outliers from numeric columns
        
        Args:
            df: DataFrame to clean
            columns: Specific columns to check (None = all numeric columns)
            method: Method to use ('iqr' or 'zscore')
            threshold: Threshold for outlier detection
            
        Returns:
            DataFrame without outliers
        """
        df_clean = df.copy()
        
        if columns is None:
            columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        
        original_count = len(df_clean)
        
        if method == 'iqr':
            for col in columns:
                if col in df_clean.columns:
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        
        elif method == 'zscore':
            from scipy import stats
            for col in columns:
                if col in df_clean.columns:
                    z_scores = np.abs(stats.zscore(df_clean[col].dropna()))
                    df_clean = df_clean[(z_scores < threshold)]
        
        removed = original_count - len(df_clean)
        if removed > 0:
            self.logger.info(f"Removed {removed} outlier rows using {method} method")
            self.cleaning_log.append(f"Removed {removed} outliers ({method})")
        
        return df_clean
    
    def convert_data_types(self, df: pd.DataFrame, 
                          type_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Convert columns to specified data types
        
        Args:
            df: DataFrame to convert
            type_mapping: Dictionary of {column: target_type}
            
        Returns:
            DataFrame with converted types
        """
        df_clean = df.copy()
        
        for col, target_type in type_mapping.items():
            if col in df_clean.columns:
                try:
                    if target_type == 'int':
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').astype('Int64')
                    elif target_type == 'float':
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                    elif target_type == 'string':
                        df_clean[col] = df_clean[col].astype(str)
                    elif target_type == 'datetime':
                        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                    elif target_type == 'bool':
                        df_clean[col] = df_clean[col].astype(bool)
                    
                    self.logger.info(f"Converted '{col}' to {target_type}")
                    self.cleaning_log.append(f"Converted '{col}' to {target_type}")
                
                except Exception as e:
                    self.logger.error(f"Failed to convert '{col}' to {target_type}: {str(e)}")
        
        return df_clean
    
    def standardize_date_format(self, df: pd.DataFrame, 
                               date_columns: List[str],
                               input_format: Optional[str] = None,
                               output_format: str = '%Y-%m-%d') -> pd.DataFrame:
        """
        Standardize date format across columns
        
        Args:
            df: DataFrame containing date columns
            date_columns: List of column names with dates
            input_format: Input date format (None = auto-detect)
            output_format: Desired output format
            
        Returns:
            DataFrame with standardized dates
        """
        df_clean = df.copy()
        
        for col in date_columns:
            if col in df_clean.columns:
                try:
                    if input_format:
                        df_clean[col] = pd.to_datetime(df_clean[col], format=input_format)
                    else:
                        df_clean[col] = pd.to_datetime(df_clean[col], infer_datetime_format=True)
                    
                    df_clean[col] = df_clean[col].dt.strftime(output_format)
                    
                    self.logger.info(f"Standardized date format for '{col}'")
                    self.cleaning_log.append(f"Standardized dates in '{col}' to {output_format}")
                
                except Exception as e:
                    self.logger.error(f"Failed to standardize dates in '{col}': {str(e)}")
        
        return df_clean
    
    def get_cleaning_summary(self) -> str:
        """
        Get summary of all cleaning operations performed
        
        Returns:
            Formatted cleaning summary
        """
        if not self.cleaning_log:
            return "No cleaning operations performed"
        
        summary = []
        summary.append("=" * 80)
        summary.append("CLEANING OPERATIONS SUMMARY")
        summary.append("=" * 80)
        summary.append("")
        
        for i, operation in enumerate(self.cleaning_log, 1):
            summary.append(f"{i}. {operation}")
        
        summary.append("")
        summary.append("=" * 80)
        
        return "\n".join(summary)


if __name__ == "__main__":
    # Test the cleaner
    import pandas as pd
    
    # Create sample data with issues
    test_data = pd.DataFrame({
        'Name': ['John Doe  ', '  Jane Smith', 'John Doe  ', 'Bob Wilson'],
        'Email': ['john@example.com', 'jane@example.com', 'john@example.com', 'bob@test.com'],
        'Age': [30, 25, 30, None],
        'Salary': [50000, 60000, 50000, 70000],
        'Empty Col': [None, None, None, None]
    })
    
    print("Original Data:")
    print(test_data)
    print(f"\nShape: {test_data.shape}")
    
    # Clean data
    cleaner = DataCleaner()
    
    logging.basicConfig(level=logging.INFO)
    
    cleaned_data = cleaner.clean_data(
        test_data,
        drop_duplicates=True,
        fill_missing='mean',
        remove_whitespace=True,
        standardize_columns=True
    )
    
    print("\n" + "="*80)
    print("Cleaned Data:")
    print(cleaned_data)
    print(f"\nShape: {cleaned_data.shape}")
    
    print("\n" + cleaner.get_cleaning_summary())
