# RoboMetrics

<div align="center">

![RoboMetrics Logo](assets/robometrics-logo.png)

Advanced analytics for Robot Framework test suites

[![PyPI version](https://badge.fury.io/py/robometrics.svg)](https://badge.fury.io/py/robometrics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

</div>

## 🔍 What is RoboMetrics?

RoboMetrics is an intelligent analyzer for Robot Framework test suites that helps you understand and optimize your test architecture. Using advanced metrics like Shannon Entropy and Jaccard Similarity, it provides actionable insights about test complexity, redundancy, and usage patterns.

### 🚀 Key Features

- **Complexity Analysis**: Measure test complexity using Shannon Entropy to identify tests that need refactoring
- **Redundancy Detection**: Find similar tests using Jaccard Similarity to reduce maintenance overhead
- **Pattern Recognition**: Track keyword usage patterns to optimize test design
- **Suite Structure Analysis**: Get a clear overview of your test organization

### 💡 Why RoboMetrics?

- **Save Time**: Quickly identify problematic tests that need attention
- **Improve Quality**: Ensure balanced test coverage and complexity
- **Data-Driven Decisions**: Make refactoring decisions based on metrics, not gut feeling
- **Simple Integration**: Works with any Robot Framework test suite

## 📦 Installation

```bash
# Via pip
pip install robometrics

# Or from source
git clone https://github.com/ScienceArtist/robometrics.git
cd robometrics
pip install -e .
```

## 🚀 Quick Start

1. Navigate to your Robot Framework test directory:
```bash
cd path/to/your/robot/tests
```

2. Run RoboMetrics:
```bash
robometrics analyze ./
```

3. View the results in `test_analysis_output/analysis_report.json`

## 📊 Understanding the Output

RoboMetrics generates a comprehensive JSON report containing:

### 1. Test Suite Summary
```json
{
    "test_suite_summary": {
        "total_tests": 56,
        "total_keywords": 56,
        "total_suites": 1
    }
}
```

### 2. Complexity Analysis
```json
{
    "complexity_analysis": [
        {
            "Test Keyword": "test_example",
            "Entropy Score": 4.52,
            "Step Count": 23
        }
    ]
}
```

#### Understanding Complexity Scores:
- **Entropy Score** (0-6):
  - > 4.0: Complex test, consider refactoring
  - 2.0-4.0: Moderate complexity
  - < 2.0: Simple test, might need more coverage
- **Step Count**: Number of test steps

### 3. Redundancy Analysis
Identifies test pairs with similarity > 80%:
```json
{
    "redundancy_analysis": [
        {
            "test1": "test_login",
            "test2": "test_login_with_sso",
            "similarity": 0.85
        }
    ]
}
```

## 🛠️ Advanced Usage

### Custom Analysis

```bash
# Analyze specific directory
robometrics analyze path/to/tests --output custom_output.json

# Set custom similarity threshold
robometrics analyze . --similarity-threshold 0.75

# Generate detailed report
robometrics analyze . --verbose
```

### Integration with CI/CD

Add to your GitHub Actions workflow:

```yaml
- name: Run RoboMetrics Analysis
  run: |
    pip install robometrics
    robometrics analyze ./tests --fail-on-complexity 4.5
```

## 📈 Best Practices

1. **Regular Analysis**
   - Run RoboMetrics as part of your CI/CD pipeline
   - Track complexity trends over time

2. **Complexity Management**
   - Keep entropy scores below 4.0
   - Split tests when step count exceeds 25

3. **Redundancy Control**
   - Review tests with similarity > 90%
   - Consider creating shared keywords for common patterns

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- Created by [@ScienceArtist](https://github.com/ScienceArtist)
- Shannon Entropy implementation inspired by [Information Theory](https://en.wikipedia.org/wiki/Shannon_entropy)
- Robot Framework community for inspiration and support

## 📞 Support

- 📫 [Report a bug](https://github.com/ScienceArtist/robometrics/issues)
- 💡 [Request a feature](https://github.com/ScienceArtist/robometrics/issues)
- 📖 [Wiki](https://github.com/ScienceArtist/robometrics/wiki)

---

<div align="center">
Made with ❤️ for the Robot Framework community
</div>
