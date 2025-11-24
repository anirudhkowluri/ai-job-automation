import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
