"""
Tests for the PlaywrightScraper class.
"""
import pytest
from pudim_hunter_driver_scraper import PlaywrightScraper

TEST_URL = "https://github.com/luismr"
TEST_SELECTOR = ".vcard-fullname"  # GitHub profile name selector

def test_scraper_context_manager():
    """Test that the scraper can be used as a context manager."""
    with PlaywrightScraper() as scraper:
        assert scraper._browser is not None
        assert scraper._context is not None
        assert scraper.page is not None
    
    # Check cleanup
    assert scraper._browser is None
    assert scraper._context is None
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        _ = scraper.page

def test_scraper_navigation():
    """Test that the scraper can navigate to a URL."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        assert "github.com/luismr" in scraper.page.url

def test_scraper_get_element():
    """Test that the scraper can get an element using a selector."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        element = scraper.page.query_selector(TEST_SELECTOR)
        assert element is not None
        assert element.text_content() is not None
        assert len(element.text_content()) > 0

def test_scraper_get_elements():
    """Test that the scraper can get multiple elements using a selector."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        elements = scraper.page.query_selector_all("a")  # Get all links
        assert len(elements) > 0
        assert all(e is not None for e in elements)

def test_scraper_get_nonexistent_element():
    """Test that the scraper handles nonexistent elements gracefully."""
    with PlaywrightScraper() as scraper:
        scraper.navigate(TEST_URL)
        element = scraper.page.query_selector("#nonexistent-element")
        assert element is None

def test_scraper_without_context():
    """Test that the scraper raises appropriate errors when used outside context."""
    scraper = PlaywrightScraper()
    
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        scraper.navigate(TEST_URL)

def test_page_property():
    """Test that the page property works correctly and raises appropriate errors."""
    scraper = PlaywrightScraper()
    
    # Should raise error when accessed outside context
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        _ = scraper.page
        
    # Should work within context
    with scraper:
        assert scraper.page is not None
        
    # Should raise error after context exit
    with pytest.raises(RuntimeError, match="Browser not initialized"):
        _ = scraper.page 