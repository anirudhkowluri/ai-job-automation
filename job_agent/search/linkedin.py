import time
import pandas as pd
from .base import JobSearcher
from ..utils.browser import BrowserManager
from ..config import Config
import logging

logger = logging.getLogger("JobAgent")

class LinkedInSearcher(JobSearcher):
    def __init__(self):
        self.browser_manager = BrowserManager(headless=Config.HEADLESS)
        self.page = None
        self.jobs = []

    def login(self):
        self.page = self.browser_manager.start()
        logger.info("Navigating to LinkedIn login page...")
        self.page.goto("https://www.linkedin.com/login")
        
        # Check if already logged in or needs login
        if "feed" not in self.page.url:
            self.page.fill("#username", Config.LINKEDIN_USERNAME)
            self.page.fill("#password", Config.LINKEDIN_PASSWORD)
            self.page.click("button[type='submit']")
            
            # Wait for navigation or manual check (2FA might be needed)
            # For now, we assume simple login or user intervention if headless=False
            self.page.wait_for_url("**/feed/**", timeout=60000) 
            logger.info("Successfully logged in to LinkedIn.")

    def search_jobs(self, keywords: list, location: str):
        for keyword in keywords:
            logger.info(f"Searching for {keyword} in {location}...")
            # Construct search URL
            # Filter for "Internship" (f_E=1) and "Entry level" (f_E=2)
            # We append &f_E=1,2 to the URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&f_E=1,2"
            self.page.goto(search_url)
            # Wait for results to load
            try:
                self.page.wait_for_selector(".jobs-search-results-list", timeout=10000)
            except:
                logger.warning("Timeout waiting for job list. Page might not have loaded correctly.")

            # Try multiple selectors for job cards
            selectors = [".job-card-container", ".jobs-search-results__list-item", "li.occludable-update"]
            job_cards = None
            for selector in selectors:
                cards = self.page.locator(selector)
                if cards.count() > 0:
                    job_cards = cards
                    logger.info(f"Found job cards using selector: {selector}")
                    break
            
            if not job_cards or job_cards.count() == 0:
                logger.warning(f"No job cards found for {keyword}. Page title: {self.page.title()}")
                self.page.screenshot(path="debug_screenshot.png")
                continue

            count = job_cards.count()
            logger.info(f"Found {count} jobs visible for {keyword}.")

            for i in range(count):
                try:
                    card = job_cards.nth(i)
                    # Try multiple title selectors
                    title_selectors = [".job-card-list__title", ".artdeco-entity-lockup__title", "strong"]
                    title = ""
                    for ts in title_selectors:
                        if card.locator(ts).count() > 0:
                            title = card.locator(ts).first.inner_text().strip()
                            break
                    
                    # Try multiple company selectors
                    company_selectors = [".job-card-container__company-name", ".artdeco-entity-lockup__subtitle", ".job-card-container__primary-description"]
                    company = ""
                    for cs in company_selectors:
                        if card.locator(cs).count() > 0:
                            company = card.locator(cs).first.inner_text().strip()
                            break

                    # Try link selectors
                    link_selectors = ["a.job-card-list__title", "a.artdeco-entity-lockup__title", "a"]
                    link = ""
                    for ls in link_selectors:
                        if card.locator(ls).count() > 0:
                            link = card.locator(ls).first.get_attribute("href")
                            break
                    
                    if title and link:
                        self.jobs.append({
                            "title": title,
                            "company": company,
                            "link": f"https://www.linkedin.com{link}" if link.startswith("/") else link,
                            "keyword": keyword
                        })
                except Exception as e:
                    logger.warning(f"Failed to parse job card {i}: {e}")

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self.jobs)

    def close(self):
        self.browser_manager.stop()
