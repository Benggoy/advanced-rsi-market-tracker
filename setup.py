"""
Setup configuration for Advanced RSI Market Tracker.
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="advanced-rsi-market-tracker",
    version="1.0.0",
    author="Advanced RSI Tracker Team",
    author_email="contact@rsitracker.com",
    description="A comprehensive RSI tracking and analysis system with real-time market data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Benggoy/advanced-rsi-market-tracker",
    project_urls={
        "Bug Tracker": "https://github.com/Benggoy/advanced-rsi-market-tracker/issues",
        "Documentation": "https://github.com/Benggoy/advanced-rsi-market-tracker/wiki",
        "Source Code": "https://github.com/Benggoy/advanced-rsi-market-tracker",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "alerts": [
            "twilio>=8.5.0",
        ],
        "advanced": [
            "ta-lib>=0.4.25",
            "plotly>=5.15.0",
            "streamlit>=1.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rsi-tracker=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yml", "*.yaml"],
    },
    keywords=[
        "rsi",
        "relative strength index",
        "technical analysis",
        "trading",
        "stocks",
        "cryptocurrency",
        "market data",
        "financial analysis",
        "algorithmic trading",
        "investment",
    ],
    zip_safe=False,
)