import os
import asyncio
import sys
from playwright.sync_api import sync_playwright
import logging

# Fix for Playwright on Windows with Streamlit/Asyncio
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

logger = logging.getLogger("JobAgent")

class BrowserManager:
    def __init__(self, headless=False):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        """Start the browser session with persistence."""
        self.playwright = sync_playwright().start()
        
        # Use a local directory for the browser profile
        user_data_dir = os.path.join(os.getcwd(), "browser_profile")
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
            
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir,
            headless=self.headless,
            channel="chrome",
            args=["--start-maximized"] # Optional, helps with visibility
        )
        
        # Get the default page or create one
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        logger.info(f"Browser started with persistent profile at {user_data_dir}")
        return self.page

    def stop(self):
        """Stop the browser session."""
        try:
            if self.context:
                self.context.close()
        except Exception as e:
            logger.warning(f"Error closing browser context (likely already closed): {e}")
            
        if self.playwright:
            self.playwright.stop()
        logger.info("Browser stopped.")
