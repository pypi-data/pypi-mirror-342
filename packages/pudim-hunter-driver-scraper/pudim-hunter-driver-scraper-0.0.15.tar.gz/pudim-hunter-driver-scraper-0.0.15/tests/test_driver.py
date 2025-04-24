"""
Tests for the ScraperJobDriver class.
"""
import pytest
from datetime import datetime
from typing import Dict, Any, Optional, List
from pudim_hunter_driver.models import JobQuery, Job
from pudim_hunter_driver.exceptions import DriverError
from pudim_hunter_driver_scraper import ScraperJobDriver

class DummyJobDriver(ScraperJobDriver):
    """Test implementation of ScraperJobDriver."""
    
    def build_search_url(self, query: JobQuery) -> str:
        return "https://github.com/luismr"
        
    def get_selectors(self) -> Dict[str, str]:
        return {
            "job_list": "article.job-item",
            "title": "h2.job-title",
            "company": "span.company-name"
        }
        
    def extract_raw_job_data(self) -> Optional[List[Dict[str, Any]]]:
        # Access scraper through property to test it
        elements = self.scraper._page.query_selector_all(".vcard-fullname")
        if not elements:
            return None
            
        # Convert elements to test data
        return [{"name": elem.text_content()} for elem in elements]

    def has_pagination(self) -> bool:
        return False
    
    def has_pagination_items_per_page(self) -> bool:
        return False
    
    def get_next_page_url(self, page_number: int) -> Optional[str]:
        return "https://github.com/jobs/1"
    
    def transform_job(self, data: Dict[str, Any]) -> Optional[Job]:
        if not data or not isinstance(data, dict) or not data.get("name"):
            return None
            
        return Job(
            id="test-1",
            title=data["name"],
            company="GitHub",
            location="Remote",
            description="Test job",
            url="https://github.com/jobs/1",
            remote=True,
            source="GitHub",
            posted_at=datetime.now()
        )

def test_scraper_property_access():
    """Test that scraper property is only accessible during job fetching."""
    driver = DummyJobDriver()
    
    # Should raise error when accessed outside fetch_jobs
    with pytest.raises(RuntimeError, match="Scraper not initialized"):
        _ = driver.scraper

def test_scraper_page_access():
    """Test that scraper's page is accessible during job fetching."""
    driver = DummyJobDriver()
    query = JobQuery(
        keywords="python",
        location="remote",
        page=1,
        items_per_page=10
    )
    
    job_list = driver.fetch_jobs(query)
    assert len(job_list.jobs) > 0
    assert job_list.jobs[0].title is not None
    assert job_list.jobs[0].posted_at is not None

def test_scraper_cleanup():
    """Test that scraper is cleaned up after job fetching."""
    driver = DummyJobDriver()
    query = JobQuery(
        keywords="python",
        location="remote",
        page=1,
        items_per_page=10
    )
    
    driver.fetch_jobs(query)
    
    # Should raise error after fetch_jobs completes
    with pytest.raises(RuntimeError, match="Scraper not initialized"):
        _ = driver.scraper

def test_scraper_cleanup_on_error():
    """Test that scraper is cleaned up even if job fetching fails."""
    class ErrorDriver(DummyJobDriver):
        def extract_raw_job_data(self):
            raise ValueError("Test error")
    
    driver = ErrorDriver()
    query = JobQuery(
        keywords="python",
        location="remote",
        page=1,
        items_per_page=10
    )
    
    with pytest.raises(DriverError):
        driver.fetch_jobs(query)
    
    # Should raise error after exception
    with pytest.raises(RuntimeError, match="Scraper not initialized"):
        _ = driver.scraper 