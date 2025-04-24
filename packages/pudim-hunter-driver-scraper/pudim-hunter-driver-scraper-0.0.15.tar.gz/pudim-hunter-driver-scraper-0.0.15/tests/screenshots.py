"""
Utility module for handling test screenshots.
"""
import os
from typing import Optional
from playwright.sync_api import Page

class ScreenshotTaker:
    """Handles taking and managing test screenshots."""
    
    def __init__(self, test_name: str, screenshots_dir: str = "test_screenshots"):
        """
        Initialize screenshot taker.
        
        Args:
            test_name: Name of the test (used as prefix for screenshot files)
            screenshots_dir: Directory to store screenshots
        """
        self.test_name = test_name
        self.screenshots_dir = screenshots_dir
        os.makedirs(screenshots_dir, exist_ok=True)
    
    def take_screenshot(self, page: Page, name: str) -> str:
        """
        Take a screenshot with proper naming convention.
        
        Args:
            page: Playwright page object
            name: Screenshot name (will be added to test_name)
            
        Returns:
            Path to the saved screenshot
        """
        filename = f"{self.test_name}_{name}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        page.screenshot(path=filepath)
        return filepath
    
    def take_error_screenshot(self, page: Optional[Page], name: str = "error") -> Optional[str]:
        """
        Take an error screenshot if page is available.
        
        Args:
            page: Optional Playwright page object
            name: Screenshot name suffix (default: "error")
            
        Returns:
            Path to the saved screenshot or None if page not available
        """
        if page:
            return self.take_screenshot(page, name)
        return None 