"""
Tests for RSI core functionality.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.rsi_tracker.core import RSIAnalyzer, RSITracker, RSISignal


class TestRSIAnalyzer:
    """Test RSI calculation and analysis."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.analyzer = RSIAnalyzer(period=14)
        
        # Create test price data
        np.random.seed(42)
        self.prices = pd.Series([
            100 + np.cumsum(np.random.randn(100) * 0.5)
        ][0])
    
    def test_rsi_calculation_basic(self):
        """Test basic RSI calculation."""
        rsi = self.analyzer.calculate_rsi(self.prices)
        
        # RSI should be between 0 and 100
        valid_rsi = rsi.dropna()
        assert all(0 <= val <= 100 for val in valid_rsi)
        
        # Should have NaN values for the first period
        assert rsi.iloc[:self.analyzer.period].isna().any()
        
        # Should have valid values after the period
        assert not rsi.iloc[self.analyzer.period:].isna().any()
    
    def test_rsi_calculation_ema(self):
        """Test EMA-based RSI calculation."""
        rsi = self.analyzer.calculate_ema_rsi(self.prices)
        
        # RSI should be between 0 and 100
        valid_rsi = rsi.dropna()
        assert all(0 <= val <= 100 for val in valid_rsi)
    
    def test_rsi_edge_cases(self):
        """Test RSI calculation edge cases."""
        # Test with insufficient data
        short_prices = pd.Series([100, 101, 102])
        
        with pytest.raises(ValueError):
            self.analyzer.calculate_rsi(short_prices)
        
        # Test with constant prices (should result in RSI around 50 or NaN)
        constant_prices = pd.Series([100] * 50)
        rsi = self.analyzer.calculate_rsi(constant_prices)
        
        # With constant prices, gains and losses are 0, so RSI should be NaN
        assert rsi.iloc[-1] == 50 or np.isnan(rsi.iloc[-1])
    
    def test_divergence_detection(self):
        """Test RSI divergence detection."""
        # Create test data with a simple pattern
        test_prices = pd.Series(range(1, 51))  # Simple ascending prices
        
        rsi_values = self.analyzer.calculate_rsi(test_prices)
        divergences = self.analyzer.detect_divergence(test_prices, rsi_values)
        
        assert 'bullish' in divergences
        assert 'bearish' in divergences
        assert isinstance(divergences['bullish'], list)
        assert isinstance(divergences['bearish'], list)


class TestRSITracker:
    """Test RSI tracking functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.config = {
            'data_sources': {'preferred_provider': 'demo'},
            'alerts': {'email_enabled': False}
        }
        self.tracker = RSITracker(self.config)
    
    def test_add_remove_symbol(self):
        """Test adding and removing symbols."""
        # Add symbol
        self.tracker.add_symbol('AAPL', '1d', 70, 30)
        
        assert 'AAPL' in self.tracker.tracked_symbols
        assert self.tracker.tracked_symbols['AAPL']['timeframe'] == '1d'
        assert self.tracker.tracked_symbols['AAPL']['overbought'] == 70
        assert self.tracker.tracked_symbols['AAPL']['oversold'] == 30
        
        # Remove symbol
        self.tracker.remove_symbol('AAPL')
        assert 'AAPL' not in self.tracker.tracked_symbols
    
    def test_alert_thresholds(self):
        """Test setting alert thresholds."""
        self.tracker.add_symbol('AAPL')
        self.tracker.set_alert_thresholds('AAPL', 75, 25)
        
        assert self.tracker.tracked_symbols['AAPL']['overbought'] == 75
        assert self.tracker.tracked_symbols['AAPL']['oversold'] == 25
    
    def test_summary_generation(self):
        """Test summary generation."""
        # Add some test symbols
        self.tracker.add_symbol('AAPL')
        self.tracker.add_symbol('GOOGL')
        
        summary = self.tracker.get_summary()
        
        assert 'total_symbols' in summary
        assert 'symbols' in summary
        assert 'alerts' in summary
        assert summary['total_symbols'] == 2
        assert 'AAPL' in summary['symbols']
        assert 'GOOGL' in summary['symbols']
    
    def test_current_rsi_calculation(self):
        """Test current RSI calculation (demo mode)."""
        self.tracker.add_symbol('AAPL')
        rsi = self.tracker.get_current_rsi('AAPL')
        
        # In demo mode, should return a random value between 20-80
        assert rsi is not None
        assert 20 <= rsi <= 80


class TestRSISignal:
    """Test RSI signal data structure."""
    
    def test_signal_creation(self):
        """Test creating RSI signals."""
        signal = RSISignal(
            symbol='AAPL',
            timestamp=datetime.now(),
            rsi_value=75.5,
            signal_type='overbought',
            price=150.25,
            volume=1000000
        )
        
        assert signal.symbol == 'AAPL'
        assert signal.rsi_value == 75.5
        assert signal.signal_type == 'overbought'
        assert signal.price == 150.25
        assert signal.volume == 1000000
        assert isinstance(signal.timestamp, datetime)


if __name__ == '__main__':
    pytest.main([__file__])