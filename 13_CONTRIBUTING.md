# Contributing to CSV Validation Tool

Thank you for considering contributing to this project!

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if the issue already exists in the Issues tab
2. If not, create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)
   - Sample data if possible (anonymized)

### Suggesting Features

We welcome feature suggestions!

1. Check existing issues and pull requests
2. Create a new issue describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Why this would be useful to others

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear messages (`git commit -am 'Add feature: description'`)
7. Push to your fork (`git push origin feature/your-feature-name`)
8. Create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/csv-validation-tool.git
cd csv-validation-tool

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Keep functions focused and small
- Write self-documenting code

Example:
```python
def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

## Testing

Before submitting a PR:

```bash
# Run existing tests
pytest

# Test with sample data
python src/main.py --input examples/sample.csv --output output/

# Test each module independently
python src/validator.py
python src/cleaner.py
python src/reporter.py
```

## Documentation

- Update README.md for new features
- Add docstrings to new functions
- Update QUICKSTART.md if usage changes
- Include examples for new functionality

## Commit Messages

Write clear, descriptive commit messages:

**Good examples:**
```
Add email validation to validator module
Fix: Handle empty CSV files gracefully
Docs: Update README with new CLI options
```

**Bad examples:**
```
update code
fix bug
changes
```

## Pull Request Process

1. Update README.md with details of changes
2. Update version numbers if applicable
3. Ensure all tests pass
4. Get approval from maintainers
5. Merge will be done by maintainers

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Enforcement

Unacceptable behavior can be reported to [your.email@example.com]. All complaints will be reviewed and investigated.

## Questions?

Feel free to open an issue for any questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make this tool better! 🙏
