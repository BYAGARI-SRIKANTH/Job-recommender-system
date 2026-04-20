from apify_client import ApifyClient
import os
from dotenv import load_dotenv
load_dotenv()

APIFY_API_KEY = os.getenv("APIFY_API_TOKEN")
if APIFY_API_KEY:
    apify_client = ApifyClient(APIFY_API_KEY)
else:
    apify_client = None

def fetch_linkedin_jobs(search_query, location="india", rows=60):
    """
    Fetch job listings from LinkedIn based on search query and location.

    Args:
        search_query (str): The job title or keywords to search for.
        location (str): The location to search in.
        rows (int): The number of jobs to fetch.

    Returns:
        list: A list of job dictionaries.
    """
    if not apify_client:
        return []

    try:
        run_input = {
            "title": search_query,
            "location": location,
            "rows": rows,
            "proxy": {
                "useApifyProxy": True,
                "apifyproxyGroups": ["RESIDENTIAL"],
            }
        }
        # Updated actor ID for LinkedIn jobs scraper
        run = apify_client.actor("curious_coder/linkedin-jobs-scraper").call(run_input=run_input)
        jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        return jobs
    except Exception as e:
        print(f"Error fetching LinkedIn jobs: {e}")
        return []


def fetch_naukri_jobs(search_query, location="india", rows=60):
    """
    Fetch job listings from Naukri based on search query and location.
    
    Args:
        search_query (str): The job title or keywords to search for.
        location (str): The location to search in.
        rows (int): The number of jobs to fetch.
        
    Returns:
        list: A list of job dictionaries.
    """
    if not apify_client:
        return []

    try:
        run_input = {
            "keyword": search_query,
            "location": location,
            "maxJobs": rows,
            "freshness": "all",
            "sortBy": "relevance",
            "experience": "all",
        }
        # Updated actor ID for Naukri jobs scraper
        run = apify_client.actor("shreyashjain24/naukri-jobs-scraper").call(run_input=run_input)
        jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        return jobs
    except Exception as e:
        print(f"Error fetching Naukri jobs: {e}")
        return []