"""
Tests for the PlaywrightScraper class.
"""
import pytest
from pudim_hunter_driver_scraper import PlaywrightScraper

TEST_URL = "https://github.com/luismr"
SELECTOR = ".vcard-fullname"  # GitHub profile name selector

def test_scraper_context_manager():
    """Test that the scraper can be used as a synchronous context manager."""
    with PlaywrightScraper() as scraper:
        assert scraper._browser is not None
        assert scraper._context is not None
        assert scraper._page is not None
    
    assert scraper._browser is None
    assert scraper._context is None
    assert scraper._page is None

def test_scraper_navigation():
    """Test that the scraper can navigate to a URL."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        assert "github.com/luismr" in scraper._page.url

def test_scraper_extract_data():
    """Test that the scraper can extract data using selectors."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        name = scraper.extract_data(SELECTOR)
        assert name is not None
        assert isinstance(name, str)
        assert len(name) > 0

def test_scraper_extract_data_invalid_selector():
    """Test that the scraper handles invalid selectors gracefully."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        data = scraper.extract_data("#non-existent-element")
        assert data is None

def test_scraper_without_context():
    """Test that the scraper raises appropriate errors when used outside context."""
    scraper = PlaywrightScraper()
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        scraper.navigate(TEST_URL)
    
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        scraper.extract_data(SELECTOR) 