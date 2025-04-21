import subprocess
import os
import signal
import psutil
from typing import Optional

class BotRestarter:
    def __init__(self, logger):
        self.logger = logger
        self.bot_process = None
    
    def _find_bot_process(self, bot_path: str) -> Optional[psutil.Process]:
        """Find running bot process by path."""
        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                if bot_path in ' '.join(proc.cmdline()):
                    return proc
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
    
    def restart_bot(self, bot_path: str):
        """Restart the Telegram music bot."""
        try:
            # Find and stop existing bot process
            proc = self._find_bot_process(bot_path)
            if proc:
                proc.terminate()
                proc.wait(timeout=10)
            
            # Start new bot process
            self.bot_process = subprocess.Popen(
                ["python", bot_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.logger.logger.info(f"Bot restarted successfully (PID: {self.bot_process.pid})")
            return True
            
        except Exception as e:
            self.logger.logger.error(f"Failed to restart bot: {e}")
            return False