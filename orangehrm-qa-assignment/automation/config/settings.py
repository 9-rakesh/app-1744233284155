import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Environment Configuration
    ENV = os.getenv("ENV", "staging")
    BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")
    
    # Browser Configuration
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    
    # Test Accounts
    ADMIN_USER = {
        "username": os.getenv("ADMIN_USER", "Admin"),
        "password": os.getenv("ADMIN_PASSWORD", "admin123")
    }
    
    # Reporting
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    VIDEO_RECORD = os.getenv("VIDEO_RECORD", "false").lower() == "true"
    
    @property
    def login_url(self):
        return f"{self.BASE_URL}/web/index.php/auth/login"

# Global settings instance
settings = Settings()
