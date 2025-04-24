"""
Tests for pagination support in ScraperJobDriver.
"""
import pytest
from datetime import datetime
from typing import Dict, Any, Optional, List
from pudim_hunter_driver.models import JobQuery, Job, JobList
from pudim_hunter_driver.exceptions import DriverError
from pudim_hunter_driver_scraper import ScraperJobDriver

class PaginatedJobDriver(ScraperJobDriver):
    """Test implementation of ScraperJobDriver with pagination support."""
    
    def __init__(self):
        super().__init__()
        self._current_page = 1
        self._total_pages = 3
        self._jobs_per_page = 2
        
    def build_search_url(self, query: JobQuery) -> str:
        """Build mock search URL."""
        return f"https://example.com/jobs?page={self._current_page}"
        
    def get_selectors(self) -> Dict[str, str]:
        """Get mock CSS selectors."""
        return {
            "job_list": ".job-item",
            "title": ".job-title",
            "company": ".company-name"
        }
        
    def extract_raw_job_data(self) -> Optional[List[Dict[str, Any]]]:
        """Extract mock job data for current page."""
        # Create mock jobs for current page
        start_idx = (self._current_page - 1) * self._jobs_per_page
        return [
            {"name": f"Job {start_idx + i + 1}"} 
            for i in range(self._jobs_per_page)
        ]

    def transform_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Transform mock job data into Job model."""
        if not data or not isinstance(data, dict) or not data.get("name"):
            return None
            
        return Job(
            id=f"job-{data['name'].split()[-1]}",
            title=data["name"],
            company="Test Company",
            location="Remote",
            description="Test job description",
            url=f"https://example.com/jobs/{data['name'].split()[-1]}",
            remote=True,
            source="TestSource",
            posted_at=datetime.now()
        )

    def has_pagination(self) -> bool:
        """Return True to enable pagination."""
        return True
    
    def has_pagination_items_per_page(self) -> bool:
        """Return True to enable pagination items per page."""
        return False
    
    def get_next_page_url(self, page_number: int) -> Optional[str]:
        """Get URL for next page if available."""
        if page_number <= self._total_pages:
            self._current_page = page_number
            return self.build_search_url(JobQuery(keywords="test", location="remote"))
        return None

def test_pagination_first_page():
    """Test fetching first page of results."""
    driver = PaginatedJobDriver()
    query = JobQuery(
        keywords="test",
        location="remote",
        page=1,
        items_per_page=2
    )
    
    job_list = driver.fetch_jobs(query)
    # Should fetch all pages but respect items_per_page in the response
    assert not driver.has_pagination_items_per_page(), "Should not have pagination items per page"
    assert job_list.total_results == 6, "Should know total number of results"
    assert job_list.page == 1, "Should return requested page number"
    assert job_list.items_per_page == 2, "Should return requested items per page"
    assert job_list.jobs[0].title == "Job 1"
    assert job_list.jobs[1].title == "Job 2"

def test_pagination_all_pages():
    """Test fetching all pages of results."""
    driver = PaginatedJobDriver()
    query = JobQuery(
        keywords="test",
        location="remote",
        page=1,
        items_per_page=6  # Request all jobs at once
    )
    
    job_list = driver.fetch_jobs(query)
    assert not driver.has_pagination_items_per_page(), "Should not have pagination items per page"
    assert len(job_list.jobs) == 6, "Should find all 6 jobs across pages"
    assert job_list.total_results == 6, "Should know total number of results"
    assert job_list.page == 1, "Should return requested page number"
    # assert job_list.items_per_page == 6, "Should return requested items per page"
    assert job_list.jobs[0].title == "Job 1"
    assert job_list.jobs[1].title == "Job 2"
    assert job_list.jobs[2].title == "Job 3"
    assert job_list.jobs[3].title == "Job 4"
    assert job_list.jobs[4].title == "Job 5"
    assert job_list.jobs[5].title == "Job 6"

def test_pagination_cleanup():
    """Test that scraper is cleaned up after paginated job fetching."""
    driver = PaginatedJobDriver()
    query = JobQuery(
        keywords="test",
        location="remote",
        page=1,
        items_per_page=6
    )
    
    driver.fetch_jobs(query)
    
    # Should raise error after fetch_jobs completes
    with pytest.raises(RuntimeError, match="Scraper not initialized"):
        _ = driver.scraper

def test_pagination_error_handling():
    """Test error handling during paginated job fetching."""
    class ErrorPaginatedDriver(PaginatedJobDriver):
        def extract_raw_job_data(self):
            if self._current_page == 2:  # Fail on second page
                raise ValueError("Test error")
            return super().extract_raw_job_data()
    
    driver = ErrorPaginatedDriver()
    query = JobQuery(
        keywords="test",
        location="remote",
        page=1,
        items_per_page=6
    )
    
    with pytest.raises(DriverError):
        driver.fetch_jobs(query)
    
    # Should raise error after exception
    with pytest.raises(RuntimeError, match="Scraper not initialized"):
        _ = driver.scraper 