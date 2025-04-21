import schedule
import time
import threading
from typing import Callable

class UpdateScheduler:
    def __init__(self, logger):
        self.logger = logger
        self.schedule_thread = None
        self.is_running = False
    
    def start(self, update_func: Callable, interval_hours: int = 6):
        """Start scheduled cookie updates."""
        self.is_running = True
        
        schedule.every(interval_hours).hours.do(update_func)
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)
        
        self.schedule_thread = threading.Thread(target=run_scheduler)
        self.schedule_thread.daemon = True
        self.schedule_thread.start()
        
        self.logger.logger.info(f"Scheduler started (interval: {interval_hours}h)")
    
    def stop(self):
        """Stop the scheduler."""
        self.is_running = False
        if self.schedule_thread:
            self.schedule_thread.join()
        schedule.clear()
        self.logger.logger.info("Scheduler stopped")