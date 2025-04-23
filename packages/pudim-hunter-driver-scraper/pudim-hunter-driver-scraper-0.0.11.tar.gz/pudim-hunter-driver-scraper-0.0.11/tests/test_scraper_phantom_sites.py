"""
Tests for the PhantomPlaywrightScraper against real sites.
"""
import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pudim_hunter_driver_scraper.scraper_phantom import PhantomPlaywrightScraper
from screenshots import ScreenshotTaker

SIMPLYHIRED_URL = "https://www.simplyhired.com"
SIMPLYHIRED_SEARCH_URL = "https://www.simplyhired.com/search?q=software+engineer&l=San+Francisco%2C+CA"

def test_simplyhired_access():
    """Test access to SimplyHired without bot detection."""
    scraper = PhantomPlaywrightScraper(navigation_timeout=60000)  # 60 second timeout
    screenshots = ScreenshotTaker("scraper_phantom_sites_simplyhired")
    
    try:
        with scraper:
            page = scraper.page
            page.goto(SIMPLYHIRED_URL)
            
            # Take screenshot for debugging
            screenshots.take_screenshot(page, "initial")
            
            # Check for bot detection elements
            recaptcha = page.query_selector('iframe[src*="recaptcha"]')
            cloudflare = page.query_selector('#challenge-running')
            
            assert recaptcha is None, "reCAPTCHA should not be present"
            assert cloudflare is None, "Cloudflare protection should not be triggered"
            
            # Verify we can interact with the page
            search_box = page.wait_for_selector('input[name="q"]', timeout=30000)
            assert search_box is not None, "Search box should be present"
            
    except Exception as e:
        print(f"\nError accessing SimplyHired: {str(e)}")
        if hasattr(scraper, 'page') and scraper.page:
            screenshots.take_error_screenshot(scraper.page)
        raise

def test_simplyhired_job_search():
    """Test searching for jobs on SimplyHired and extracting listings."""
    scraper = PhantomPlaywrightScraper(navigation_timeout=60000)  # 60 second timeout
    screenshots = ScreenshotTaker("scraper_phantom_sites_job_search")
    
    try:
        with scraper:
            page = scraper.page
            page.goto(SIMPLYHIRED_SEARCH_URL)
            
            # Take screenshot before job list loads
            screenshots.take_screenshot(page, "initial")
            
            # Wait for job listings to appear and get them
            job_list = page.wait_for_selector('#job-list', timeout=30000)
            assert job_list is not None, "Job list container should be present"
            
            job_items = page.query_selector_all('#job-list li')
            assert len(job_items) > 0, "Should find at least one job listing"
            
            print(f"\nFound {len(job_items)} job listings")
            
            # Take screenshot after job list loads
            screenshots.take_screenshot(page, "loaded")
            
    except Exception as e:
        print(f"\nError searching SimplyHired jobs: {str(e)}")
        if hasattr(scraper, 'page') and scraper.page:
            screenshots.take_error_screenshot(scraper.page)
        raise 