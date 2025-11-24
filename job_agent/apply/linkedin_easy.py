import time
from .base import JobApplier
import logging

logger = logging.getLogger("JobAgent")

class LinkedInEasyApplier(JobApplier):
    def __init__(self, page):
        self.page = page

    def apply(self, job_url: str, resume_path: str):
        logger.info(f"Attempting to apply to {job_url}")
        self.page.goto(job_url)
        time.sleep(2)

        # Check for "Easy Apply" button
        try:
            easy_apply_button = self.page.locator("button.jobs-apply-button")
            if easy_apply_button.count() > 0 and "Easy Apply" in easy_apply_button.inner_text():
                easy_apply_button.click()
                logger.info("Clicked Easy Apply button.")
                
                # Handle the application modal
                # This is highly variable. A robust agent needs to handle multiple steps.
                # For this MVP, we will just try to click "Next" or "Submit"
                
                # Wait for modal
                self.page.wait_for_selector(".jobs-easy-apply-content", timeout=5000)
                
                # Try to find submit button
                submit_button = self.page.locator("button[aria-label='Submit application']")
                if submit_button.count() > 0:
                    # In a real scenario, we would click this. 
                    # For safety/testing, we might just log it.
                    # submit_button.click()
                    logger.info("Found Submit button. Application would be submitted here.")
                else:
                    next_button = self.page.locator("button[aria-label='Continue to next step']")
                    if next_button.count() > 0:
                         logger.info("Found Next button. Multi-step application detected.")
                         # Handle multi-step... (complex)
            else:
                logger.info("No Easy Apply button found (or already applied).")
        except Exception as e:
            logger.error(f"Error applying to {job_url}: {e}")
