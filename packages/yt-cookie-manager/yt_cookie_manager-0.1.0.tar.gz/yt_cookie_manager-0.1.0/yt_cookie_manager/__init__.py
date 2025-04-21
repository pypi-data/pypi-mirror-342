"""
YouTube Cookie Manager for Telegram Music Bots.
Provides automated cookie management and updates for yt-dlp based bots.
"""

from .main import auto_update_cookies

__version__ = "0.1.0"
__all__ = ["auto_update_cookies"]