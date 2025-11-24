from abc import ABC, abstractmethod

class JobApplier(ABC):
    @abstractmethod
    def apply(self, job_url: str, resume_path: str):
        """Apply to a job given its URL and a resume."""
        pass
