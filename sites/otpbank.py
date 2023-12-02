from scraper_peviitor import Scraper, Rules, loadingData
import json
from utils import translate_city
from getCounty import get_county, remove_diacritics

#Cream o instanta a clasei Scraper
scraper = Scraper("https://cariere.otpbank.ro/Posturi")
rules = Rules(scraper)

#Cautam numarul total de joburi
number_of_jobs = int(rules.getTag("div", {"class": "page-subtitle-counter"}).text.split(" ")[0])

#Cream o lista cu numerele de joburi de 10 in 10
pages = [*range(0, number_of_jobs, 10)]

company = {"company": "OTPBank"}
finalJobs = list()

#Pentru fiecare numar din lista, extragem joburile
for page in range(len(pages)):
    #setam link-ul paginii
    page_url = f"https://cariere.otpbank.ro/Posturi?page={page + 1}"
    scraper.url = page_url

    #Cautam elementele care contin joburile si locatiile
    elements = rules.getTags("div", {"class": "vacancy-item"})

    #Pentru fiecare job, extragem titlul, link-ul, compania, tara si orasul
    for element in elements:
        job_title = element.find("h2").find("a").text
        job_link = "https://cariere.otpbank.ro" + element.find("h2").find("a")["href"]

        try:
            city = translate_city(remove_diacritics(element.find("span", {"class": "more"}).text.split("-")[0].strip()))
        except:
            city = translate_city(remove_diacritics(element.find("span", {"class": "more"}).text))

        county = get_county(city)

        if not county:
            city = city.replace(" ", "-")
            county = get_county(city)

        finalJobs.append({
            "job_title": job_title,
            "job_link": job_link,
            "company": company.get("company"),
            "country": "Romania",
            "city": city
        })


#Afisam numarul total de joburi gasite
print(json.dumps(finalJobs, indent=4))

#Incarcam datele in baza de date
loadingData(finalJobs, company.get("company"))