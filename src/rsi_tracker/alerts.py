"""
Alert management system for RSI notifications.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

from .core import RSISignal


@dataclass
class AlertConfig:
    """Alert configuration settings."""
    email_enabled: bool = False
    email_smtp_server: str = ""
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_recipients: List[str] = None
    
    sms_enabled: bool = False
    sms_provider: str = ""  # 'twilio', etc.
    sms_api_key: str = ""
    sms_api_secret: str = ""
    sms_recipients: List[str] = None
    
    webhook_enabled: bool = False
    webhook_url: str = ""
    
    cooldown_minutes: int = 60  # Prevent spam alerts
    
    def __post_init__(self):
        if self.email_recipients is None:
            self.email_recipients = []
        if self.sms_recipients is None:
            self.sms_recipients = []


class EmailNotifier:
    """Email notification handler."""
    
    def __init__(self, config: AlertConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, signal: RSISignal) -> bool:
        """Send email alert for RSI signal."""
        if not self.config.email_enabled or not self.config.email_recipients:
            return False
        
        try:
            # Create email content
            subject = f"RSI Alert: {signal.symbol} - {signal.signal_type.title()}"
            body = self._create_email_body(signal)
            
            # Setup email message
            msg = MIMEMultipart()
            msg['From'] = self.config.email_username
            msg['To'] = ', '.join(self.config.email_recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.config.email_smtp_server, self.config.email_smtp_port) as server:
                server.starttls()
                server.login(self.config.email_username, self.config.email_password)
                server.send_message(msg)
            
            self.logger.info(f"Email alert sent for {signal.symbol}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
            return False
    
    def _create_email_body(self, signal: RSISignal) -> str:
        """Create HTML email body for RSI alert."""
        
        # Determine color based on signal type
        if signal.signal_type == 'overbought':
            color = '#ff6b6b'  # Red
            icon = '🔴'
        elif signal.signal_type == 'oversold':
            color = '#51cf66'  # Green
            icon = '🟢'
        else:
            color = '#ffd43b'  # Yellow
            icon = '🟡'
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .alert-box {{ background-color: {color}; color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
                .details {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .metric {{ display: flex; justify-content: space-between; margin: 10px 0; padding: 10px 0; border-bottom: 1px solid #e9ecef; }}
                .footer {{ text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>RSI Alert Notification</h1>
                    <p>Advanced RSI Market Tracker</p>
                </div>
                
                <div class="alert-box">
                    <h2>{icon} {signal.signal_type.title()} Signal</h2>
                    <h3>{signal.symbol}</h3>
                </div>
                
                <div class="details">
                    <h3>Signal Details</h3>
                    <div class="metric">
                        <span><strong>RSI Value:</strong></span>
                        <span>{signal.rsi_value:.2f}</span>
                    </div>
                    <div class="metric">
                        <span><strong>Signal Type:</strong></span>
                        <span>{signal.signal_type.title()}</span>
                    </div>
                    <div class="metric">
                        <span><strong>Timestamp:</strong></span>
                        <span>{signal.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</span>
                    </div>
                    <div class="metric">
                        <span><strong>Current Price:</strong></span>
                        <span>${signal.price:.2f}</span>
                    </div>
                </div>
                
                <div class="details">
                    <h3>What This Means</h3>
                    <p>
                    {'The RSI indicates the asset may be overbought and due for a pullback. Consider taking profits or waiting for a better entry point.' if signal.signal_type == 'overbought' else 
                     'The RSI indicates the asset may be oversold and due for a bounce. Consider this as a potential buying opportunity.' if signal.signal_type == 'oversold' else 
                     'The RSI is in neutral territory. Monitor for potential breakout signals.'}
                    </p>
                </div>
                
                <div class="footer">
                    <p>This alert was generated by Advanced RSI Market Tracker</p>
                    <p>This is not financial advice. Always do your own research.</p>
                </div>
            </div>
        </body>
        </html>
        """


class SMSNotifier:
    """SMS notification handler using Twilio."""
    
    def __init__(self, config: AlertConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        if config.sms_enabled and config.sms_provider == 'twilio':
            try:
                from twilio.rest import Client
                self.client = Client(config.sms_api_key, config.sms_api_secret)
            except ImportError:
                self.logger.warning("Twilio package not installed. SMS alerts disabled.")
                self.client = None
        else:
            self.client = None
    
    def send_alert(self, signal: RSISignal) -> bool:
        """Send SMS alert for RSI signal."""
        if not self.config.sms_enabled or not self.client or not self.config.sms_recipients:
            return False
        
        try:
            message = self._create_sms_message(signal)
            
            for recipient in self.config.sms_recipients:
                self.client.messages.create(
                    body=message,
                    from_='+1234567890',  # Configure your Twilio number
                    to=recipient
                )
            
            self.logger.info(f"SMS alert sent for {signal.symbol}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send SMS alert: {e}")
            return False
    
    def _create_sms_message(self, signal: RSISignal) -> str:
        """Create SMS message for RSI alert."""
        emoji = '🔴' if signal.signal_type == 'overbought' else '🟢' if signal.signal_type == 'oversold' else '🟡'
        
        return f"""{emoji} RSI Alert: {signal.symbol}
Signal: {signal.signal_type.title()}
RSI: {signal.rsi_value:.1f}
Price: ${signal.price:.2f}
Time: {signal.timestamp.strftime('%H:%M UTC')}

Advanced RSI Tracker"""


class WebhookNotifier:
    """Webhook notification handler."""
    
    def __init__(self, config: AlertConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, signal: RSISignal) -> bool:
        """Send webhook notification for RSI signal."""
        if not self.config.webhook_enabled or not self.config.webhook_url:
            return False
        
        try:
            import requests
            
            payload = {
                'symbol': signal.symbol,
                'rsi_value': signal.rsi_value,
                'signal_type': signal.signal_type,
                'price': signal.price,
                'timestamp': signal.timestamp.isoformat(),
                'volume': signal.volume
            }
            
            response = requests.post(
                self.config.webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            response.raise_for_status()
            self.logger.info(f"Webhook alert sent for {signal.symbol}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook alert: {e}")
            return False


class AlertManager:
    """Main alert management system."""
    
    def __init__(self, config: Dict):
        # Load alert configuration
        alert_config_dict = config.get('alerts', {})
        self.alert_config = AlertConfig(
            email_enabled=alert_config_dict.get('email_enabled', False),
            email_smtp_server=alert_config_dict.get('email_smtp_server', 'smtp.gmail.com'),
            email_smtp_port=alert_config_dict.get('email_smtp_port', 587),
            email_username=alert_config_dict.get('email_username', ''),
            email_password=alert_config_dict.get('email_password', ''),
            email_recipients=alert_config_dict.get('email_recipients', []),
            
            sms_enabled=alert_config_dict.get('sms_enabled', False),
            sms_provider=alert_config_dict.get('sms_provider', 'twilio'),
            sms_api_key=alert_config_dict.get('sms_api_key', ''),
            sms_api_secret=alert_config_dict.get('sms_api_secret', ''),
            sms_recipients=alert_config_dict.get('sms_recipients', []),
            
            webhook_enabled=alert_config_dict.get('webhook_enabled', False),
            webhook_url=alert_config_dict.get('webhook_url', ''),
            
            cooldown_minutes=alert_config_dict.get('cooldown_minutes', 60)
        )
        
        # Initialize notifiers
        self.email_notifier = EmailNotifier(self.alert_config)
        self.sms_notifier = SMSNotifier(self.alert_config)
        self.webhook_notifier = WebhookNotifier(self.alert_config)
        
        # Track recent alerts to prevent spam
        self.recent_alerts: Dict[str, datetime] = {}
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, signal: RSISignal) -> bool:
        """Send alert through all enabled channels."""
        # Check cooldown
        if not self._check_cooldown(signal):
            self.logger.info(f"Alert for {signal.symbol} skipped due to cooldown")
            return False
        
        success = False
        
        # Send through all enabled channels
        if self.email_notifier.send_alert(signal):
            success = True
        
        if self.sms_notifier.send_alert(signal):
            success = True
        
        if self.webhook_notifier.send_alert(signal):
            success = True
        
        if success:
            # Update recent alerts tracking
            alert_key = f"{signal.symbol}_{signal.signal_type}"
            self.recent_alerts[alert_key] = signal.timestamp
            
            # Clean up old entries
            self._cleanup_recent_alerts()
        
        return success
    
    def _check_cooldown(self, signal: RSISignal) -> bool:
        """Check if enough time has passed since last alert for this symbol/signal type."""
        alert_key = f"{signal.symbol}_{signal.signal_type}"
        
        if alert_key in self.recent_alerts:
            last_alert = self.recent_alerts[alert_key]
            cooldown_period = timedelta(minutes=self.alert_config.cooldown_minutes)
            
            if signal.timestamp - last_alert < cooldown_period:
                return False
        
        return True
    
    def _cleanup_recent_alerts(self):
        """Remove old alert entries beyond cooldown period."""
        cutoff_time = datetime.now() - timedelta(hours=24)  # Keep 24 hours of history
        
        keys_to_remove = [
            key for key, timestamp in self.recent_alerts.items()
            if timestamp < cutoff_time
        ]
        
        for key in keys_to_remove:
            del self.recent_alerts[key]
    
    def test_notifications(self) -> Dict[str, bool]:
        """Test all notification channels."""
        test_signal = RSISignal(
            symbol='TEST',
            timestamp=datetime.now(),
            rsi_value=75.0,
            signal_type='overbought',
            price=100.0
        )
        
        results = {
            'email': False,
            'sms': False,
            'webhook': False
        }
        
        # Test each channel
        if self.alert_config.email_enabled:
            results['email'] = self.email_notifier.send_alert(test_signal)
        
        if self.alert_config.sms_enabled:
            results['sms'] = self.sms_notifier.send_alert(test_signal)
        
        if self.alert_config.webhook_enabled:
            results['webhook'] = self.webhook_notifier.send_alert(test_signal)
        
        return results
    
    def get_alert_stats(self) -> Dict:
        """Get statistics about recent alerts."""
        now = datetime.now()
        
        # Count alerts by time period
        stats = {
            'total_recent_alerts': len(self.recent_alerts),
            'alerts_last_hour': 0,
            'alerts_last_24h': len(self.recent_alerts),
            'alerts_by_symbol': {},
            'alerts_by_type': {'overbought': 0, 'oversold': 0, 'neutral': 0}
        }
        
        hour_ago = now - timedelta(hours=1)
        
        for alert_key, timestamp in self.recent_alerts.items():
            symbol, signal_type = alert_key.rsplit('_', 1)
            
            # Count by symbol
            if symbol not in stats['alerts_by_symbol']:
                stats['alerts_by_symbol'][symbol] = 0
            stats['alerts_by_symbol'][symbol] += 1
            
            # Count by type
            if signal_type in stats['alerts_by_type']:
                stats['alerts_by_type'][signal_type] += 1
            
            # Count last hour
            if timestamp > hour_ago:
                stats['alerts_last_hour'] += 1
        
        return stats
