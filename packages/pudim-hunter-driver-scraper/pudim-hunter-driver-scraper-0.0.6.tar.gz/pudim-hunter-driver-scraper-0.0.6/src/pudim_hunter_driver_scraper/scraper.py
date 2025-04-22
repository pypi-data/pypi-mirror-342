"""
Base Playwright scraper implementation.
"""
import asyncio
import subprocess
import logging

from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright, Browser, Page

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

    def __enter__(self):
        """Set up the browser context for synchronous usage."""
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        self._context = self._browser.new_context()
        self._page = self._context.new_page()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up browser resources for synchronous usage."""
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
            
    async def __aenter__(self):
        """Set up the browser context for asynchronous usage."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=self.headless)
        self._context = await self._browser.new_context()
        self._page = await self._context.new_page()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up browser resources for asynchronous usage."""
        if self._page:
            await self._page.close()
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._page = None
        self._context = None
        self._browser = None
        self._playwright = None
            
    def navigate(self, url: str) -> None:
        """Navigate to a URL synchronously.
        
        Args:
            url: The URL to navigate to.
        """
        if not self._page:
            raise RuntimeError("Browser not initialized. Use with context.")
        self._page.goto(url)
                
    def extract_data(self, selector: str) -> Any:
        """Extract data from the page using CSS selectors synchronously.
        
        Args:
            selector: Any Valid Playwright selector.
            
        Returns:
            The text content of the element.
        """
        if not self._page:
            raise RuntimeError("Browser not initialized. Use with context.")
            
        element = self._page.query_selector(selector)
        if element:
            return element.text_content()
        else:
            return element
                
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