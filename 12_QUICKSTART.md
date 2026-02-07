# 🚀 Quick Start Guide

Get up and running with the CSV Validation Tool in 3 minutes!

## Step 1: Install (30 seconds)

```bash
# Clone the repository
git clone https://github.com/yourusername/csv-validation-tool.git
cd csv-validation-tool

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Prepare Your Data (30 seconds)

Place your CSV or Excel files in the `input/` directory:

```bash
# Example: Copy your data file
cp /path/to/your/data.csv input/
```

## Step 3: Run the Tool (30 seconds)

```bash
# Basic usage - validate and clean
python src/main.py --input input/data.csv --output output/

# Or process all files in input directory
python src/main.py --input input/ --output output/
```

## Step 4: Check Results (1 minute)

Your cleaned data and reports are in the `output/` directory:

```
output/
├── cleaned_data.csv           # Your cleaned data
├── report_data.txt            # Validation report
└── stats_data.txt             # Summary statistics
```

## Common Use Cases

### Validate Required Columns
```bash
python src/main.py \
  --input input/data.csv \
  --output output/ \
  --required-columns "name,email,phone"
```

### Validation Only (No Cleaning)
```bash
python src/main.py \
  --input input/data.csv \
  --output output/ \
  --validate-only
```

### Custom Missing Value Handling
```bash
python src/main.py \
  --input input/data.csv \
  --output output/ \
  --fill-missing median
```

### Process Multiple Files
```bash
python src/main.py \
  --input input/ \
  --output output/ \
  --verbose
```

## Understanding the Output

### Cleaned CSV File
- Duplicates removed
- Missing values handled
- Whitespace trimmed
- Column names standardized

### Validation Report
Shows:
- Data quality score (0-100)
- Missing values analysis
- Duplicate detection
- Column-by-column analysis
- Recommendations

### Summary Statistics
Contains:
- Descriptive statistics for numeric columns
- Value distributions for categorical columns
- Data completeness metrics

## Next Steps

1. ✅ Read the full [README.md](README.md) for detailed documentation
2. ✅ Customize validation rules in your code
3. ✅ Automate with cron jobs or task schedulers
4. ✅ Integrate into your data pipelines

## Need Help?

- Check [README.md](README.md) for detailed usage
- See `logs/tool.log` for execution details
- Review example files in `examples/` directory

---

**That's it! You're ready to clean your data!** 🎉
