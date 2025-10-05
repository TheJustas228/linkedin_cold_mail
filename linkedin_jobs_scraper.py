import requests
from bs4 import BeautifulSoup
import csv
import time

# ==============================
# 🔧 CONFIGURATION
# ==============================
OUTPUT_FILE = "linkedin_jobs.csv"
MAX_PAGES = 5
REQUEST_DELAY = 2  # seconds between page requests

BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ------------------------------
# Experience Level (f_E)
# ------------------------------
EXPERIENCE_LEVELS = {
    "0": ("No filter (include everything)", None),
    "1": ("Internship", "1"),
    "2": ("Entry level", "2"),
    "3": ("Associate", "3"),
    "4": ("Mid-Senior level", "4"),
    "5": ("Director", "5"),
    "6": ("Executive", "6"),
}

# ------------------------------
# Date Posted (f_TPR)
# ------------------------------
DATE_POSTED = {
    "1": ("Any time", None),
    "2": ("Past month", "r2592000"),
    "3": ("Past week", "r604800"),
    "4": ("Past 24 hours", "r86400"),
}

# ------------------------------
# Work Type (f_WT)
# ------------------------------
REMOTE_TYPES = {
    "0": ("Any", None),
    "1": ("On-site", "1"),
    "2": ("Remote", "2"),
    "3": ("Hybrid", "3"),
}


# ==============================
# 🌍 LOCATION SELECTION
# ==============================
def get_geo_id_from_location():
    print("\n🌍 Select location:")
    print("  1. European Union")
    print("  2. United States")
    choice = input("👉 Enter choice: ").strip()

    if choice == "1":
        return "91000000", "European Union"
    elif choice == "2":
        return "103644278", "United States"
    else:
        print("❌ Invalid choice. Defaulting to European Union.")
        return "91000000", "European Union"


# ==============================
# 🧠 MENU FUNCTIONS
# ==============================
def choose_filter(options_dict, title, allow_multiple=False):
    print(f"\n📌 Select {title}:")
    for k, (label, _) in options_dict.items():
        print(f"  {k}. {label}")

    choice = input("👉 Enter choice(s) (comma-separated for multiple): ").strip()
    if not choice:
        return None

    if allow_multiple:
        selected_values = []
        for c in choice.split(","):
            c = c.strip()
            if c in options_dict and options_dict[c][1]:
                selected_values.append(options_dict[c][1])
        return ",".join(selected_values) if selected_values else None
    else:
        return options_dict.get(choice, (None, None))[1]


# ==============================
# 🌐 SCRAPER FUNCTIONS
# ==============================
def scrape_page(params, start):
    """Scrape one page of job results."""
    params["start"] = start
    resp = requests.get(BASE_URL, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.text


def parse_jobs(html):
    """Extract job data from LinkedIn HTML snippets."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for li in soup.find_all("li"):
        title_tag = li.find("h3")
        company_tag = li.find("h4")
        location_tag = li.find(class_="job-search-card__location")
        link_tag = li.find("a", href=True)

        if not (title_tag and company_tag and link_tag):
            continue

        raw_url = link_tag["href"]
        job_url = raw_url if raw_url.startswith("http") else "https://www.linkedin.com" + raw_url

        job = {
            "title": title_tag.get_text(strip=True),
            "company": company_tag.get_text(strip=True),
            "location": location_tag.get_text(strip=True) if location_tag else "",
            "url": job_url,
        }
        jobs.append(job)
    return jobs


def save_to_csv(jobs, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "url"])
        writer.writeheader()
        writer.writerows(jobs)


# ==============================
# 🏁 MAIN
# ==============================
def main():
    print("🔹 LinkedIn Job Scraper with Filters 🔹\n")

    keywords = input("🔍 Enter keywords: ").strip()
    geo_id, location_label = get_geo_id_from_location()
    print(f"✅ Selected location: {location_label} (geoId={geo_id})")

    experience_filter = choose_filter(EXPERIENCE_LEVELS, "Experience level (multi-select allowed)", allow_multiple=True)
    date_filter = choose_filter(DATE_POSTED, "Date posted")
    remote_filter = choose_filter(REMOTE_TYPES, "Remote / On-site")

    params = {
        "keywords": keywords,
        "geoId": geo_id,
    }

    if experience_filter:
        params["f_E"] = experience_filter
    if date_filter:
        params["f_TPR"] = date_filter
    if remote_filter:
        params["f_WT"] = remote_filter

    print("\n📝 Search Parameters:")
    for k, v in params.items():
        print(f"  {k}: {v}")

    all_jobs = []
    for page in range(MAX_PAGES):
        start = page * 25
        print(f"\n📄 Scraping page {page + 1}...")
        html = scrape_page(params, start)
        jobs = parse_jobs(html)
        if not jobs:
            print("No more jobs found.")
            break
        all_jobs.extend(jobs)
        time.sleep(REQUEST_DELAY)

    save_to_csv(all_jobs, OUTPUT_FILE)
    print(f"\n✅ Scraped {len(all_jobs)} jobs total.")
    print(f"📁 Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
