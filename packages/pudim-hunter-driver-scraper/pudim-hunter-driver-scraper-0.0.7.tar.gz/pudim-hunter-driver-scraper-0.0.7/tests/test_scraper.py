"""
Tests for the PlaywrightScraper class.
"""
import pytest
from pudim_hunter_driver_scraper import PlaywrightScraper

TEST_URL = "https://github.com/luismr"
TEST_SELECTORS = {
    "name": ".vcard-fullname",
    "bio": ".user-profile-bio",
    "repositories": "nav.UnderlineNav-body a[href$='repositories'] span.Counter"
}

def test_scraper_context_manager():
    """Test that the scraper can be used as a context manager."""
    with PlaywrightScraper() as scraper:
        assert scraper._browser is not None
        assert scraper._context is not None
        assert scraper._page is not None
    
    # Check cleanup
    assert scraper._browser is None
    assert scraper._context is None
    assert scraper._page is None

def test_scraper_navigation():
    """Test that the scraper can navigate to a URL."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        assert "github.com/luismr" in scraper._page.url

def test_scraper_extract_data():
    """Test that the scraper can extract data using multiple selectors."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        data = scraper.extract_data(TEST_SELECTORS)
        
        # Verify all fields are present
        assert all(field in data for field in TEST_SELECTORS)
        
        # Verify name is present (this should always exist)
        assert data["name"] is not None
        assert isinstance(data["name"], str)
        assert len(data["name"]) > 0

def test_scraper_extract_data_invalid_selectors():
    """Test that the scraper handles invalid selectors gracefully."""
    invalid_selectors = {
        "nonexistent1": "#this-element-does-not-exist",
        "nonexistent2": ".this-class-does-not-exist",
        "nonexistent3": "[data-test='nonexistent']"
    }
    
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        data = scraper.extract_data(invalid_selectors)
        
        assert all(field in data for field in invalid_selectors)
        assert all(value is None for value in data.values())

def test_scraper_without_context():
    """Test that the scraper raises appropriate errors when used outside context."""
    scraper = PlaywrightScraper()
    
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        scraper.navigate(TEST_URL)
    
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        scraper.extract_data(TEST_SELECTORS) 