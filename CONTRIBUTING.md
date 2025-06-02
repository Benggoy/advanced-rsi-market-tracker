# Contributing to Advanced RSI Market Tracker

Thank you for your interest in contributing to the Advanced RSI Market Tracker! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of technical analysis and RSI indicators

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/advanced-rsi-market-tracker.git
   cd advanced-rsi-market-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Install development dependencies**
   ```bash
   pip install pytest pytest-cov black flake8 mypy pre-commit
   ```

5. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting: `black .`
- Use flake8 for linting: `flake8 .`
- Use mypy for type checking: `mypy src/`

### Testing

- Write tests for all new functionality
- Maintain test coverage above 80%
- Run tests with: `pytest tests/`
- Run tests with coverage: `pytest tests/ --cov=src/`

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tool changes

Examples:
```
feat(core): add RSI divergence detection
fix(alerts): resolve email notification bug
docs(readme): update installation instructions
```

## 🛠️ Types of Contributions

### 🐛 Bug Reports

When filing a bug report, please include:

- **Clear description** of the issue
- **Steps to reproduce** the bug
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages** or logs if applicable

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear description of what you expected to happen.

**Environment:**
- OS: [e.g. Windows 10, macOS 12.1]
- Python Version: [e.g. 3.9.7]
- Package Version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### 💡 Feature Requests

For feature requests:

- **Explain the use case** and why it's valuable
- **Describe the proposed solution**
- **Consider implementation complexity**
- **Check existing issues** to avoid duplicates

### 🔧 Code Contributions

#### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   pytest tests/
   flake8 .
   black --check .
   mypy src/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): add your feature"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use a clear, descriptive title
   - Fill out the PR template
   - Link related issues
   - Request review from maintainers

#### Pull Request Guidelines

- **Keep PRs focused** - one feature or fix per PR
- **Write clear descriptions** of what changed and why
- **Include tests** for new functionality
- **Update documentation** when necessary
- **Ensure CI passes** before requesting review

## 📋 Project Areas

### High Priority Areas

- **Real-time data integration** improvements
- **Performance optimizations** for large datasets
- **Additional technical indicators** beyond RSI
- **Mobile app development** (React Native/Flutter)
- **Machine learning** integration for predictions

### Technical Areas

- **Backend/Core**
  - RSI calculation algorithms
  - Data fetching and caching
  - Alert system improvements
  - Database integration

- **Frontend/UI**
  - Web dashboard (React/Vue.js)
  - Charting and visualization
  - Mobile responsive design
  - User experience improvements

- **DevOps/Infrastructure**
  - Docker containerization
  - CI/CD pipeline improvements
  - Cloud deployment scripts
  - Monitoring and logging

- **Documentation**
  - API documentation
  - User guides and tutorials
  - Code comments and docstrings
  - Example implementations

## 🧪 Testing Guidelines

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Performance Tests**: Test with large datasets

### Test Structure

```python
# tests/test_feature.py
import pytest
from src.rsi_tracker.core import RSIAnalyzer

class TestRSIAnalyzer:
    def setup_method(self):
        \"\"\"Setup test fixtures.\"\"\"
        self.analyzer = RSIAnalyzer()
    
    def test_calculate_rsi_basic(self):
        \"\"\"Test basic RSI calculation.\"\"\"
        # Arrange
        prices = [100, 101, 102, 101, 100]
        
        # Act
        result = self.analyzer.calculate_rsi(prices)
        
        # Assert
        assert result is not None
        assert 0 <= result <= 100
```

## 📚 Documentation

### Code Documentation

- Use Google-style docstrings
- Document all public methods and classes
- Include examples in docstrings when helpful
- Keep comments clear and concise

Example:
```python
def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (RSI).
    
    Args:
        prices (pd.Series): Series of closing prices
        period (int, optional): RSI calculation period. Defaults to 14.
    
    Returns:
        pd.Series: RSI values between 0 and 100
        
    Raises:
        ValueError: If insufficient data points provided
        
    Example:
        >>> analyzer = RSIAnalyzer()
        >>> rsi = analyzer.calculate_rsi(price_series)
        >>> print(f"Current RSI: {rsi.iloc[-1]:.2f}")
    """
```

## 🤝 Community Guidelines

### Code of Conduct

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Provide constructive feedback**
- **Focus on the code**, not the person
- **Assume good intentions**

### Communication

- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Use GitHub Issues for bugs and features
- **Pull Requests**: Use for code contributions
- **Documentation**: Keep README and docs updated

## 🏷️ Release Process

### Versioning

We use Semantic Versioning (semver):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality
- **PATCH**: Backward-compatible bug fixes

### Release Steps

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release PR
4. Tag release after merge
5. Automated CI/CD handles publishing

## 📞 Getting Help

- **Documentation**: Check the Wiki and README
- **Issues**: Search existing issues first
- **Discussions**: Use GitHub Discussions for questions
- **Email**: contact@rsitracker.com for sensitive matters

## 🙏 Recognition

Contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page
- Special mentions for significant contributions

Thank you for contributing to Advanced RSI Market Tracker! 🚀