import os
import shutil
from pathlib import Path

class CookieInjector:
    def __init__(self, logger):
        self.logger = logger
    
    def inject_cookies(self, source_path: str, bot_path: str, cookie_filename: str):
        """
        Copy cookie file to the bot's directory and ensure proper permissions.
        """
        source = Path(source_path)
        target = Path(bot_path) / cookie_filename
        
        try:
            # Create bot path if it doesn't exist
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the cookie file
            shutil.copy2(source, target)
            
            # Set appropriate permissions
            os.chmod(target, 0o600)  # User read/write only
            
            self.logger.logger.info(f"Cookies injected successfully to {target}")
            return True
            
        except Exception as e:
            self.logger.logger.error(f"Failed to inject cookies: {e}")
            return False