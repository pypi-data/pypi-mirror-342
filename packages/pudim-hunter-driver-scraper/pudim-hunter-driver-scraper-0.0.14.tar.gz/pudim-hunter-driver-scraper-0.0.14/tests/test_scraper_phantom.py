"""
Tests for PhantomPlaywrightScraper against bot detection test site.
"""
import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pudim_hunter_driver_scraper.scraper_phantom import PhantomPlaywrightScraper
from pudim_hunter_driver_scraper.scraper import PlaywrightScraper
from screenshots import ScreenshotTaker
import os

# Skip all tests in this module if running in CI
pytestmark = pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Phantom scraper tests are skipped in CI environment due to IP blocking"
)

TEST_URL = "https://bot.sannysoft.com"

def test_bot_detection_site():
    """Test access to bot detection test site."""
    scraper = PhantomPlaywrightScraper(navigation_timeout=60000)  # 60 second timeout
    screenshots = ScreenshotTaker("scraper_phantom_bot_detection")
    
    try:
        with scraper:
            page = scraper.page
            page.goto(TEST_URL)
            
            # Take screenshot for debugging
            screenshots.take_screenshot(page, "initial")
            
            # Check WebGL values
            webgl_vendor = page.evaluate("""() => {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                return gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
            }""")
            
            webgl_renderer = page.evaluate("""() => {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                return gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
            }""")
            
            print(f"\nWebGL Vendor: {webgl_vendor}")
            print(f"WebGL Renderer: {webgl_renderer}")
            
            assert webgl_vendor == "Intel Inc."
            assert webgl_renderer == "Intel Iris OpenGL Engine"
            
            # Test other anti-detection features
            webdriver = page.evaluate("() => navigator.webdriver")
            assert webdriver is False, "WebDriver should not be detected"
            
            chrome = page.evaluate("() => window.chrome !== undefined")
            assert chrome is True, "Chrome object should be present"
            
            plugins = page.evaluate("""() => {
                const plugins = navigator.plugins;
                return plugins.length > 0 && plugins[0].name === 'Chrome PDF Plugin';
            }""")
            assert plugins is True, "Should have fake plugins"
            
            languages = page.evaluate("""() => {
                return navigator.languages[0] === 'en-US' && navigator.languages[1] === 'en';
            }""")
            assert languages is True, "Should have specified languages"
            
    except Exception as e:
        print(f"\nError accessing bot detection site: {str(e)}")
        if hasattr(scraper, 'page') and scraper.page:
            screenshots.take_error_screenshot(scraper.page)
        raise

def test_basic_scraper_comparison():
    """Test that our anti-detection features make a difference."""
    # First try with basic scraper
    basic_scraper = PlaywrightScraper(navigation_timeout=60000)
    phantom_scraper = PhantomPlaywrightScraper(navigation_timeout=60000)
    screenshots = ScreenshotTaker("scraper_phantom_comparison")
    
    try:
        # Test basic scraper
        with basic_scraper:
            page = basic_scraper.page
            page.goto(TEST_URL)
            screenshots.take_screenshot(page, "basic")
            
            webdriver_basic = page.evaluate("() => navigator.webdriver")
            chrome_basic = page.evaluate("() => window.chrome !== undefined")
            
        # Test phantom scraper
        with phantom_scraper:
            page = phantom_scraper.page
            page.goto(TEST_URL)
            screenshots.take_screenshot(page, "phantom")
            
            webdriver_phantom = page.evaluate("() => navigator.webdriver")
            chrome_phantom = page.evaluate("() => window.chrome !== undefined")
        
        # Compare results
        assert webdriver_basic is not False, "Basic scraper should be detected"
        assert webdriver_phantom is False, "Phantom scraper should not be detected"
        assert chrome_phantom is True, "Phantom scraper should have chrome object"
            
    except Exception as e:
        print(f"\nError in comparison test: {str(e)}")
        raise 