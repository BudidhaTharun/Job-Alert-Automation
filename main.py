import pandas as pd
from bs4 import BeautifulSoup
import yagmail
from datetime import date
from chrome_setup import get_driver
import time

locations = ["Hyderabad", "Pune", "Bangalore", "Chennai", "Coimbatore"]
keywords = [
    "SDE Intern",
    "Junior Software Developer",
    "Software Trainee",
    "Associate Software Engineer",
    "Entry Level Software Developer",
    "SDE 1"
]

def fetch_indeed():
    print("🌐 Scraping Indeed...")
    driver = get_driver()
    jobs = []
    for loc in locations:
        for key in keywords:
            query = f"https://www.indeed.com/jobs?q={key.replace(' ', '+')}&l={loc.replace(' ', '+')}&fromage=1"
            driver.get(query)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cards = soup.select("a.tapItem")
            for card in cards:
                try:
                    title = card.select_one("h2.jobTitle").text.strip()
                    company = card.select_one("span.companyName").text.strip()
                    location = card.select_one("div.companyLocation").text.strip()
                    link = "https://www.indeed.com" + card.get("href")
                    jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": location,
                        "Posted": "Last 24 hrs",
                        "Source": "Indeed",
                        "Link": link
                    })
                except:
                    continue
    driver.quit()
    return jobs

def fetch_naukri():
    print("🌐 Scraping Naukri...")
    driver = get_driver()
    jobs = []
    for loc in locations:
        for key in keywords:
            query = f"https://www.naukri.com/{key.replace(' ', '-')}-jobs-in-{loc.replace(' ', '-')}"
            driver.get(query)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cards = soup.find_all("article", class_="jobTuple")
            for card in cards:
                try:
                    title = card.find("a", class_="title").text.strip()
                    company = card.find("a", class_="subTitle").text.strip()
                    location = card.find("li", class_="location").text.strip()
                    posted = card.find("span", class_="type").text.strip()
                    link = card.find("a", class_="title")["href"]
                    if "hour" in posted or "day" in posted.lower():
                        jobs.append({
                            "Job Title": title,
                            "Company": company,
                            "Location": location,
                            "Posted": posted,
                            "Source": "Naukri",
                            "Link": link
                        })
                except:
                    continue
    driver.quit()
    return jobs

def fetch_linkedin():
    print("🌐 Scraping LinkedIn...")
    driver = get_driver()
    jobs = []
    for loc in locations:
        for key in keywords:
            query = f"https://www.linkedin.com/jobs/search/?keywords={key.replace(' ', '%20')}&location={loc.replace(' ', '%20')}&f_TPR=r86400&f_E=1"
            driver.get(query)
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cards = soup.find_all("li", class_="jobs-search-results__list-item")
            for card in cards:
                try:
                    title = card.find("span", class_="sr-only").text.strip()
                    company = card.find("h4").text.strip()
                    location = card.find("span", class_="job-search-card__location").text.strip()
                    link = card.find("a")["href"]
                    jobs.append({
                        "Job Title": title,
                        "Company": company,
                        "Location": location,
                        "Posted": "Last 24 hrs",
                        "Source": "LinkedIn",
                        "Link": link
                    })
                except:
                    continue
    driver.quit()
    return jobs

def save_to_excel(jobs):
    df = pd.DataFrame(jobs)
    filename = f"entry_jobs_{date.today()}.xlsx"
    df.to_excel(filename, index=False)
    return filename

def send_email(file):
    user = "your_email@gmail.com"
    app_pass = "your_app_password"
    yag = yagmail.SMTP(user=user, password=app_pass)
    yag.send(
        to=user,
        subject="Daily Software Jobs - Fresher (LinkedIn, Naukri, Indeed)",
        contents="Attached is today's entry-level job report.",
        attachments=file
    )
    print("📧 Email sent!")

def run():
    indeed_jobs = fetch_indeed()
    naukri_jobs = fetch_naukri()
    linkedin_jobs = fetch_linkedin()

    all_jobs = indeed_jobs + naukri_jobs + linkedin_jobs
    print(f"✅ Total jobs collected: {len(all_jobs)}")

    if all_jobs:
        file = save_to_excel(all_jobs)
        send_email(file)
    else:
        print("❌ No jobs found today.")

if __name__ == "__main__":
    run()
