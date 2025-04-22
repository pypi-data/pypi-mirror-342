"""
Pudim Hunter Driver Scraper - A Playwright-based scraper implementation for The Pudim Hunter platform.
"""

from .scraper import PlaywrightScraper
from .driver import ScraperJobDriver

__version__ = "0.0.5"
__all__ = ["PlaywrightScraper", "ScraperJobDriver"] 