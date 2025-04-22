"""
Base Playwright scraper implementation.
"""
import subprocess
import logging
from typing import Optional

from playwright.sync_api import sync_playwright, Browser, Page

logger = logging.getLogger(__name__)

class PlaywrightScraper:
    """Base class for Playwright-based scrapers."""
    
    def __init__(self, headless: bool = True):
        """Initialize the scraper.
        
        Args:
            headless: Whether to run the browser in headless mode.
        """
        self.__install_playwright()

        self.headless = headless
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
            raise RuntimeError("Browser not initialized. Use with context.")
        return self._page

    def __enter__(self):
        """Set up the browser context."""
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
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
            
    def navigate(self, url: str) -> None:
        """Navigate to a URL.
        
        Args:
            url: The URL to navigate to.
            
        Raises:
            RuntimeError: If browser is not initialized.
        """
        if not self._page:
            raise RuntimeError("Browser not initialized. Use with context.")
        self._page.goto(url)
                
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