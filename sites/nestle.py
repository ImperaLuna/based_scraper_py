from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city
from getCounty import get_county

#Se creeaza o instanta a clasei Scraper
scraper = Scraper("https://www.nestle.ro/jobs/search-jobs?keyword=Romania&country=&location=&career_area=All")
rules = Rules(scraper)

company = {"company": "Nestle"}
finalJobs = list()

#Se extrag joburile
while True:
    #Se cauta joburile care au clasa jobs-card
    elements = rules.getTags("div", {"class":"jobs-card"})

    #Pentru fiecare job, se extrage titlul, link-ul, compania, tara si orasul
    for element in elements:
        job_title = element.find("a").text.replace("\t", "").replace("\r", "").replace("\n", "").replace("  ", "")
        job_link = element.find("a")["href"]
        remote = element.find("div", {"class": "jobs-type"}).text
        city = translate_city(element.find("div", {"class":"jobs-location"}).text.split(",")[0])
        county = get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city,
            "county": county,
            "remote": remote
        })

    #Se cauta butonul de next
    domain = "https://www.nestle.ro/jobs/search-jobs"
    try:
        #Daca exista butonul de next, se extrage link-ul si se pune in url-ul scraper-ului
        nextPage = rules.getTag("div", {"class":"pager__item--next"})
        nextPageLink = nextPage.find("a")["href"]
        scraper.url = domain + nextPageLink
    except:
        break

#Afiseaza numarul de joburi gasite
print(json.dumps(finalJobs, indent=4))

#Incarca datele in baza de date
loadingData(finalJobs, company.get("company"))