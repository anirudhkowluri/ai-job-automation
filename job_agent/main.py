import argparse
from job_agent.config import Config
from job_agent.search.linkedin import LinkedInSearcher
from job_agent.apply.linkedin_easy import LinkedInEasyApplier
from job_agent.utils.logger import setup_logger

from job_agent.user_profile import UserProfile

logger = setup_logger()

def run_job_agent(keywords, locations, apply_mode=False):
    logger.info(f"Starting AI Job Application Agent for {UserProfile.NAME}...")
    
    searcher = LinkedInSearcher()
    try:
        searcher.login()
        
        all_results = []
        for location in locations:
            searcher.search_jobs(keywords, location)
            
        results = searcher.get_results()
        
        if not results.empty:
            logger.info(f"Found {len(results)} jobs.")
            results.to_csv("job_results.csv", index=False)
            logger.info("Saved results to job_results.csv")
            
            if apply_mode:
                import os
                if not os.path.exists(UserProfile.RESUME_PATH):
                    logger.error(f"Resume not found at {UserProfile.RESUME_PATH}. Please place your resume file there.")
                    return results

                applier = LinkedInEasyApplier(searcher.page)
                for index, row in results.iterrows():
                    applier.apply(row['link'], UserProfile.RESUME_PATH)
            return results
        else:
            logger.info("No jobs found.")
            return results

    finally:
        searcher.close()

def main():
    parser = argparse.ArgumentParser(description="AI Job Application Agent")
    parser.add_argument("--keywords", nargs="+", default=["Data Scientist", "Machine Learning Engineer", "AI Engineer"], help="Job keywords to search for")
    parser.add_argument("--location", default="Hyderabad, Bangalore, Pune, Remote", help="Location to search in")
    parser.add_argument("--apply", action="store_true", help="Enable auto-apply mode (Use with caution)")
    args = parser.parse_args()

    locations = [loc.strip() for loc in args.location.split(',')]
    run_job_agent(args.keywords, locations, args.apply)

if __name__ == "__main__":
    main()
