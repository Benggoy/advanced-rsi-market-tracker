# Advanced RSI Market Tracker

## Overview

The Advanced RSI Market Tracker is a comprehensive technical analysis tool that monitors Relative Strength Index (RSI) indicators across multiple financial instruments with real-time market data integration.

## Features

### 🎯 Core Functionality
- **Real-time RSI Calculation**: Calculate RSI for any timeframe (1m, 5m, 15m, 1h, 4h, 1d)
- **Multi-Asset Support**: Track stocks, cryptocurrencies, forex, and commodities
- **Custom Alerts**: Set overbought/oversold alerts with email/SMS notifications
- **Historical Analysis**: Backtest RSI strategies with historical data

### 📊 Advanced Analytics
- **RSI Divergence Detection**: Identify bullish and bearish divergences
- **Multi-Timeframe Analysis**: Compare RSI across different timeframes
- **Trend Correlation**: Analyze RSI patterns with price movements
- **Statistical Metrics**: Mean reversion probability, volatility analysis

### 🔔 Alert System
- **Smart Notifications**: Custom thresholds for overbought (>70) and oversold (<30) conditions
- **Trend Alerts**: Notify when RSI crosses key levels or shows divergence
- **Email Integration**: Automated email alerts with detailed analysis
- **Dashboard Notifications**: Real-time browser notifications

### 📈 Visualization
- **Interactive Charts**: Real-time RSI charts with candlestick overlays
- **Heatmaps**: RSI levels across multiple assets
- **Performance Metrics**: Success rate of RSI signals
- **Export Capabilities**: Save charts and data for further analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Benggoy/advanced-rsi-market-tracker.git
   cd advanced-rsi-market-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   ```bash
   cp config/config.example.json config/config.json
   # Edit config.json with your API keys
   ```

## Quick Start

### Basic RSI Tracking
```python
from rsi_tracker import RSITracker

# Initialize tracker
tracker = RSITracker()

# Add symbols to track
tracker.add_symbol('AAPL', timeframe='1h')
tracker.add_symbol('BTC/USD', timeframe='15m')

# Start monitoring
tracker.start_monitoring()
```

### Custom Alerts
```python
# Set custom RSI thresholds
tracker.set_alert('AAPL', overbought=75, oversold=25)

# Enable email notifications
tracker.enable_email_alerts('your-email@example.com')
```

## Configuration

### API Keys Required
- **Alpha Vantage**: For stock market data
- **Binance**: For cryptocurrency data (optional)
- **Twelve Data**: Alternative data provider (optional)

### Email Configuration
- **SMTP Settings**: Configure for email alerts
- **Notification Preferences**: Customize alert frequency

## Usage Examples

### 1. Single Asset Monitoring
```python
from rsi_tracker import RSIAnalyzer

analyzer = RSIAnalyzer('TSLA')
rsi_data = analyzer.get_rsi_history(period=14, timeframe='1d')
print(f"Current RSI: {rsi_data.current_rsi}")
```

### 2. Multi-Asset Dashboard
```python
from dashboard import RSIDashboard

dashboard = RSIDashboard()
dashboard.add_watchlist(['AAPL', 'GOOGL', 'MSFT', 'TSLA'])
dashboard.launch()  # Opens web interface on localhost:8080
```

### 3. Backtesting RSI Strategy
```python
from backtester import RSIBacktester

backtester = RSIBacktester('SPY')
results = backtester.test_strategy(
    start_date='2023-01-01',
    end_date='2024-01-01',
    buy_threshold=30,
    sell_threshold=70
)
print(f"Strategy Return: {results.total_return:.2%}")
```

## Project Structure

```
advanced-rsi-market-tracker/
├── src/
│   ├── rsi_tracker/
│   │   ├── __init__.py
│   │   ├── core.py           # Main RSI calculation engine
│   │   ├── data_fetcher.py   # Market data APIs
│   │   ├── alerts.py         # Notification system
│   │   └── analyzer.py       # Technical analysis
│   ├── dashboard/
│   │   ├── app.py           # Web dashboard
│   │   ├── templates/       # HTML templates
│   │   └── static/          # CSS/JS files
│   └── utils/
│       ├── config.py        # Configuration management
│       └── helpers.py       # Utility functions
├── tests/
│   ├── test_rsi_core.py
│   ├── test_data_fetcher.py
│   └── test_alerts.py
├── config/
│   ├── config.example.json  # Example configuration
│   └── symbols.json         # Default watchlist
├── docs/
│   ├── api_reference.md
│   ├── user_guide.md
│   └── examples/
├── requirements.txt
├── setup.py
└── README.md
```

## API Reference

### RSITracker Class
- `add_symbol(symbol, timeframe)`: Add asset to monitoring
- `remove_symbol(symbol)`: Remove asset from monitoring
- `get_current_rsi(symbol)`: Get latest RSI value
- `set_alert(symbol, overbought, oversold)`: Configure alerts

### RSIAnalyzer Class
- `calculate_rsi(prices, period)`: Calculate RSI for price series
- `detect_divergence(symbol)`: Find RSI divergences
- `get_support_resistance()`: Identify key RSI levels

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src/ --cov-report=html
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

### Version 2.0 (Planned)
- [ ] Machine learning-based RSI prediction
- [ ] Options chain RSI analysis
- [ ] Social sentiment integration
- [ ] Mobile app development
- [ ] Advanced portfolio RSI metrics

### Version 1.1 (In Progress)
- [ ] WebSocket real-time data
- [ ] Advanced charting library
- [ ] Database integration
- [ ] REST API endpoints

## Support

- **Documentation**: [Wiki](https://github.com/Benggoy/advanced-rsi-market-tracker/wiki)
- **Issues**: [GitHub Issues](https://github.com/Benggoy/advanced-rsi-market-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Benggoy/advanced-rsi-market-tracker/discussions)

## Disclaimer

This tool is for educational and informational purposes only. It should not be considered financial advice. Always do your own research and consult with financial professionals before making investment decisions.

---

**⭐ Star this repository if you find it useful!**