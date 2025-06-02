"""
Data fetching module for various market data sources.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import requests
import time
import logging
from abc import ABC, abstractmethod


class DataProvider(ABC):
    """Abstract base class for data providers."""
    
    @abstractmethod
    def get_historical_data(self, symbol: str, timeframe: str, limit: int) -> Optional[pd.DataFrame]:
        """Fetch historical market data."""
        pass
    
    @abstractmethod
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Fetch real-time market data."""
        pass


class YFinanceProvider(DataProvider):
    """Yahoo Finance data provider using yfinance."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            import yfinance as yf
            self.yf = yf
        except ImportError:
            self.logger.warning("yfinance package not installed. Install with: pip install yfinance")
            self.yf = None
    
    def get_historical_data(self, symbol: str, timeframe: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """Fetch historical data from Yahoo Finance."""
        if not self.yf:
            return None
            
        try:
            # Map timeframes
            interval_map = {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '1h': '1h',
                '4h': '4h',
                '1d': '1d'
            }
            
            if timeframe not in interval_map:
                self.logger.error(f"Unsupported timeframe: {timeframe}")
                return None
            
            ticker = self.yf.Ticker(symbol)
            
            # Determine period based on timeframe and limit
            if timeframe in ['1m', '5m']:
                period = '7d'  # Max for minute data
            elif timeframe in ['15m', '1h']:
                period = '60d'
            else:
                period = '2y'
            
            data = ticker.history(period=period, interval=interval_map[timeframe])
            
            if data.empty:
                self.logger.warning(f"No data received for {symbol}")
                return None
            
            # Convert to standard format
            df = pd.DataFrame({
                'timestamp': data.index,
                'open': data['Open'].values,
                'high': data['High'].values,
                'low': data['Low'].values,
                'close': data['Close'].values,
                'volume': data['Volume'].values
            })
            
            df = df.tail(limit).reset_index(drop=True)
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching data from Yahoo Finance: {e}")
            return None
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Fetch real-time data from Yahoo Finance."""
        if not self.yf:
            return None
            
        try:
            ticker = self.yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'price': info.get('regularMarketPrice', 0),
                'change': info.get('regularMarketChange', 0),
                'change_percent': info.get('regularMarketChangePercent', 0),
                'volume': info.get('regularMarketVolume', 0),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching real-time data: {e}")
            return None


class AlphaVantageProvider(DataProvider):
    """Alpha Vantage data provider."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.logger = logging.getLogger(__name__)
        
    def get_historical_data(self, symbol: str, timeframe: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """Fetch historical data from Alpha Vantage."""
        if not self.api_key:
            self.logger.warning("Alpha Vantage API key not provided")
            return None
            
        try:
            # Map timeframes to Alpha Vantage functions
            function_map = {
                '1d': 'TIME_SERIES_DAILY',
                '1h': 'TIME_SERIES_INTRADAY',
                '15m': 'TIME_SERIES_INTRADAY',
                '5m': 'TIME_SERIES_INTRADAY'
            }
            
            if timeframe not in function_map:
                self.logger.error(f"Unsupported timeframe: {timeframe}")
                return None
            
            params = {
                'function': function_map[timeframe],
                'symbol': symbol,
                'apikey': self.api_key,
                'outputsize': 'full'
            }
            
            if timeframe != '1d':
                params['interval'] = timeframe
            
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            # Parse the response
            if 'Error Message' in data:
                self.logger.error(f"Alpha Vantage error: {data['Error Message']}")
                return None
            
            # Extract time series data
            time_series_key = None
            for key in data.keys():
                if 'Time Series' in key:
                    time_series_key = key
                    break
            
            if not time_series_key:
                self.logger.error("No time series data found")
                return None
            
            ts_data = data[time_series_key]
            
            # Convert to DataFrame
            df_data = []
            for timestamp, values in ts_data.items():
                row = {
                    'timestamp': pd.to_datetime(timestamp),
                    'open': float(values['1. open']),
                    'high': float(values['2. high']),
                    'low': float(values['3. low']),
                    'close': float(values['4. close']),
                    'volume': int(values['5. volume'])
                }
                df_data.append(row)
            
            df = pd.DataFrame(df_data)
            df = df.sort_values('timestamp').tail(limit).reset_index(drop=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error fetching data from Alpha Vantage: {e}")
            return None
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Fetch real-time quote from Alpha Vantage."""
        if not self.api_key:
            return None
            
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': quote['01. symbol'],
                    'price': float(quote['05. price']),
                    'change': float(quote['09. change']),
                    'change_percent': quote['10. change percent'].rstrip('%'),
                    'volume': int(quote['06. volume']),
                    'timestamp': datetime.now()
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching real-time data: {e}")
            return None


class CryptoProvider(DataProvider):
    """Cryptocurrency data provider using public APIs."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.binance_base = "https://api.binance.com/api/v3"
        
    def get_historical_data(self, symbol: str, timeframe: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """Fetch crypto historical data from Binance."""
        try:
            # Convert symbol format (e.g., BTC/USD -> BTCUSDT)
            binance_symbol = symbol.replace('/', '').replace('USD', 'USDT')
            
            # Map timeframes
            interval_map = {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '1h': '1h',
                '4h': '4h',
                '1d': '1d'
            }
            
            if timeframe not in interval_map:
                self.logger.error(f"Unsupported timeframe: {timeframe}")
                return None
            
            url = f"{self.binance_base}/klines"
            params = {
                'symbol': binance_symbol,
                'interval': interval_map[timeframe],
                'limit': limit
            }
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if isinstance(data, dict) and 'code' in data:
                self.logger.error(f"Binance API error: {data.get('msg')}")
                return None
            
            # Convert to DataFrame
            df_data = []
            for kline in data:
                row = {
                    'timestamp': pd.to_datetime(int(kline[0]), unit='ms'),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5])
                }
                df_data.append(row)
            
            return pd.DataFrame(df_data)
            
        except Exception as e:
            self.logger.error(f"Error fetching crypto data: {e}")
            return None
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Fetch real-time crypto data."""
        try:
            binance_symbol = symbol.replace('/', '').replace('USD', 'USDT')
            
            url = f"{self.binance_base}/ticker/24hr"
            params = {'symbol': binance_symbol}
            
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if isinstance(data, dict) and 'code' in data:
                return None
            
            return {
                'symbol': symbol,
                'price': float(data['lastPrice']),
                'change': float(data['priceChange']),
                'change_percent': float(data['priceChangePercent']),
                'volume': float(data['volume']),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching real-time crypto data: {e}")
            return None


class DataFetcher:
    """Main data fetching coordinator."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.providers = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize providers based on config
        self._setup_providers()
    
    def _setup_providers(self):
        """Setup data providers based on configuration."""
        # Yahoo Finance (free, no API key required)
        self.providers['stocks'] = YFinanceProvider()
        
        # Alpha Vantage (requires API key)
        alpha_key = self.config.get('data_sources', {}).get('alpha_vantage_key')
        if alpha_key and alpha_key != "YOUR_ALPHA_VANTAGE_API_KEY":
            self.providers['alpha_vantage'] = AlphaVantageProvider(alpha_key)
        
        # Crypto provider (free)
        self.providers['crypto'] = CryptoProvider()
    
    def get_historical_data(self, symbol: str, timeframe: str, limit: int = 100) -> Optional[pd.DataFrame]:
        """Fetch historical data using the best available provider."""
        # Determine asset type and provider
        if '/' in symbol or symbol.upper().endswith(('USDT', 'BTC', 'ETH')):
            # Cryptocurrency
            provider = self.providers.get('crypto')
        else:
            # Stock/traditional asset
            provider = self.providers.get('stocks')
            
            # Fallback to Alpha Vantage if available
            if not provider and 'alpha_vantage' in self.providers:
                provider = self.providers['alpha_vantage']
        
        if not provider:
            self.logger.error("No suitable data provider available")
            return None
        
        return provider.get_historical_data(symbol, timeframe, limit)
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """Fetch real-time data using the best available provider."""
        # Similar logic to historical data
        if '/' in symbol or symbol.upper().endswith(('USDT', 'BTC', 'ETH')):
            provider = self.providers.get('crypto')
        else:
            provider = self.providers.get('stocks')
            
            if not provider and 'alpha_vantage' in self.providers:
                provider = self.providers['alpha_vantage']
        
        if not provider:
            return None
        
        return provider.get_real_time_data(symbol)
    
    def get_multiple_quotes(self, symbols: List[str]) -> Dict[str, Dict]:
        """Fetch real-time quotes for multiple symbols."""
        results = {}
        
        for symbol in symbols:
            quote = self.get_real_time_data(symbol)
            if quote:
                results[symbol] = quote
            else:
                self.logger.warning(f"Failed to fetch quote for {symbol}")
        
        return results
    
    def test_connection(self) -> Dict[str, bool]:
        """Test connection to all configured providers."""
        results = {}
        
        for provider_name, provider in self.providers.items():
            try:
                # Test with a simple symbol
                test_symbol = 'AAPL' if provider_name != 'crypto' else 'BTC/USD'
                data = provider.get_real_time_data(test_symbol)
                results[provider_name] = data is not None
            except Exception as e:
                self.logger.error(f"Connection test failed for {provider_name}: {e}")
                results[provider_name] = False
        
        return results
