"""
Base Playwright scraper implementation.
"""
import subprocess
import logging
import os
from typing import Optional, Dict, Any

from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

class PlaywrightScraper:
    """Base class for Playwright-based scrapers."""
    
    DEFAULT_NAVIGATION_TIMEOUT = 60000  # 60 seconds
    DEFAULT_WAIT_TIMEOUT = 30000  # 30 seconds
    
    def __init__(self, headless: bool = True, navigation_timeout: int = DEFAULT_NAVIGATION_TIMEOUT):
        """Initialize the scraper.
        
        Args:
            headless: Whether to run the browser in headless mode.
            navigation_timeout: Maximum time in milliseconds to wait for navigation.
        """
        self.__install_playwright()

        self.headless = headless
        self.navigation_timeout = navigation_timeout
        self._browser: Optional[Browser] = None
        self._context = None
        self._page: Optional[Page] = None
        self._playwright = None

    @property
    def page(self) -> Page:
        """Get the current page instance.
        
        Returns:
            The current page instance.
            
        Raises:
            RuntimeError: If browser is not initialized.
        """
        if not self._page:
            raise RuntimeError("Browser not initialized. Call open() first.")
        return self._page

    def _get_browser_launch_options(self) -> Dict[str, Any]:
        """Get browser launch options.
        
        Returns:
            Dictionary of browser launch options.
        """
        return {
            "headless": self.headless,
            "args": [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-position=0,0',
                '--ignore-certifcate-errors',
                '--ignore-certifcate-errors-spki-list'
            ]
        }

    def _get_context_options(self) -> Dict[str, Any]:
        """Get browser context options.
        
        Returns:
            Dictionary of context options.
        """
        return {
            "viewport": {
                "width": 1280,
                "height": 720
            },
            "ignore_https_errors": True
        }

    def open(self) -> 'PlaywrightScraper':
        """Initialize and open the browser.
        
        Returns:
            Self for method chaining.
            
        Raises:
            RuntimeError: If browser is already open.
        """
        if self._playwright:
            raise RuntimeError("Browser is already open. Close it first.")
            
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(**self._get_browser_launch_options())
        self._context = self._browser.new_context(**self._get_context_options())
        self._page = self._context.new_page()
        
        # Set navigation timeout
        self._page.set_default_navigation_timeout(self.navigation_timeout)
        self._page.set_default_timeout(self.DEFAULT_WAIT_TIMEOUT)
        
        return self

    def close(self) -> None:
        """Clean up browser resources."""
        if self._page:
            self._page.close()
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None

    def __enter__(self):
        """Set up the browser context."""
        return self.open()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up browser resources."""
        self.close()
            
    def navigate(self, url: str, wait_until: str = "domcontentloaded") -> None:
        """Navigate to a URL.
        
        Args:
            url: The URL to navigate to.
            wait_until: Navigation wait condition ('load'|'domcontentloaded'|'networkidle'|'commit')
            
        Raises:
            RuntimeError: If browser is not initialized.
            PlaywrightTimeoutError: If navigation times out.
        """
        if not self._page:
            raise RuntimeError("Browser not initialized. Call open() first.")
            
        try:
            self._page.goto(url, wait_until=wait_until, timeout=self.navigation_timeout)
        except PlaywrightTimeoutError as e:
            logger.warning(f"Navigation timeout for URL: {url}")
            # Take a screenshot for debugging
            try:
                screenshots_dir = "test_screenshots"
                os.makedirs(screenshots_dir, exist_ok=True)
                self._page.screenshot(path=f"{screenshots_dir}/navigation_timeout.png")
                logger.info("Screenshot saved as navigation_timeout.png")
            except:
                pass
            raise
                
    def __install_playwright(self):
        """Ensure Playwright and its browsers are installed."""
        try:
            from playwright.sync_api import sync_playwright
            logger.info("✅ Playwright is already installed.")
        except ImportError:
            logger.info("⚠️ Playwright not found. Installing now...")
            subprocess.run(["pip", "install", "playwright"], check=True)

        # Ensure Playwright browsers are installed
        logger.info("🔄 Installing Playwright browsers...")
        subprocess.run(["playwright", "install"], check=True)
        logger.info("✅ Playwright installation complete!")