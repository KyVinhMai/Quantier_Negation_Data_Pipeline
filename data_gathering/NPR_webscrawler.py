import selenium
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options as options
from selenium.webdriver.firefox.service import Service

hub_url = "https://www.npr.org/programs/all-things-considered/archive?date=12-31-2021"
page = requests.get(hub_url)
soup = BeautifulSoup(page.content, "html.parser")

#///////////////// Init binary & driver
new_driver_path = r'C:\Users\kyvin\SeleniumDrivers\geckodriver.exe'
new_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

ops = options()
ops.binary_location = new_binary_path
serv = Service(new_driver_path)
driver = selenium.webdriver.Firefox(service=serv, options=ops)

driver.get('https://www.npr.org/programs/all-things-considered/archive?date=12-31-2021')
SCROLL_PAUSE_TIME = 10

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

def grab_day_links(month_link: str):
    page = requests.get(month_link)
    month = BeautifulSoup(page.content, "html.parser")
    episode_list = month.find(id="episode-list")

    for article in episode_list.find_all("article", {"class": "program-segment"}):
        validate_quant_neg(article.find('a').get('href'))

def search_months(year_list: list):
    archive_container = soup.find("nav", {"class": "archive-nav"})
    years = archive_container.find_all("div")[1:] #Remove year 2022 as it has no handwritten transcripts
    search_months(years)
    main_link = "https://www.npr.org/"
    for year in year_list[:13]: #Ends at 2009

        print(f"Going into year: {year}")

        for link in year.find_all('li'):

            grab_day_links(main_link + link.a.get("href"))
        "We put link.a to get the descendent of <li>"


while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(10)
driver.quit()