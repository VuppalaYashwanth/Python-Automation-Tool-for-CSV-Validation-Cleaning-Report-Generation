"""
Data Validation Module
Validates CSV/Excel file structure, data types, and quality
"""

import pandas as pd
import numpy as np
import logging
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class DataValidator:
    """Validates data files for structure and quality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_report = []
    
    def validate_file(self, df: pd.DataFrame, filename: str, 
                     required_columns: Optional[List[str]] = None,
                     expected_dtypes: Optional[Dict[str, str]] = None) -> Tuple[bool, List[str]]:
        """
        Validate a DataFrame against requirements
        
        Args:
            df: DataFrame to validate
            filename: Name of file being validated
            required_columns: List of required column names
            expected_dtypes: Dictionary of column: expected_type
            
        Returns:
            Tuple of (is_valid, list of error/warning messages)
        """
        errors = []
        warnings = []
        
        self.logger.info(f"Validating file: {filename}")
        
        # Check if DataFrame is empty
        if df.empty:
            errors.append("File is empty (0 rows)")
            self.logger.error(f"{filename}: Empty file")
            return False, errors
        
        # Validate required columns
        if required_columns:
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                errors.append(f"Missing required columns: {', '.join(missing_cols)}")
                self.logger.error(f"{filename}: Missing columns - {missing_cols}")
        
        # Validate data types
        if expected_dtypes:
            for col, expected_type in expected_dtypes.items():
                if col in df.columns:
                    actual_type = str(df[col].dtype)
                    if not self._is_compatible_dtype(actual_type, expected_type):
                        warnings.append(
                            f"Column '{col}' type mismatch: expected {expected_type}, got {actual_type}"
                        )
        
        # Check for duplicate rows
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            warnings.append(f"Found {duplicate_count} duplicate rows ({duplicate_count/len(df)*100:.1f}%)")
            self.logger.warning(f"{filename}: {duplicate_count} duplicate rows found")
        
        # Check for missing values
        missing_summary = self._check_missing_values(df)
        if missing_summary:
            warnings.append(f"Missing values detected:\n{missing_summary}")
        
        # Check for completely empty columns
        empty_cols = df.columns[df.isna().all()].tolist()
        if empty_cols:
            warnings.append(f"Completely empty columns: {', '.join(empty_cols)}")
            self.logger.warning(f"{filename}: Empty columns - {empty_cols}")
        
        # Check for whitespace issues
        whitespace_issues = self._check_whitespace(df)
        if whitespace_issues:
            warnings.append(f"Whitespace issues in columns: {', '.join(whitespace_issues)}")
        
        # Log validation results
        is_valid = len(errors) == 0
        
        if is_valid:
            self.logger.info(f"{filename}: Validation PASSED")
            if warnings:
                for warning in warnings:
                    self.logger.warning(f"{filename}: {warning}")
        else:
            self.logger.error(f"{filename}: Validation FAILED")
            for error in errors:
                self.logger.error(f"{filename}: {error}")
        
        # Store validation report
        self.validation_report.append({
            'filename': filename,
            'rows': len(df),
            'columns': len(df.columns),
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        return is_valid, errors + warnings
    
    def validate_columns(self, df: pd.DataFrame, required_cols: List[str]) -> bool:
        """
        Check if DataFrame has all required columns
        
        Args:
            df: DataFrame to check
            required_cols: List of required column names
            
        Returns:
            True if all required columns exist
        """
        return all(col in df.columns for col in required_cols)
    
    def validate_numeric_column(self, df: pd.DataFrame, column: str, 
                               min_val: Optional[float] = None,
                               max_val: Optional[float] = None) -> Tuple[bool, str]:
        """
        Validate numeric column values
        
        Args:
            df: DataFrame containing the column
            column: Column name to validate
            min_val: Minimum acceptable value
            max_val: Maximum acceptable value
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if column not in df.columns:
            return False, f"Column '{column}' not found"
        
        # Check if column is numeric
        if not pd.api.types.is_numeric_dtype(df[column]):
            return False, f"Column '{column}' is not numeric"
        
        # Check range
        if min_val is not None:
            below_min = (df[column] < min_val).sum()
            if below_min > 0:
                return False, f"Column '{column}' has {below_min} values below {min_val}"
        
        if max_val is not None:
            above_max = (df[column] > max_val).sum()
            if above_max > 0:
                return False, f"Column '{column}' has {above_max} values above {max_val}"
        
        return True, ""
    
    def validate_email_format(self, df: pd.DataFrame, column: str) -> Tuple[bool, int]:
        """
        Validate email addresses in a column
        
        Args:
            df: DataFrame containing the column
            column: Column name with email addresses
            
        Returns:
            Tuple of (all_valid, invalid_count)
        """
        if column not in df.columns:
            return False, 0
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Check non-null values
        non_null_emails = df[column].dropna()
        invalid_count = 0
        
        for email in non_null_emails:
            if not re.match(email_pattern, str(email)):
                invalid_count += 1
        
        return invalid_count == 0, invalid_count
    
    def validate_date_format(self, df: pd.DataFrame, column: str, 
                           date_format: str = '%Y-%m-%d') -> Tuple[bool, int]:
        """
        Validate date format in a column
        
        Args:
            df: DataFrame containing the column
            column: Column name with dates
            date_format: Expected date format
            
        Returns:
            Tuple of (all_valid, invalid_count)
        """
        if column not in df.columns:
            return False, 0
        
        non_null_dates = df[column].dropna()
        invalid_count = 0
        
        for date_val in non_null_dates:
            try:
                datetime.strptime(str(date_val), date_format)
            except ValueError:
                invalid_count += 1
        
        return invalid_count == 0, invalid_count
    
    def get_data_quality_score(self, df: pd.DataFrame) -> int:
        """
        Calculate overall data quality score (0-100)
        
        Args:
            df: DataFrame to score
            
        Returns:
            Quality score from 0-100
        """
        score = 100
        
        # Deduct points for missing values
        missing_percentage = (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
        score -= min(missing_percentage, 30)
        
        # Deduct points for duplicates
        duplicate_percentage = (df.duplicated().sum() / len(df)) * 100
        score -= min(duplicate_percentage, 20)
        
        # Deduct points for empty columns
        empty_cols = df.columns[df.isna().all()].tolist()
        score -= len(empty_cols) * 5
        
        # Deduct points for whitespace issues
        whitespace_cols = self._check_whitespace(df)
        score -= len(whitespace_cols) * 2
        
        return max(0, int(score))
    
    def _is_compatible_dtype(self, actual: str, expected: str) -> bool:
        """Check if actual dtype is compatible with expected"""
        dtype_compatibility = {
            'int': ['int', 'int64', 'int32'],
            'float': ['float', 'float64', 'float32'],
            'string': ['object', 'string'],
            'bool': ['bool'],
            'datetime': ['datetime64']
        }
        
        for key, compatible_types in dtype_compatibility.items():
            if expected.lower().startswith(key):
                return any(ct in actual.lower() for ct in compatible_types)
        
        return actual == expected
    
    def _check_missing_values(self, df: pd.DataFrame) -> str:
        """
        Generate missing values summary
        
        Returns:
            Formatted string with missing value statistics
        """
        missing = df.isna().sum()
        missing = missing[missing > 0]
        
        if len(missing) == 0:
            return ""
        
        summary_lines = []
        for col, count in missing.items():
            percentage = (count / len(df)) * 100
            summary_lines.append(f"  - {col}: {count} ({percentage:.1f}%)")
        
        return "\n".join(summary_lines)
    
    def _check_whitespace(self, df: pd.DataFrame) -> List[str]:
        """
        Check for leading/trailing whitespace in string columns
        
        Returns:
            List of column names with whitespace issues
        """
        whitespace_cols = []
        
        for col in df.select_dtypes(include=['object']).columns:
            # Check if any values have leading/trailing whitespace
            has_whitespace = df[col].astype(str).str.strip() != df[col].astype(str)
            if has_whitespace.any():
                whitespace_cols.append(col)
        
        return whitespace_cols
    
    def get_validation_summary(self) -> str:
        """
        Get formatted summary of all validations performed
        
        Returns:
            Formatted validation summary string
        """
        if not self.validation_report:
            return "No validations performed yet"
        
        summary = []
        summary.append("=" * 80)
        summary.append("VALIDATION SUMMARY")
        summary.append("=" * 80)
        summary.append("")
        
        for report in self.validation_report:
            summary.append(f"File: {report['filename']}")
            summary.append(f"Timestamp: {report['timestamp']}")
            summary.append(f"Rows: {report['rows']:,}")
            summary.append(f"Columns: {report['columns']}")
            summary.append(f"Status: {'✓ PASSED' if report['valid'] else '✗ FAILED'}")
            
            if report['errors']:
                summary.append("\nErrors:")
                for error in report['errors']:
                    summary.append(f"  ✗ {error}")
            
            if report['warnings']:
                summary.append("\nWarnings:")
                for warning in report['warnings']:
                    summary.append(f"  ⚠ {warning}")
            
            summary.append("-" * 80)
            summary.append("")
        
        return "\n".join(summary)


if __name__ == "__main__":
    # Test the validator
    import pandas as pd
    
    # Create sample data
    test_data = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith', 'John Doe', '  Bob  '],
        'email': ['john@example.com', 'invalid-email', 'john@example.com', 'bob@test.com'],
        'age': [30, 25, 30, 150],
        'salary': [50000, 60000, 50000, None]
    })
    
    # Test validation
    validator = DataValidator()
    
    logging.basicConfig(level=logging.INFO)
    
    is_valid, messages = validator.validate_file(
        test_data, 
        'test.csv',
        required_columns=['name', 'email']
    )
    
    print(f"\nValidation Result: {'PASSED' if is_valid else 'FAILED'}")
    print(f"\nMessages:")
    for msg in messages:
        print(f"  {msg}")
    
    print(f"\nData Quality Score: {validator.get_data_quality_score(test_data)}/100")
    
    # Test email validation
    is_valid, invalid_count = validator.validate_email_format(test_data, 'email')
    print(f"\nEmail Validation: {invalid_count} invalid emails found")
    
    print("\n" + validator.get_validation_summary())
