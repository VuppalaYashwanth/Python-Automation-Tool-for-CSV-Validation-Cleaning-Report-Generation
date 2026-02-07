"""
CSV/Excel Validation and Cleaning Tool
Main CLI entry point
"""

import argparse
import pandas as pd
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List

# Import our modules
from validator import DataValidator
from cleaner import DataCleaner
from reporter import Reporter

# Try to import colorama for colored output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False


class CSVValidationTool:
    """Main tool class for CSV/Excel validation and cleaning"""
    
    def __init__(self, args):
        self.args = args
        self.validator = DataValidator()
        self.cleaner = DataCleaner()
        self.reporter = Reporter()
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging"""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'tool.log'
        
        # Configure logging
        log_level = logging.DEBUG if self.args.verbose else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout) if self.args.verbose else logging.NullHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("=" * 80)
        self.logger.info("CSV Validation Tool Started")
        self.logger.info("=" * 80)
    
    def run(self):
        """Main execution method"""
        try:
            self.print_header()
            
            # Get input files
            input_files = self.get_input_files()
            
            if not input_files:
                self.print_error("No valid CSV/Excel files found in input path")
                return 1
            
            self.print_info(f"Found {len(input_files)} file(s) to process\n")
            
            # Process each file
            results = []
            for i, file_path in enumerate(input_files, 1):
                self.print_info(f"[{i}/{len(input_files)}] Processing: {file_path.name}")
                result = self.process_file(file_path)
                results.append(result)
                print()
            
            # Generate summary
            self.generate_summary(results)
            
            self.print_success("\n✓ Processing complete!")
            self.print_info(f"Reports saved to: {self.args.output}")
            
            return 0
        
        except Exception as e:
            self.print_error(f"Fatal error: {str(e)}")
            self.logger.exception("Fatal error occurred")
            return 1
    
    def get_input_files(self) -> List[Path]:
        """Get list of input files to process"""
        input_path = Path(self.args.input)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input path does not exist: {input_path}")
        
        files = []
        
        if input_path.is_file():
            files.append(input_path)
        elif input_path.is_dir():
            # Find all CSV and Excel files
            for ext in ['*.csv', '*.xlsx', '*.xls']:
                files.extend(input_path.glob(ext))
        
        return sorted(files)
    
    def process_file(self, file_path: Path) -> dict:
        """Process a single file"""
        result = {
            'filename': file_path.name,
            'success': False,
            'validation_passed': False,
            'rows_before': 0,
            'rows_after': 0
        }
        
        try:
            # Load file
            self.print_info(f"  Loading file...")
            df = self.load_file(file_path)
            result['rows_before'] = len(df)
            
            # Validate
            self.print_info(f"  Validating data...")
            required_cols = self.args.required_columns.split(',') if self.args.required_columns else None
            is_valid, messages = self.validator.validate_file(df, file_path.name, required_columns=required_cols)
            
            result['validation_passed'] = is_valid
            
            # Show validation results
            if is_valid:
                self.print_success("  ✓ Validation passed")
            else:
                self.print_warning("  ⚠ Validation passed with warnings")
            
            for msg in messages[:3]:  # Show first 3 messages
                self.print_warning(f"    - {msg}")
            
            if len(messages) > 3:
                self.print_info(f"    ... and {len(messages) - 3} more issues")
            
            # Clean data (unless validate-only mode)
            if not self.args.validate_only:
                self.print_info(f"  Cleaning data...")
                
                df_clean = self.cleaner.clean_data(
                    df,
                    drop_duplicates=self.args.drop_duplicates,
                    fill_missing=self.args.fill_missing,
                    remove_whitespace=True,
                    standardize_columns=True
                )
                
                result['rows_after'] = len(df_clean)
                rows_removed = result['rows_before'] - result['rows_after']
                
                if rows_removed > 0:
                    self.print_info(f"  Removed {rows_removed} rows during cleaning")
                
                # Save cleaned file
                output_dir = Path(self.args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
                
                output_file = output_dir / f"cleaned_{file_path.name}"
                df_clean.to_csv(output_file, index=False)
                self.print_success(f"  ✓ Saved cleaned file: {output_file.name}")
                
                # Generate report
                report_file = output_dir / f"report_{file_path.stem}.txt"
                self.reporter.generate_report(df, df_clean, str(report_file), file_path.name)
                self.print_success(f"  ✓ Saved report: {report_file.name}")
                
                # Generate summary statistics
                stats_file = output_dir / f"stats_{file_path.stem}.txt"
                self.reporter.generate_summary_statistics(df_clean, str(stats_file))
                
            else:
                # Validation-only mode: just generate validation report
                output_dir = Path(self.args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
                
                report_file = output_dir / f"validation_{file_path.stem}.txt"
                self.reporter.generate_report(df, None, str(report_file), file_path.name)
                self.print_success(f"  ✓ Saved validation report: {report_file.name}")
            
            result['success'] = True
            
        except Exception as e:
            self.print_error(f"  ✗ Error processing file: {str(e)}")
            self.logger.exception(f"Error processing {file_path.name}")
            result['error'] = str(e)
        
        return result
    
    def load_file(self, file_path: Path) -> pd.DataFrame:
        """Load CSV or Excel file"""
        encoding = self.args.encoding
        
        if file_path.suffix.lower() == '.csv':
            return pd.read_csv(file_path, encoding=encoding)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    def generate_summary(self, results: List[dict]):
        """Generate overall summary"""
        print("\n" + "=" * 80)
        print("PROCESSING SUMMARY")
        print("=" * 80)
        
        total = len(results)
        successful = sum(1 for r in results if r['success'])
        validated = sum(1 for r in results if r.get('validation_passed', False))
        
        print(f"Total files:        {total}")
        print(f"Successful:         {successful}")
        print(f"Validation passed:  {validated}")
        
        if not self.args.validate_only:
            total_rows_before = sum(r.get('rows_before', 0) for r in results)
            total_rows_after = sum(r.get('rows_after', 0) for r in results)
            total_removed = total_rows_before - total_rows_after
            
            print(f"\nRows processed:     {total_rows_before:,}")
            print(f"Rows after clean:   {total_rows_after:,}")
            print(f"Rows removed:       {total_removed:,}")
        
        print("=" * 80)
    
    def print_header(self):
        """Print tool header"""
        header = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              CSV & EXCEL VALIDATION & CLEANING TOOL                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(header)
    
    def print_success(self, message: str):
        """Print success message"""
        if HAS_COLOR:
            print(Fore.GREEN + message)
        else:
            print(message)
    
    def print_info(self, message: str):
        """Print info message"""
        if HAS_COLOR:
            print(Fore.CYAN + message)
        else:
            print(message)
    
    def print_warning(self, message: str):
        """Print warning message"""
        if HAS_COLOR:
            print(Fore.YELLOW + message)
        else:
            print(message)
    
    def print_error(self, message: str):
        """Print error message"""
        if HAS_COLOR:
            print(Fore.RED + message)
        else:
            print(message)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='CSV/Excel Validation & Cleaning Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Validate and clean a single file
  python main.py --input data.csv --output output/
  
  # Process all files in a directory
  python main.py --input input/ --output output/
  
  # Validate specific columns
  python main.py --input data.csv --output output/ --required-columns "name,email,phone"
  
  # Validation only (no cleaning)
  python main.py --input data.csv --output output/ --validate-only
  
  # Custom missing value handling
  python main.py --input data.csv --output output/ --fill-missing median
        '''
    )
    
    # Required arguments
    parser.add_argument(
        '--input',
        required=True,
        help='Input CSV/Excel file or directory'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output directory for cleaned files and reports'
    )
    
    # Optional arguments
    parser.add_argument(
        '--required-columns',
        help='Comma-separated list of required columns'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate, do not clean data'
    )
    
    parser.add_argument(
        '--drop-duplicates',
        action='store_true',
        default=True,
        help='Remove duplicate rows (default: True)'
    )
    
    parser.add_argument(
        '--fill-missing',
        choices=['mean', 'median', 'mode', 'drop'],
        help='How to handle missing values'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='File encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress'
    )
    
    args = parser.parse_args()
    
    # Run the tool
    tool = CSVValidationTool(args)
    exit_code = tool.run()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
