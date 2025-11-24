from abc import ABC, abstractmethod
import pandas as pd

class JobSearcher(ABC):
    @abstractmethod
    def login(self):
        """Login to the job board."""
        pass

    @abstractmethod
    def search_jobs(self, keywords: list, location: str):
        """Search for jobs based on keywords and location."""
        pass

    @abstractmethod
    def get_results(self) -> pd.DataFrame:
        """Return the search results as a DataFrame."""
        pass
