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
    async def build_search_url(self, query: JobQuery) -> str:
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
    def transform_data(self, data: Dict[str, Any]) -> Optional[Job]:
        """Transform scraped data into a Job object.
        
        Args:
            data: Raw scraped data.
            
        Returns:
            Job object or None if data is invalid.
        """
        pass
        
    async def fetch_jobs(self, query: JobQuery) -> JobList:
        """Fetch jobs using Playwright scraper.
        
        Args:
            query: The job search query.
            
        Returns:
            List of jobs matching the query.
        """
        try:
            async with PlaywrightScraper(headless=self.headless) as scraper:
                url = await self.build_search_url(query)
                await scraper.navigate(url)
                
                raw_data = await scraper.extract_data(self.get_selectors())
                job = self.transform_data(raw_data)
                
                jobs = [job] if job else []
                
                return JobList(
                    jobs=jobs,
                    total_results=len(jobs),
                    page=query.page,
                    items_per_page=query.items_per_page
                )
                
        except Exception as e:
            raise DriverError(f"Failed to fetch jobs: {str(e)}")
            
    async def validate_credentials(self) -> bool:
        """Validate driver credentials.
        
        Returns:
            True if credentials are valid, False otherwise.
        """
        # No credentials needed for basic scraping
        return True 