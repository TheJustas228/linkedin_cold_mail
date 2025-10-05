import requests
from bs4 import BeautifulSoup
import csv
import time

# =======================
# CONFIGURATION
# =======================
KEYWORDS = "AI Data"       # Change this to your desired job title or keyword
LOCATION = "European union"          # You can use cities too, e.g. "Amsterdam"
MAX_PAGES =  10                    # Each page = 25 jobs; adjust for more
OUTPUT_FILE = "linkedin_jobs.csv" # Where results are saved
REQUEST_DELAY = 2                 # Seconds between page requests to avoid getting blocked

# =======================
# SCRAPER LOGIC
# =======================
BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_page(start):
    """Scrape a single page of LinkedIn job results."""
    params = {
        "keywords": KEYWORDS,
        "location": LOCATION,
        "start": start
    }
    resp = requests.get(BASE_URL, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.text

def parse_jobs(html):
    """Parse job postings from LinkedIn HTML snippet."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for li in soup.find_all("li"):
        title_tag = li.find("h3")
        company_tag = li.find("h4")
        location_tag = li.find(class_="job-search-card__location")
        link_tag = li.find("a", href=True)

        if not (title_tag and company_tag and link_tag):
            continue

        job = {
            "title": title_tag.get_text(strip=True),
            "company": company_tag.get_text(strip=True),
            "location": location_tag.get_text(strip=True) if location_tag else "",
            "url": link_tag["href"]
        }
        jobs.append(job)
    return jobs

def save_to_csv(jobs, filename):
    """Save job postings to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "url"])
        writer.writeheader()
        writer.writerows(jobs)

def main():
    all_jobs = []
    for page in range(MAX_PAGES):
        start = page * 25
        print(f"Scraping page {page + 1} (start={start})...")
        html = scrape_page(start)
        jobs = parse_jobs(html)
        if not jobs:
            print("No more jobs found — stopping.")
            break
        all_jobs.extend(jobs)
        time.sleep(REQUEST_DELAY)

    print(f"Scraped {len(all_jobs)} jobs total.")
    save_to_csv(all_jobs, OUTPUT_FILE)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()