from typing import Dict, Optional
import json
import browser_cookie3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CookieFetcher:
    def __init__(self, use_selenium: bool = False):
        self.use_selenium = use_selenium
    
    def fetch_cookies(self) -> Dict:
        """Fetch YouTube cookies using either Selenium or browser_cookie3."""
        if self.use_selenium:
            return self._fetch_with_selenium()
        return self._fetch_with_browser_cookie3()
    
    def _fetch_with_browser_cookie3(self) -> Dict:
        """Fetch cookies using browser_cookie3 library."""
        cookies = browser_cookie3.chrome(domain_name=".youtube.com")
        return {
            cookie.name: cookie.value 
            for cookie in cookies
        }
    
    def _fetch_with_selenium(self) -> Dict:
        """Fetch cookies using Selenium with Chrome."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(options=options)
        try:
            driver.get("https://www.youtube.com")
            # Wait for cookies to be set
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            cookies = driver.get_cookies()
            return {
                cookie["name"]: cookie["value"] 
                for cookie in cookies
            }
        finally:
            driver.quit()
    
    def save_cookies(self, cookies: Dict, filepath: str):
        """Save cookies in yt-dlp compatible JSON format."""
        cookie_list = [
            {
                "name": name,
                "value": value,
                "domain": ".youtube.com",
                "path": "/"
            }
            for name, value in cookies.items()
        ]
        
        with open(filepath, "w") as f:
            json.dump({"cookies": cookie_list}, f, indent=2)