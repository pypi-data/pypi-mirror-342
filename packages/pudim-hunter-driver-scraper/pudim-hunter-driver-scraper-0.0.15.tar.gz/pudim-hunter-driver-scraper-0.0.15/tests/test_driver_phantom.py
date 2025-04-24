"""
Tests for PhantomPlaywrightScraper with a dummy job driver implementation.
"""
import os
import pytest
from datetime import datetime
from typing import Dict, Any, Optional, List
from pudim_hunter_driver.models import JobQuery, Job, JobList
from pudim_hunter_driver.exceptions import DriverError
from pudim_hunter_driver_scraper import ScraperJobDriver
from pudim_hunter_driver_scraper.driver import ScraperType
from pudim_hunter_driver_scraper.scraper_phantom import PhantomPlaywrightScraper
from screenshots import ScreenshotTaker

# Skip all tests in this module if running in CI
pytestmark = pytest.mark.skipif(
    os.getenv("GITHUB_ACTIONS") == "true",
    reason="Phantom scraper tests are skipped in CI environment due to IP blocking"
)

class DummyPhantomJobDriver(ScraperJobDriver):
    """Test implementation of ScraperJobDriver using PhantomPlaywrightScraper."""
    
    def __init__(self):
        super().__init__(scraper_type=ScraperType.PHANTOM)
        self.screenshots = ScreenshotTaker("scraper_phantom_driver")
    
    def build_search_url(self, query: JobQuery) -> str:
        """Build search URL for SimplyHired."""
        query_param = query.keywords.replace(" ", "+")
        location_param = query.location.replace(" ", "+").replace(",", "%2C")
        return f"https://www.simplyhired.com/search?q={query_param}&l={location_param}"
    
    def fetch_jobs(self, query: JobQuery) -> JobList:
        """Fetch jobs using Playwright scraper.
        
        Args:
            query: The job search query.
            
        Returns:
            List of jobs matching the query.
            
        Raises:
            DriverError: If job fetching fails.
        """
        try:
            with self._create_scraper() as scraper:
                self._scraper = scraper  # Store the scraper instance
                url = self.build_search_url(query)
                self.scraper.navigate(url)
                
                raw_jobs = self.extract_raw_job_data()
                if not raw_jobs:
                    return JobList(
                        jobs=[],
                        total=0,
                        total_results=0,
                        page=query.page,
                        items_per_page=query.items_per_page
                    )
                
                # Create dummy jobs with the same length as raw_jobs
                dummy_jobs = []
                for i in range(len(raw_jobs)):
                    dummy_jobs.append(Job(
                        id=f"dummy-{i}",
                        title=f"Dummy Job {i}",
                        company="Dummy Company",
                        location="Dummy Location",
                        description="Dummy Description",
                        url="https://example.com",
                        remote=False,
                        source="SimplyHired",
                        posted_at=datetime.now()
                    ))
                
                return JobList(
                    jobs=dummy_jobs,
                    total=len(dummy_jobs),
                    total_results=len(dummy_jobs),
                    page=query.page,
                    items_per_page=query.items_per_page
                )
                
        except Exception as e:
            raise DriverError(f"Failed to fetch jobs: {str(e)}")
        finally:
            self._scraper = None  # Always clean up the scraper reference


    def get_selectors(self) -> Dict[str, str]:
        """Get CSS selectors for job elements."""
        return {
            "job_list": "#job-list li",
            "title": 'h3[class*="jobposting-title"]',
            "company": '[class*="jobposting-company"]',
            "location": '[class*="jobposting-location"]'
        }
    
    def extract_raw_job_data(self) -> Optional[Any]:
        """Extract raw job data from the page."""
        try:
            # Take screenshot before extraction
            self.screenshots.take_screenshot(self.scraper._page, "search_initial")
            
            # Wait for job list
            selectors = self.get_selectors()
            job_list = self.scraper._page.wait_for_selector(selectors["job_list"], timeout=30000)
            if not job_list:
                return None
            
            # Get all job items
            job_items = self.scraper._page.query_selector_all(selectors["job_list"])
            if not job_items:
                return None
                
            # Take screenshot after job list loads
            self.screenshots.take_screenshot(self.scraper._page, "search_loaded")
                        
            print(f"\nFound {len(job_items)} valid job listings")
            return job_items
            
        except Exception as e:
            print(f"\nError extracting job data: {str(e)}")
            self.screenshots.take_error_screenshot(self.scraper._page)
            raise DriverError(f"Failed to extract job data: {str(e)}")
    
    def transform_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Transform raw job data into Job model."""
        pass

    def has_pagination(self) -> bool:
        return False
    
    def get_next_page_url(self, page_number: int) -> Optional[str]:
        return None
    
    def has_pagination_items_per_page(self) -> bool:
        return False

def test_phantom_driver_search():
    """Test job search functionality with phantom driver."""
    driver = DummyPhantomJobDriver()
    query = JobQuery(
        keywords="software engineer",
        location="San Francisco, CA",
        page=1,
        items_per_page=10
    )
    
    job_list = driver.fetch_jobs(query)
    assert len(job_list.jobs) > 0, "Should find at least one job"
    
def test_phantom_driver_cleanup():
    """Test that phantom scraper is cleaned up after job fetching."""
    driver = DummyPhantomJobDriver()
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

def test_phantom_driver_error_handling():
    """Test error handling in phantom driver."""
    class ErrorPhantomDriver(DummyPhantomJobDriver):
        def extract_raw_job_data(self):
            raise ValueError("Test error")
    
    driver = ErrorPhantomDriver()
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