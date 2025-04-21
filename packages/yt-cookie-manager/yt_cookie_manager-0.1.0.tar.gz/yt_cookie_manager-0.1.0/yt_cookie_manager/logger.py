import logging
import os
from datetime import datetime
from typing import Optional

from pyrogram import Client

class CookieLogger:
    def __init__(self, log_file: str = "cookie_manager.log", 
                 telegram_bot_token: Optional[str] = None,
                 telegram_chat_id: Optional[int] = None):
        self.logger = logging.getLogger("CookieManager")
        self.logger.setLevel(logging.INFO)
        
        # File handler
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Telegram notification setup
        self.telegram_bot = None
        if telegram_bot_token and telegram_chat_id:
            self.telegram_bot = Client(
                "cookie_manager_bot",
                bot_token=telegram_bot_token,
                no_updates=True
            )
            self.telegram_chat_id = telegram_chat_id
    
    async def notify(self, message: str, level: str = "info"):
        """Log message and optionally send Telegram notification."""
        getattr(self.logger, level)(message)
        
        if self.telegram_bot:
            try:
                async with self.telegram_bot:
                    await self.telegram_bot.send_message(
                        self.telegram_chat_id,
                        f"🍪 Cookie Manager: {message}"
                    )
            except Exception as e:
                self.logger.error(f"Failed to send Telegram notification: {e}")