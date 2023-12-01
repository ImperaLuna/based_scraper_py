from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city
from getCounty import get_county

url = " https://www.mazarscareers.com/ro/wp-admin/admin-ajax.php?action=get_job_listing_html&searchTerm=&form=contract%3D%26location%3D%26service%3D&amount=-1&location="

company = {"company": "Mazars"}
finalJobs = list()

scraper = Scraper()
rules = Rules(scraper)

scraper.url = url

html = scraper.getJson()
scraper.soup = html.get("html")

jobs = rules.getTags("article", {"class": "JobResult"})

for job in jobs:
    job_title = job.find("p", {"class":"job-title"}).text.strip()
    job_link = job.find("a").get("href")
    city = [translate_city(job.find_all("p")[1].text.split(":")[1].strip())]

    if not city[0]:
        city = ["Bucuresti", "Cluj-Napoca"]
    
    counties = [get_county(city) for city in city]
    
    finalJobs.append({
        "job_title": job_title,
        "job_link": job_link,
        "country": "Romania",
        "city": city,
        "county": counties,
        "company": company.get("company")
    })

print(json.dumps(finalJobs, indent=4))

loadingData(finalJobs, company.get("company"))

logoUrl = "https://www.mazarscareers.com/ro/wp-content/themes/mazars-2020/assets/images/mazars-logo.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))