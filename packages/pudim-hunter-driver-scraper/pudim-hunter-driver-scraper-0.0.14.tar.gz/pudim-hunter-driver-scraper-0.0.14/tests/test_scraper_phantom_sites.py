"""
Tests for the PhantomPlaywrightScraper against real sites.
"""
import pytest
import os
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pudim_hunter_driver_scraper.scraper_phantom import PhantomPlaywrightScraper
from screenshots import ScreenshotTaker

# Skip all tests in this module if running in CI
pytestmark = pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Phantom scraper tests are skipped in CI environment due to IP blocking"
)

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
    scraper = PhantomPlaywrightScraper(navigation_timeout=90000)  # 90 second timeout
    screenshots = ScreenshotTaker("scraper_phantom_sites_job_search")
    
    try:
        with scraper:
            page = scraper.page
            print("\nNavigating to SimplyHired search URL...")
            page.goto(SIMPLYHIRED_SEARCH_URL, wait_until='networkidle')
            
            # Take screenshot after initial load
            screenshots.take_screenshot(page, "initial_load")
            
            print("Checking for common elements...")
            # Check for basic page elements first
            header = page.wait_for_selector('header', timeout=30000)
            assert header is not None, "Page header should be present"
            
            # Wait for search results container
            print("Waiting for search results container...")
            results_container = page.wait_for_selector(selector='#job-list li', timeout=45000)
            assert results_container is not None, "Search results container should be present"
            
            # Take screenshot after container loads
            screenshots.take_screenshot(page, "container_loaded")
            
            # Now wait for actual job listings
            print("Waiting for job listings...")
            job_items = page.query_selector_all(selector='#job-list li')
            assert len(job_items) > 0, "Should find at least one job listing"
            
            print(f"\nFound {len(job_items)} job listings")
            
            # Take screenshot of loaded listings
            screenshots.take_screenshot(page, "listings_loaded")
            
    except PlaywrightTimeoutError as e:
        print(f"\nTimeout error while searching SimplyHired jobs: {str(e)}")
        if hasattr(scraper, 'page') and scraper.page:
            screenshots.take_error_screenshot(scraper.page)
            # Get the current page content for debugging
            print("\nCurrent page content:")
            print(page.content())
        raise
    except Exception as e:
        print(f"\nError searching SimplyHired jobs: {str(e)}")
        if hasattr(scraper, 'page') and scraper.page:
            screenshots.take_error_screenshot(scraper.page)
        raise 