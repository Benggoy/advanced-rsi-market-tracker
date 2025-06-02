"""
Core RSI calculation and tracking functionality.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass


@dataclass
class RSISignal:
    """RSI signal data structure."""
    symbol: str
    timestamp: datetime
    rsi_value: float
    signal_type: str  # 'overbought', 'oversold', 'neutral'
    price: float
    volume: Optional[float] = None


class RSIAnalyzer:
    """Advanced RSI calculation and analysis engine."""
    
    def __init__(self, period: int = 14):
        """
        Initialize RSI Analyzer.
        
        Args:
            period (int): RSI calculation period (default: 14)
        """
        self.period = period
        self.logger = logging.getLogger(__name__)
        
    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """
        Calculate RSI using the traditional method.
        
        Args:
            prices (pd.Series): Series of closing prices
            
        Returns:
            pd.Series: RSI values
        """
        if len(prices) < self.period + 1:
            raise ValueError(f"Need at least {self.period + 1} price points")
            
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=self.period).mean()
        avg_losses = losses.rolling(window=self.period).mean()
        
        # Calculate RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_ema_rsi(self, prices: pd.Series) -> pd.Series:
        """
        Calculate RSI using exponential moving average (Wilder's method).
        
        Args:
            prices (pd.Series): Series of closing prices
            
        Returns:
            pd.Series: RSI values using EMA
        """
        delta = prices.diff()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Initialize result series
        rsi_values = pd.Series(index=prices.index, dtype=float)
        
        # Calculate RSI using EMA
        alpha = 1.0 / self.period
        avg_gain = None
        avg_loss = None
        
        for i in range(self.period, len(prices)):
            if i == self.period:
                avg_gain = gains.iloc[1:i+1].mean()
                avg_loss = losses.iloc[1:i+1].mean()
            else:
                avg_gain = alpha * gains.iloc[i] + (1 - alpha) * avg_gain
                avg_loss = alpha * losses.iloc[i] + (1 - alpha) * avg_loss
            
            if avg_loss == 0:
                rsi_values.iloc[i] = 100
            else:
                rs = avg_gain / avg_loss
                rsi_values.iloc[i] = 100 - (100 / (1 + rs))
                
        return rsi_values
    
    def detect_divergence(self, prices: pd.Series, rsi_values: pd.Series, 
                         window: int = 20) -> Dict[str, List[Tuple]]:
        """
        Detect bullish and bearish divergences.
        
        Args:
            prices (pd.Series): Price data
            rsi_values (pd.Series): RSI values
            window (int): Lookback window for divergence detection
            
        Returns:
            Dict: Dictionary with 'bullish' and 'bearish' divergence points
        """
        divergences = {'bullish': [], 'bearish': []}
        
        # Find local peaks and troughs
        price_peaks = self._find_peaks(prices, window)
        price_troughs = self._find_troughs(prices, window)
        rsi_peaks = self._find_peaks(rsi_values, window)
        rsi_troughs = self._find_troughs(rsi_values, window)
        
        # Detect bearish divergence (price higher highs, RSI lower highs)
        for i in range(1, len(price_peaks)):
            curr_price_peak = price_peaks[i]
            prev_price_peak = price_peaks[i-1]
            
            # Find corresponding RSI peaks
            curr_rsi_peak = self._find_nearest_peak(rsi_peaks, curr_price_peak)
            prev_rsi_peak = self._find_nearest_peak(rsi_peaks, prev_price_peak)
            
            if (curr_rsi_peak and prev_rsi_peak and 
                prices.iloc[curr_price_peak] > prices.iloc[prev_price_peak] and
                rsi_values.iloc[curr_rsi_peak] < rsi_values.iloc[prev_rsi_peak]):
                
                divergences['bearish'].append((
                    curr_price_peak, 
                    prices.iloc[curr_price_peak],
                    rsi_values.iloc[curr_rsi_peak]
                ))
        
        # Detect bullish divergence (price lower lows, RSI higher lows)
        for i in range(1, len(price_troughs)):
            curr_price_trough = price_troughs[i]
            prev_price_trough = price_troughs[i-1]
            
            # Find corresponding RSI troughs
            curr_rsi_trough = self._find_nearest_trough(rsi_troughs, curr_price_trough)
            prev_rsi_trough = self._find_nearest_trough(rsi_troughs, prev_price_trough)
            
            if (curr_rsi_trough and prev_rsi_trough and 
                prices.iloc[curr_price_trough] < prices.iloc[prev_price_trough] and
                rsi_values.iloc[curr_rsi_trough] > rsi_values.iloc[prev_rsi_trough]):
                
                divergences['bullish'].append((
                    curr_price_trough,
                    prices.iloc[curr_price_trough],
                    rsi_values.iloc[curr_rsi_trough]
                ))
        
        return divergences
    
    def _find_peaks(self, series: pd.Series, window: int) -> List[int]:
        """Find local peaks in a series."""
        peaks = []
        for i in range(window, len(series) - window):
            if series.iloc[i] == series.iloc[i-window:i+window+1].max():
                peaks.append(i)
        return peaks
    
    def _find_troughs(self, series: pd.Series, window: int) -> List[int]:
        """Find local troughs in a series."""
        troughs = []
        for i in range(window, len(series) - window):
            if series.iloc[i] == series.iloc[i-window:i+window+1].min():
                troughs.append(i)
        return troughs
    
    def _find_nearest_peak(self, peaks: List[int], target: int) -> Optional[int]:
        """Find the nearest peak to a target index."""
        if not peaks:
            return None
        return min(peaks, key=lambda x: abs(x - target))
    
    def _find_nearest_trough(self, troughs: List[int], target: int) -> Optional[int]:
        """Find the nearest trough to a target index."""
        if not troughs:
            return None
        return min(troughs, key=lambda x: abs(x - target))


class RSITracker:
    """Main RSI tracking and monitoring system."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize RSI Tracker.
        
        Args:
            config (Dict, optional): Configuration dictionary
        """
        self.config = config or {}
        self.analyzer = RSIAnalyzer()
        
        # Tracking state
        self.tracked_symbols: Dict[str, Dict] = {}
        self.rsi_history: Dict[str, pd.DataFrame] = {}
        self.active_alerts: Dict[str, Dict] = {}
        
        self.logger = logging.getLogger(__name__)
        
    def add_symbol(self, symbol: str, timeframe: str = '1h', 
                   overbought: float = 70, oversold: float = 30) -> None:
        """
        Add a symbol to track.
        
        Args:
            symbol (str): Trading symbol (e.g., 'AAPL', 'BTC/USD')
            timeframe (str): Data timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
            overbought (float): Overbought threshold
            oversold (float): Oversold threshold
        """
        self.tracked_symbols[symbol] = {
            'timeframe': timeframe,
            'overbought': overbought,
            'oversold': oversold,
            'last_update': None,
            'last_rsi': None
        }
        
        self.logger.info(f"Added {symbol} to tracking with {timeframe} timeframe")
    
    def remove_symbol(self, symbol: str) -> None:
        """Remove a symbol from tracking."""
        if symbol in self.tracked_symbols:
            del self.tracked_symbols[symbol]
            if symbol in self.rsi_history:
                del self.rsi_history[symbol]
            self.logger.info(f"Removed {symbol} from tracking")
    
    def get_current_rsi(self, symbol: str) -> Optional[float]:
        """Get the current RSI value for a symbol."""
        if symbol not in self.tracked_symbols:
            return None
            
        try:
            # For demo purposes, generate a random RSI value
            # In real implementation, this would fetch actual market data
            import random
            rsi_value = random.uniform(20, 80)
            
            # Update tracking state
            self.tracked_symbols[symbol]['last_update'] = datetime.now()
            self.tracked_symbols[symbol]['last_rsi'] = rsi_value
            
            return rsi_value
            
        except Exception as e:
            self.logger.error(f"Error calculating RSI for {symbol}: {e}")
            return None
    
    def update_all_symbols(self) -> Dict[str, float]:
        """Update RSI for all tracked symbols."""
        results = {}
        
        for symbol in self.tracked_symbols:
            rsi = self.get_current_rsi(symbol)
            if rsi is not None:
                results[symbol] = rsi
                self._check_alerts(symbol, rsi)
        
        return results
    
    def _check_alerts(self, symbol: str, current_rsi: float) -> None:
        """Check if any alerts should be triggered."""
        config = self.tracked_symbols[symbol]
        
        signal_type = 'neutral'
        if current_rsi >= config['overbought']:
            signal_type = 'overbought'
        elif current_rsi <= config['oversold']:
            signal_type = 'oversold'
        
        if signal_type != 'neutral':
            # Create RSI signal
            signal = RSISignal(
                symbol=symbol,
                timestamp=datetime.now(),
                rsi_value=current_rsi,
                signal_type=signal_type,
                price=100.0  # Placeholder price
            )
            
            self.logger.info(f"RSI Alert: {symbol} is {signal_type} with RSI {current_rsi:.2f}")
    
    def set_alert_thresholds(self, symbol: str, overbought: float, oversold: float) -> None:
        """Update alert thresholds for a symbol."""
        if symbol in self.tracked_symbols:
            self.tracked_symbols[symbol]['overbought'] = overbought
            self.tracked_symbols[symbol]['oversold'] = oversold
            self.logger.info(f"Updated thresholds for {symbol}: OB={overbought}, OS={oversold}")
    
    def get_summary(self) -> Dict:
        """Get a summary of all tracked symbols and their current state."""
        summary = {
            'total_symbols': len(self.tracked_symbols),
            'symbols': {},
            'alerts': {
                'overbought': 0,
                'oversold': 0,
                'neutral': 0
            }
        }
        
        for symbol, config in self.tracked_symbols.items():
            current_rsi = config.get('last_rsi')
            
            if current_rsi is not None:
                if current_rsi >= config['overbought']:
                    status = 'overbought'
                    summary['alerts']['overbought'] += 1
                elif current_rsi <= config['oversold']:
                    status = 'oversold'
                    summary['alerts']['oversold'] += 1
                else:
                    status = 'neutral'
                    summary['alerts']['neutral'] += 1
            else:
                status = 'unknown'
            
            summary['symbols'][symbol] = {
                'rsi': current_rsi,
                'status': status,
                'timeframe': config['timeframe'],
                'last_update': config['last_update']
            }
        
        return summary
