
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import yagmail

# --- Job Parameters ---
locations = ["Hyderabad", "Pune", "Bangalore", "Chennai", "Coimbatore"]
keywords = [
    "SDE Intern",
    "Junior Software Developer",
    "Software Trainee",
    "Associate Software Engineer",
    "Entry Level Software Developer",
    "SDE 1"
]

def fetch_jobs():
    base_url = "https://www.indeed.com/jobs"
    all_jobs = []

    for location in locations:
        for keyword in keywords:
            params = {
                "q": keyword,
                "l": location,
                "limit": "10"
            }
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(base_url, params=params, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            for card in soup.select("a.tapItem"):
                try:
                    title = card.select_one("h2.jobTitle").text.strip()
                    company = card.select_one("span.companyName").text.strip()
                    loc = card.select_one("div.companyLocation").text.strip()
                    link = "https://www.indeed.com" + card["href"]

                    all_jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": loc,
                        "Link": link
                    })
                except:
                    continue

    return all_jobs

def save_to_excel(jobs):
    df = pd.DataFrame(jobs)
    filename = f"entry_level_jobs_{date.today()}.xlsx"
    df.to_excel(filename, index=False)
    return filename

def send_email(file):
    user = "your_email@gmail.com"
    app_password = "your_app_password"  # Create from Gmail > Security > App Passwords
    yag = yagmail.SMTP(user=user, password=app_password)
    yag.send(
        to=user,
        subject="Daily Entry-Level Software Jobs",
        contents="Attached is the job list for today.",
        attachments=file
    )
    print("✅ Email sent successfully!")

def run():
    print("🔍 Fetching jobs...")
    jobs = fetch_jobs()
    if jobs:
        file = save_to_excel(jobs)
        send_email(file)
    else:
        print("❌ No jobs found.")

if __name__ == "__main__":
    run()
