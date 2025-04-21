import os
from typing import Optional
import time
# Change relative imports to absolute imports
from yt_cookie_manager.logger import CookieLogger
from yt_cookie_manager.cookie_fetcher import CookieFetcher
from yt_cookie_manager.cookie_checker import CookieChecker
from yt_cookie_manager.cookie_injector import CookieInjector
from yt_cookie_manager.bot_restarter import BotRestarter
from yt_cookie_manager.scheduler import UpdateScheduler

def auto_update_cookies(
    bot_path: str,
    cookie_file: str,
    use_selenium: bool = False,
    check_interval: int = 6,
    telegram_bot_token: Optional[str] = None,
    telegram_chat_id: Optional[int] = None
):
    """
    Main function to initialize and run the cookie management system.
    
    Args:
        bot_path: Path to the Telegram music bot
        cookie_file: Name of the cookie file
        use_selenium: Whether to use Selenium for cookie fetching
        check_interval: Hours between cookie validity checks
        telegram_bot_token: Optional bot token for notifications
        telegram_chat_id: Optional chat ID for notifications
    """
    # Initialize components
    logger = CookieLogger(
        telegram_bot_token=telegram_bot_token,
        telegram_chat_id=telegram_chat_id
    )
    fetcher = CookieFetcher(use_selenium=use_selenium)
    checker = CookieChecker()
    injector = CookieInjector(logger)
    restarter = BotRestarter(logger)
    scheduler = UpdateScheduler(logger)
    
    async def update_cycle():
        """Full cookie update cycle."""
        try:
            # Fetch new cookies
            cookies = fetcher.fetch_cookies()
            
            # Save to temporary file
            temp_cookie_file = "temp_cookies.json"
            fetcher.save_cookies(cookies, temp_cookie_file)
            
            # Verify cookies
            is_valid, message = checker.check_validity(cookies)
            if not is_valid:
                await logger.notify(f"Cookie validation failed: {message}", "error")
                return
            
            # Inject cookies
            if injector.inject_cookies(temp_cookie_file, bot_path, cookie_file):
                # Restart bot
                if restarter.restart_bot(bot_path):
                    await logger.notify("Cookies updated and bot restarted successfully")
                else:
                    await logger.notify("Failed to restart bot", "error")
            else:
                await logger.notify("Failed to inject cookies", "error")
            
            # Cleanup
            os.remove(temp_cookie_file)
            
        except Exception as e:
            await logger.notify(f"Update cycle failed: {str(e)}", "error")
    
    # Start the scheduler
    scheduler.start(update_cycle, check_interval)
    
    return scheduler

# Add this if you want to run the file directly
if __name__ == "__main__":
    # Example usage
    scheduler = auto_update_cookies(
        bot_path="/path/to/your/bot.py",
        cookie_file="cookies.json",
        check_interval=4,  # Check every 4 hours
    )
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()