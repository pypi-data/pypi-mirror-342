import json
import requests
from typing import Dict, Tuple

class CookieChecker:
    def __init__(self):
        self.test_url = "https://www.youtube.com/feed/subscriptions"
    
    def load_cookies(self, cookie_file: str) -> Dict:
        """Load cookies from file."""
        with open(cookie_file, 'r') as f:
            data = json.load(f)
            return {
                cookie['name']: cookie['value']
                for cookie in data.get('cookies', [])
            }
    
    def check_validity(self, cookies: Dict) -> Tuple[bool, str]:
        """
        Check if cookies are valid by making a test request.
        Returns (is_valid, message)
        """
        try:
            response = requests.get(
                self.test_url,
                cookies=cookies,
                allow_redirects=False
            )
            
            if response.status_code == 200:
                return True, "Cookies are valid"
            elif response.status_code == 302:
                return False, "Cookies expired (redirect to login)"
            else:
                return False, f"Unexpected status code: {response.status_code}"
        
        except requests.RequestException as e:
            return False, f"Request failed: {str(e)}"