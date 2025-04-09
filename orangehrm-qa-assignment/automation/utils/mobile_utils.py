from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.settings import settings
import logging
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
import time
from enum import Enum

logger = logging.getLogger(__name__)

class SwipeDirection(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

class MobileUtils:
    def __init__(self, platform: str = "android"):
        self.driver = None
        self.platform = platform.lower()
        self._setup_driver()

    def _setup_driver(self):
        """Initialize Appium driver with platform-specific capabilities"""
        desired_caps = {
            "platformName": self.platform.capitalize(),
            "newCommandTimeout": 300,
            "autoGrantPermissions": True,
            "noReset": False,
            "fullReset": False
        }

        # Platform-specific capabilities
        if self.platform == "android":
            desired_caps.update({
                "platformVersion": settings.ANDROID_VERSION,
                "deviceName": settings.ANDROID_DEVICE,
                "app": str(Path(settings.ANDROID_APP_PATH).absolute()),
                "automationName": "UiAutomator2",
                "appPackage": settings.ANDROID_PACKAGE,
                "appActivity": settings.ANDROID_ACTIVITY
            })
        elif self.platform == "ios":
            desired_caps.update({
                "platformVersion": settings.IOS_VERSION,
                "deviceName": settings.IOS_DEVICE,
                "app": str(Path(settings.IOS_APP_PATH).absolute()),
                "automationName": "XCUITest",
                "bundleId": settings.IOS_BUNDLE_ID
            })
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

        try:
            self.driver = webdriver.Remote(
                settings.APPIUM_SERVER,
                desired_capabilities=desired_caps
            )
            logger.info(f"{self.platform.capitalize()} driver initialized")
        except Exception as e:
            logger.error(f"Mobile driver setup failed: {str(e)}")
            raise

    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 30) -> Any:
        """Wait for mobile element to be present with platform-specific locators"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            logger.error(f"Element not found: {locator} - {str(e)}")
            raise

    def tap_element(self, locator: Tuple[str, str]):
        """Tap on mobile element"""
        element = self.wait_for_element(locator)
        element.click()

    def enter_text(self, locator: Tuple[str, str], text: str):
        """Enter text into a mobile text field"""
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def swipe(self, direction: SwipeDirection = SwipeDirection.UP, duration: int = 800):
        """Perform swipe gesture in specified direction"""
        size = self.driver.get_window_size()
        start_x, start_y = size['width'] // 2, size['height'] // 2

        if direction == SwipeDirection.UP:
            end_x, end_y = start_x, size['height'] * 0.2
        elif direction == SwipeDirection.DOWN:
            end_x, end_y = start_x, size['height'] * 0.8
        elif direction == SwipeDirection.LEFT:
            end_x, end_y = size['width'] * 0.2, start_y
        elif direction == SwipeDirection.RIGHT:
            end_x, end_y = size['width'] * 0.8, start_y

        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def take_screenshot(self, name: str) -> Path:
        """Capture mobile screenshot with timestamp"""
        screenshot_dir = Path("results/mobile_screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = screenshot_dir / f"{name}_{timestamp}.png"
        self.driver.save_screenshot(str(file_path))
        logger.info(f"Screenshot saved: {file_path}")
        return file_path

    def close(self):
        """Clean up mobile driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Mobile driver closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
