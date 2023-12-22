from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = "https://www.hcltech.com/romania/careers"

scraper = Scraper()
rules = Rules(scraper)

pgeNumber = 0

company = {"company": "HCLTechnologies"}
finalJobs = list()

while True:
    pagesQuery = url + f"?_wrapper_format=html&field_job_geography_value=All&field_designation_value_ers=&page={pgeNumber}"
    scraper.url = pagesQuery

    try:
        jobs = rules.getTag("div", {"class": "view-hcl-ers-career-jobs"}).find("tbody").find_all("tr")
    except:
        break

    for job in jobs:
        id = uuid.uuid4()
        job_title = job.find("td", {"class": "views-field-title"}).text.strip()
        job_link = "https://www.hcltech.com" + job.find("td", {"class": "views-field-title"}).find("a").get("href")
        city = job.find("td", {"class": "views-field-field-job-location"}).text.strip()

        finalJobs.append({
            "id": str(id),
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })

    pgeNumber += 1

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))
