# LinkedIn Cold Mail

A personal Python project that helps automate job outreach by:
- 🔍 Scraping LinkedIn job postings
- 🏢 Identifying target companies
- ✉️ (Planned) Finding recruiters and sending personalized cold emails

---

## 🚀 Features

- Search LinkedIn jobs by keyword and location (public guest endpoint)
- Save job details (title, company, location, URL) to a CSV file
- Lightweight and works without LinkedIn authentication
- Roadmap for adding recruiter finder and cold mailer

---

## 🛠 Installation

1) Clone this repository and install dependencies:
```bash
git clone https://github.com/TheJustas228/linkedin_cold_mail.git
cd linkedin_cold_mail
pip install -r requirements.txt
```

---

## 📌 Usage

Run the scraper script:
```bash
python linkedin_jobs_scraper.py
```
This will scrape LinkedIn jobs based on your chosen keywords and location, then save the results to `linkedin_jobs.csv`.
You can edit the script to change the keywords, location, and number of pages.

---

## 🧭 Roadmap

- [x] Basic LinkedIn job scraper
- [ ] Recruiter finder (LinkedIn people search)
- [ ] Email finder (e.g. Hunter.io / Apollo integration)
- [ ] Cold email sender (SMTP / API)
- [ ] Daily automated run (cron job or scheduler)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🧠 Notes

This project is intended for **personal use only**. Automated scraping of LinkedIn may be against their terms of service — use responsibly and at your own risk.
