"""
Base scraper job driver implementation.
"""
from typing import Dict, Any, Optional
from abc import abstractmethod

from pudim_hunter_driver.driver import JobDriver
from pudim_hunter_driver.models import JobQuery, JobList, Job
from pudim_hunter_driver.exceptions import DriverError

from .scraper import PlaywrightScraper

class ScraperJobDriver(JobDriver):
    """Base class for scraper-based job drivers."""
    
    def __init__(self, headless: bool = True):
        """Initialize the driver.
        
        Args:
            headless: Whether to run the browser in headless mode.
        """
        self.headless = headless

        
    @abstractmethod
    def build_search_url(self, query: JobQuery) -> str:
        """Build the search URL for the job board.
        
        Args:
            query: The job search query.
            
        Returns:
            The complete search URL.
        """
        pass

        
    @abstractmethod
    def get_selectors(self) -> Dict[str, str]:
        """Get the CSS selectors for job data extraction.
        
        Returns:
            Dictionary mapping field names to CSS selectors.
        """
        pass
        

    @abstractmethod
    def extract_raw_job_data(self) -> Optional[Any]:
        """Extract job data from the page using a CSS selector.
        
        Args:
            selector: The Playwright selector to use.
            
        Returns:
            ElementHandle or None if selector not found.
        """
        pass
        

    @abstractmethod
    def transform_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Transform scraped data into a Job object.
        
        Args:
            data: Raw scraped data.
            
        Returns:
            Job object or None if data is invalid.
        """
        pass
        

    def fetch_jobs(self, query: JobQuery) -> JobList:
        """Fetch jobs using Playwright scraper.
        
        Args:
            query: The job search query.
            
        Returns:
            List of jobs matching the query.
        """
        try:
            with PlaywrightScraper(headless=self.headless) as scraper:
                url = self.build_search_url(query)
                scraper.navigate(url)
                
                jobs = []
                
                raw_jobs = self.extract_raw_job_data()
                for raw_job in raw_jobs:
                    job = self.transform_job(raw_job)
                    jobs.append(job)
                
                return JobList(
                    jobs=jobs,
                    total_results=len(jobs),
                    page=query.page,
                    items_per_page=query.items_per_page
                )
                
        except Exception as e:
            raise DriverError(f"Failed to fetch jobs: {str(e)}")
            
    def validate_credentials(self) -> bool:
        """Validate driver credentials.
        
        Returns:
            True if credentials are valid, False otherwise.
        """
        # No credentials needed for basic scraping
        return True 