"""
Report Generation Module
Generates comprehensive reports on data validation and cleaning
"""

import pandas as pd
import logging
from typing import Optional, Dict, List
from datetime import datetime
from pathlib import Path


class Reporter:
    """Generates validation and cleaning reports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_report(self, original_df: pd.DataFrame, 
                       cleaned_df: Optional[pd.DataFrame] = None,
                       output_path: str = 'output/report.txt',
                       filename: str = 'data.csv') -> str:
        """
        Generate comprehensive data quality report
        
        Args:
            original_df: Original DataFrame before cleaning
            cleaned_df: DataFrame after cleaning (optional)
            output_path: Path to save report
            filename: Name of the data file
            
        Returns:
            Path to generated report
        """
        self.logger.info(f"Generating report for {filename}")
        
        report_lines = []
        
        # Header
        report_lines.extend(self._generate_header(filename))
        
        # File statistics
        report_lines.extend(self._generate_file_stats(original_df, filename))
        
        # Data quality summary
        report_lines.extend(self._generate_quality_summary(original_df))
        
        # Column analysis
        report_lines.extend(self._generate_column_analysis(original_df))
        
        # Missing values analysis
        report_lines.extend(self._generate_missing_analysis(original_df))
        
        # Duplicate analysis
        report_lines.extend(self._generate_duplicate_analysis(original_df))
        
        # If cleaned data provided, show before/after comparison
        if cleaned_df is not None:
            report_lines.extend(self._generate_cleaning_comparison(original_df, cleaned_df))
        
        # Recommendations
        report_lines.extend(self._generate_recommendations(original_df))
        
        # Footer
        report_lines.extend(self._generate_footer())
        
        # Write report to file
        report_content = '\n'.join(report_lines)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        self.logger.info(f"Report saved to: {output_path}")
        
        return str(output_file)
    
    def generate_summary_statistics(self, df: pd.DataFrame, 
                                   output_path: str = 'output/summary_stats.txt') -> str:
        """
        Generate summary statistics report
        
        Args:
            df: DataFrame to analyze
            output_path: Path to save statistics
            
        Returns:
            Path to generated statistics file
        """
        summary_lines = []
        
        summary_lines.append("=" * 80)
        summary_lines.append("SUMMARY STATISTICS")
        summary_lines.append("=" * 80)
        summary_lines.append("")
        
        # Numeric columns statistics
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary_lines.append("Numeric Columns:")
            summary_lines.append("-" * 80)
            
            stats_df = df[numeric_cols].describe()
            summary_lines.append(stats_df.to_string())
            summary_lines.append("")
        
        # Categorical columns statistics
        categorical_cols = df.select_dtypes(include=['object']).columns
        if len(categorical_cols) > 0:
            summary_lines.append("Categorical Columns:")
            summary_lines.append("-" * 80)
            
            for col in categorical_cols[:5]:  # Limit to first 5
                value_counts = df[col].value_counts().head(10)
                summary_lines.append(f"\n{col}:")
                summary_lines.append(value_counts.to_string())
            
            summary_lines.append("")
        
        # Write to file
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_lines))
        
        return str(output_file)
    
    def _generate_header(self, filename: str) -> List[str]:
        """Generate report header"""
        lines = []
        lines.append("=" * 80)
        lines.append("DATA QUALITY VALIDATION REPORT")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"File: {filename}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        return lines
    
    def _generate_file_stats(self, df: pd.DataFrame, filename: str) -> List[str]:
        """Generate file statistics section"""
        lines = []
        lines.append("FILE STATISTICS")
        lines.append("-" * 80)
        lines.append(f"Total Rows:          {len(df):,}")
        lines.append(f"Total Columns:       {len(df.columns)}")
        
        # Memory usage
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        lines.append(f"Memory Usage:        {memory_usage:.2f} MB")
        
        lines.append("")
        return lines
    
    def _generate_quality_summary(self, df: pd.DataFrame) -> List[str]:
        """Generate data quality summary"""
        lines = []
        lines.append("DATA QUALITY SUMMARY")
        lines.append("-" * 80)
        
        # Calculate quality metrics
        total_cells = len(df) * len(df.columns)
        missing_cells = df.isna().sum().sum()
        duplicate_rows = df.duplicated().sum()
        
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        uniqueness = ((len(df) - duplicate_rows) / len(df)) * 100 if len(df) > 0 else 100
        
        # Overall quality score
        quality_score = int((completeness + uniqueness) / 2)
        
        lines.append(f"Completeness:        {completeness:.2f}%")
        lines.append(f"Uniqueness:          {uniqueness:.2f}%")
        lines.append(f"Overall Score:       {quality_score}/100")
        
        # Quality assessment
        if quality_score >= 90:
            assessment = "EXCELLENT"
        elif quality_score >= 75:
            assessment = "GOOD"
        elif quality_score >= 60:
            assessment = "FAIR"
        else:
            assessment = "NEEDS IMPROVEMENT"
        
        lines.append(f"Assessment:          {assessment}")
        lines.append("")
        
        return lines
    
    def _generate_column_analysis(self, df: pd.DataFrame) -> List[str]:
        """Generate column-by-column analysis"""
        lines = []
        lines.append("COLUMN ANALYSIS")
        lines.append("-" * 80)
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            non_null = df[col].count()
            null = df[col].isna().sum()
            unique = df[col].nunique()
            
            lines.append(f"\n{col}:")
            lines.append(f"  Type:        {dtype}")
            lines.append(f"  Non-null:    {non_null:,}")
            lines.append(f"  Null:        {null:,}")
            lines.append(f"  Unique:      {unique:,}")
            
            # For numeric columns, show range
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val = df[col].min()
                max_val = df[col].max()
                mean_val = df[col].mean()
                lines.append(f"  Range:       {min_val} to {max_val}")
                lines.append(f"  Mean:        {mean_val:.2f}")
        
        lines.append("")
        return lines
    
    def _generate_missing_analysis(self, df: pd.DataFrame) -> List[str]:
        """Generate missing values analysis"""
        lines = []
        lines.append("MISSING VALUES ANALYSIS")
        lines.append("-" * 80)
        
        missing = df.isna().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        
        if len(missing) == 0:
            lines.append("✓ No missing values found")
        else:
            lines.append(f"Columns with missing values: {len(missing)}\n")
            lines.append(f"{'Column':<30} {'Missing':<15} {'Percentage'}")
            lines.append("-" * 80)
            
            for col, count in missing.items():
                percentage = (count / len(df)) * 100
                lines.append(f"{col:<30} {count:<15,} {percentage:.2f}%")
        
        lines.append("")
        return lines
    
    def _generate_duplicate_analysis(self, df: pd.DataFrame) -> List[str]:
        """Generate duplicate rows analysis"""
        lines = []
        lines.append("DUPLICATE ANALYSIS")
        lines.append("-" * 80)
        
        duplicate_count = df.duplicated().sum()
        
        if duplicate_count == 0:
            lines.append("✓ No duplicate rows found")
        else:
            duplicate_pct = (duplicate_count / len(df)) * 100
            lines.append(f"⚠ Found {duplicate_count:,} duplicate rows ({duplicate_pct:.2f}%)")
            
            # Show example duplicates
            duplicates = df[df.duplicated(keep=False)]
            if len(duplicates) > 0:
                lines.append("\nExample duplicate rows:")
                lines.append(duplicates.head(5).to_string())
        
        lines.append("")
        return lines
    
    def _generate_cleaning_comparison(self, original_df: pd.DataFrame, 
                                     cleaned_df: pd.DataFrame) -> List[str]:
        """Generate before/after cleaning comparison"""
        lines = []
        lines.append("CLEANING RESULTS")
        lines.append("-" * 80)
        
        lines.append(f"{'Metric':<30} {'Before':<15} {'After':<15} {'Change'}")
        lines.append("-" * 80)
        
        # Rows
        original_rows = len(original_df)
        cleaned_rows = len(cleaned_df)
        row_change = cleaned_rows - original_rows
        lines.append(f"{'Rows':<30} {original_rows:<15,} {cleaned_rows:<15,} {row_change:+,}")
        
        # Columns
        original_cols = len(original_df.columns)
        cleaned_cols = len(cleaned_df.columns)
        col_change = cleaned_cols - original_cols
        lines.append(f"{'Columns':<30} {original_cols:<15} {cleaned_cols:<15} {col_change:+}")
        
        # Missing values
        original_missing = original_df.isna().sum().sum()
        cleaned_missing = cleaned_df.isna().sum().sum()
        missing_change = cleaned_missing - original_missing
        lines.append(f"{'Missing Values':<30} {original_missing:<15,} {cleaned_missing:<15,} {missing_change:+,}")
        
        # Duplicates
        original_dupes = original_df.duplicated().sum()
        cleaned_dupes = cleaned_df.duplicated().sum()
        dupe_change = cleaned_dupes - original_dupes
        lines.append(f"{'Duplicates':<30} {original_dupes:<15,} {cleaned_dupes:<15,} {dupe_change:+,}")
        
        lines.append("")
        return lines
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate data quality recommendations"""
        lines = []
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)
        
        recommendations = []
        
        # Check for duplicates
        if df.duplicated().sum() > 0:
            recommendations.append("• Remove duplicate rows to ensure data uniqueness")
        
        # Check for missing values
        missing_cols = df.columns[df.isna().any()].tolist()
        if missing_cols:
            recommendations.append(f"• Handle missing values in {len(missing_cols)} columns")
        
        # Check for empty columns
        empty_cols = df.columns[df.isna().all()].tolist()
        if empty_cols:
            recommendations.append(f"• Remove {len(empty_cols)} completely empty columns")
        
        # Check for whitespace
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            if (df[col].astype(str).str.strip() != df[col].astype(str)).any():
                recommendations.append("• Trim whitespace from text columns")
                break
        
        # Check for type consistency
        for col in df.select_dtypes(include=['object']).columns:
            try:
                pd.to_numeric(df[col], errors='raise')
                recommendations.append(f"• Consider converting '{col}' to numeric type")
                break
            except:
                pass
        
        if not recommendations:
            lines.append("✓ No major data quality issues detected")
        else:
            for rec in recommendations:
                lines.append(rec)
        
        lines.append("")
        return lines
    
    def _generate_footer(self) -> List[str]:
        """Generate report footer"""
        lines = []
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        return lines


if __name__ == "__main__":
    # Test the reporter
    import pandas as pd
    
    # Create sample data
    test_data = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith', 'John Doe', 'Bob Wilson', None],
        'email': ['john@example.com', 'jane@example.com', 'john@example.com', 'bob@test.com', None],
        'age': [30, 25, 30, 35, None],
        'salary': [50000, 60000, 50000, 70000, 55000],
        'empty_col': [None, None, None, None, None]
    })
    
    # Create cleaned version
    cleaned_data = test_data.drop_duplicates().dropna(subset=['name'])
    cleaned_data = cleaned_data.drop(columns=['empty_col'])
    
    # Generate report
    reporter = Reporter()
    
    logging.basicConfig(level=logging.INFO)
    
    report_path = reporter.generate_report(
        test_data,
        cleaned_data,
        'test_report.txt',
        'sample_data.csv'
    )
    
    print(f"Report generated: {report_path}")
    
    # Also generate summary statistics
    stats_path = reporter.generate_summary_statistics(cleaned_data, 'test_stats.txt')
    print(f"Statistics generated: {stats_path}")
    
    # Show report content
    with open(report_path, 'r') as f:
        print("\n" + f.read())
