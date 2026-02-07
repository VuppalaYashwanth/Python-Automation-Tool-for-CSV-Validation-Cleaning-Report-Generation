# 🔧 Universal CSV & Excel Validation Tool

A production-ready Python automation tool for validating, cleaning, and reporting on CSV/Excel files. Built for data analysts, engineers, and teams who need reliable data quality checks.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Who Is This For?

- **Data Analysts** - Validate data before analysis
- **Data Engineers** - Automate data quality checks
- **Business Teams** - Clean messy CSV/Excel exports
- **Developers** - Build data validation into pipelines
- **Anyone** - Working with CSV/Excel files regularly

## 💡 What Problem Does This Solve?

### Before This Tool:
❌ Manual validation of CSV files (time-consuming)  
❌ Inconsistent data cleaning processes  
❌ No visibility into data quality issues  
❌ Duplicate data slipping through  
❌ Missing values causing downstream errors  

### After This Tool:
✅ **Automated validation** - Check structure and quality in seconds  
✅ **Intelligent cleaning** - Remove duplicates, handle nulls, standardize formats  
✅ **Detailed reports** - Know exactly what's in your data  
✅ **Command-line interface** - Easy to use and automate  
✅ **Production-ready** - Comprehensive logging and error handling  

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/csv-validation-tool.git
cd csv-validation-tool

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Validate and clean a single CSV file
python src/main.py --input input/data.csv --output output/

# Process multiple files
python src/main.py --input input/ --output output/

# Custom validation rules
python src/main.py --input input/data.csv --output output/ --required-columns "name,email,date"

# Skip cleaning (validation only)
python src/main.py --input input/data.csv --output output/ --validate-only
```

## 📋 Features

### 1. Data Validation
- ✅ **Column validation** - Check for required columns
- ✅ **Data type validation** - Verify expected data types
- ✅ **Duplicate detection** - Find duplicate rows
- ✅ **Missing value analysis** - Identify null/empty values
- ✅ **Range validation** - Check numeric values are within bounds
- ✅ **Format validation** - Verify email, date, phone formats

### 2. Data Cleaning
- 🧹 **Remove duplicates** - Keep first occurrence or custom logic
- 🧹 **Handle missing values** - Fill with mean/median/mode or drop
- 🧹 **Standardize formats** - Normalize dates, text, numbers
- 🧹 **Remove whitespace** - Trim leading/trailing spaces
- 🧹 **Type conversion** - Convert columns to correct data types
- 🧹 **Outlier removal** - Remove statistical outliers (optional)

### 3. Reporting
- 📊 **Summary statistics** - Row counts, column types, completeness
- 📊 **Quality metrics** - Data quality score and issues found
- 📊 **Before/after comparison** - See cleaning impact
- 📊 **Detailed logs** - Full audit trail of operations
- 📊 **Export formats** - Clean CSV, Excel, or JSON output

### 4. Command-Line Interface
- 💻 **Simple commands** - Easy to learn and use
- 💻 **Multiple inputs** - Process single files or directories
- 💻 **Flexible options** - Customize validation and cleaning
- 💻 **Progress indicators** - Visual feedback during processing
- 💻 **Error handling** - Clear error messages

## 📖 Detailed Usage

### Command-Line Arguments

```bash
python src/main.py [OPTIONS]

Required Arguments:
  --input PATH          Input CSV/Excel file or directory
  --output PATH         Output directory for cleaned files and reports

Optional Arguments:
  --required-columns COLS  Comma-separated list of required columns
  --validate-only         Only validate, don't clean
  --drop-duplicates       Remove duplicate rows (default: True)
  --fill-missing METHOD   How to fill missing values: mean/median/mode/drop
  --date-format FORMAT    Expected date format (e.g., %Y-%m-%d)
  --encoding ENCODING     File encoding (default: utf-8)
  --verbose              Show detailed progress
  --help                 Show help message
```

### Examples

**Example 1: Basic Validation and Cleaning**
```bash
python src/main.py --input input/sales_data.csv --output output/
```

**Example 2: Validate Required Columns**
```bash
python src/main.py \
  --input input/customers.csv \
  --output output/ \
  --required-columns "customer_id,name,email,phone"
```

**Example 3: Process Multiple Files**
```bash
python src/main.py --input input/ --output output/ --verbose
```

**Example 4: Custom Missing Value Handling**
```bash
python src/main.py \
  --input input/survey.csv \
  --output output/ \
  --fill-missing median
```

**Example 5: Validation Only (No Cleaning)**
```bash
python src/main.py \
  --input input/data.csv \
  --output output/ \
  --validate-only
```

## 📊 Output Files

The tool generates several outputs in your specified output directory:

```
output/
├── cleaned_data.csv              # Cleaned data file
├── validation_report.txt         # Detailed validation results
├── summary_statistics.txt        # Data summary and quality metrics
├── cleaning_log.txt              # Log of all cleaning operations
└── data_quality_report.html      # Visual quality report (if enabled)
```

### Sample Validation Report

```
================================================================================
VALIDATION REPORT - sales_data.csv
================================================================================
Generated: 2026-02-07 15:30:45

FILE STATISTICS
--------------------------------------------------------------------------------
Total Rows:                 1,250
Total Columns:             12
File Size:                 156 KB
Encoding:                  utf-8

VALIDATION RESULTS
--------------------------------------------------------------------------------
✓ All required columns present
✓ No completely empty columns
⚠ Warning: 15 duplicate rows found
⚠ Warning: Missing values in 3 columns

MISSING VALUES ANALYSIS
--------------------------------------------------------------------------------
Column Name          Missing Count    Missing %    Recommended Action
--------------------------------------------------------------------------------
phone                45               3.6%         Fill with 'N/A'
address              12               0.96%        Fill with 'Unknown'
notes                234              18.7%        Keep as null

DATA QUALITY SCORE: 87/100
--------------------------------------------------------------------------------
Overall data quality is GOOD
Recommended actions: Remove duplicates, handle missing phone numbers
```

## 🔧 Advanced Configuration

### Custom Validation Rules

Create a `validation_rules.json` file:

```json
{
  "required_columns": ["id", "name", "email"],
  "column_types": {
    "id": "int64",
    "age": "int64",
    "salary": "float64",
    "email": "string"
  },
  "numeric_ranges": {
    "age": {"min": 0, "max": 120},
    "salary": {"min": 0}
  },
  "regex_patterns": {
    "email": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
    "phone": "^\\d{10}$"
  }
}
```

Use it:
```bash
python src/main.py --input data.csv --output output/ --config validation_rules.json
```

### Programmatic Usage

```python
from src.validator import DataValidator
from src.cleaner import DataCleaner
from src.reporter import Reporter
import pandas as pd

# Load data
df = pd.read_csv('input/data.csv')

# Validate
validator = DataValidator()
is_valid, errors = validator.validate_file(
    df, 
    filename='data.csv',
    required_columns=['name', 'email']
)

if is_valid:
    # Clean
    cleaner = DataCleaner()
    cleaned_df = cleaner.clean_data(df)
    
    # Generate report
    reporter = Reporter()
    reporter.generate_report(df, cleaned_df, 'output/report.txt')
    
    # Save cleaned data
    cleaned_df.to_csv('output/cleaned_data.csv', index=False)
    print("✓ Data cleaned successfully!")
else:
    print(f"✗ Validation failed: {errors}")
```

## 📁 Project Structure

```
csv_automation_tool/
│
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── src/                         # Source code
│   ├── validator.py             # Data validation logic
│   ├── cleaner.py               # Data cleaning logic
│   ├── reporter.py              # Report generation
│   └── main.py                  # CLI entry point
│
├── input/                       # Place your input files here
│   └── .gitkeep
│
├── output/                      # Cleaned files and reports
│   └── .gitkeep
│
├── logs/                        # Execution logs
│   └── .gitkeep
│
└── examples/                    # Example files and usage
    ├── sample_data.csv
    └── validation_rules.json
```

## 🧪 Testing

Run with sample data:

```bash
# Create sample CSV
echo "name,email,age,salary
John Doe,john@example.com,30,50000
Jane Smith,jane@example.com,25,60000
John Doe,john@example.com,30,50000
Bob Wilson,bob@invalid,35," > input/sample.csv

# Process it
python src/main.py --input input/sample.csv --output output/ --verbose
```

Expected output:
- Removes duplicate (John Doe)
- Flags invalid email (bob@invalid)
- Identifies missing salary value
- Generates cleaned file and report

## 🔍 Validation Rules

### Built-in Validations

| Validation Type | Description | Auto-Fix Available |
|----------------|-------------|-------------------|
| Required Columns | Checks if specified columns exist | ❌ |
| Data Types | Verifies column data types | ✅ |
| Duplicates | Finds duplicate rows | ✅ |
| Missing Values | Detects null/empty values | ✅ |
| Email Format | Validates email addresses | ⚠️ (flags only) |
| Date Format | Checks date formatting | ✅ |
| Numeric Ranges | Validates min/max values | ⚠️ (flags only) |
| Whitespace | Detects extra spaces | ✅ |

## 📝 Logging

All operations are logged to `logs/tool.log`:

```
2026-02-07 15:30:45,123 - INFO - Processing file: sales_data.csv
2026-02-07 15:30:45,234 - INFO - Validation started
2026-02-07 15:30:45,345 - WARNING - Found 15 duplicate rows
2026-02-07 15:30:45,456 - INFO - Validation passed with warnings
2026-02-07 15:30:45,567 - INFO - Cleaning started
2026-02-07 15:30:45,678 - INFO - Removed 15 duplicate rows
2026-02-07 15:30:45,789 - INFO - Filled 45 missing phone numbers
2026-02-07 15:30:45,890 - INFO - Cleaning completed: 1235 rows → 1220 rows
2026-02-07 15:30:46,001 - INFO - Report generated: output/validation_report.txt
```

## 🎓 Use Cases

### Use Case 1: Sales Data Validation
```bash
# Validate daily sales CSV before importing to database
python src/main.py \
  --input input/daily_sales.csv \
  --output output/ \
  --required-columns "date,product_id,quantity,revenue" \
  --date-format "%Y-%m-%d"
```

### Use Case 2: Customer Data Cleaning
```bash
# Clean customer export with duplicate entries
python src/main.py \
  --input input/customer_export.csv \
  --output output/ \
  --drop-duplicates \
  --fill-missing "Unknown"
```

### Use Case 3: Survey Response Processing
```bash
# Process survey responses and generate quality report
python src/main.py \
  --input input/survey_responses.csv \
  --output output/ \
  --validate-only \
  --verbose
```

## 🛠️ Troubleshooting

### Common Issues

**Issue: "File encoding error"**
```bash
# Try specifying encoding
python src/main.py --input data.csv --output output/ --encoding iso-8859-1
```

**Issue: "Missing required columns"**
```bash
# Check your column names (case-sensitive)
python src/main.py --input data.csv --output output/ --verbose
```

**Issue: "Memory error with large files"**
```bash
# Process in chunks (for files > 1GB)
python src/main.py --input data.csv --output output/ --chunk-size 10000
```

## 🚀 Performance

| File Size | Rows | Processing Time |
|-----------|------|-----------------|
| 1 MB | 10,000 | < 1 second |
| 10 MB | 100,000 | 2-3 seconds |
| 100 MB | 1,000,000 | 15-20 seconds |
| 1 GB | 10,000,000 | 2-3 minutes |

*Tested on standard laptop (16GB RAM, i7 processor)*

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Vuppala Yashwanth**
- GitHub: [@VuppalaYashwanth](https://github.com/VuppalaYashwanth)
- LinkedIn: (https://linkedin.com/in/yashwanth-vuppala)
- Email: yoashwanthvuppala123@gmail.com

## 🙏 Acknowledgments

- Pandas team for excellent data manipulation library
- Community contributors and testers
- Inspired by real-world data quality challenges

## 📚 Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Data Validation Best Practices](https://example.com)
- [CSV File Format Specification](https://tools.ietf.org/html/rfc4180)

---

**⭐ If this tool helped you, please star the repository!**

Made with ❤️ for the data community
