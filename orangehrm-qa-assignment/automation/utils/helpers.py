import json
import random
import string
import logging
from datetime import datetime
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestHelpers:
    @staticmethod
    def load_test_data(file_name):
        """Load test data from JSON file with error handling"""
        try:
            data_path = Path(__file__).parent.parent / "data" / file_name
            with open(data_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading test data: {str(e)}")
            raise

    @staticmethod
    def generate_random_string(length=8, prefix='', suffix=''):
        """Generate random test data with optional prefix/suffix"""
        chars = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(chars) for _ in range(length))
        return f"{prefix}{random_str}{suffix}"

    @staticmethod
    def wait_for_element(driver, locator, timeout=None):
        """Enhanced element waiting with configurable timeout"""
        timeout = timeout or settings.IMPLICIT_WAIT
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            logger.error(f"Element not found: {locator} - {str(e)}")
            raise

    @staticmethod
    def capture_screenshot(driver, test_name):
        """Capture screenshot with timestamp"""
        if settings.SCREENSHOT_ON_FAILURE:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = Path('results/screenshots')
            screenshot_dir.mkdir(exist_ok=True)
            file_path = screenshot_dir / f"{test_name}_{timestamp}.png"
            driver.save_screenshot(str(file_path))
            logger.info(f"Screenshot saved: {file_path}")
            return file_path
        return None

    @staticmethod
    def get_current_datetime(format="%Y-%m-%d %H:%M:%S"):
        """Get formatted current datetime"""
        return datetime.now().strftime(format)
