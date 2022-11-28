import selenium
from csv import writer
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

def scroll(url: str):
    driver.get(url)
    SCROLL_PAUSE_TIME = 10

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(6):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("Scrolled all the way to the bottom!")

    page_source = driver.page_source

    return page_source

def grab_daylinks(day_link: str) -> set[str]:
    npr_links = set()
    page = requests.get(day_link)
    day = BeautifulSoup(page.content, "html.parser")
    for transcript in day.find_all("li", {"class": "audio-tool audio-tool-transcript"}):
        npr_links.add(transcript.find('a').get('href'))

    return npr_links

def grab_month_links(month_link: str) -> set[str]:
    npr_links = set()
    page_source = scroll(month_link) #Scroll all the way to the bottom before grabbing the links
    month = BeautifulSoup(page_source.content, "html.parser")
    episode_list = month.find(id="episode-list")

    for article in episode_list.find_all("h2", {"class": "program-show_title"}):
        time.sleep(3)
        try:
            npr_links.union(grab_daylinks(article.find('a').get('href')))
            print("="*45)
            print("Grabbed a bunch of day links!")
            print("="*45)
        except Exception as e:
            print(e, ">>>>> DAY links <<<<< failed!")

    return npr_links

def search_months(year_list: list) -> set[str]:
    npr_links = set()
    main_link = "https://www.npr.org/"
    for year in year_list[:13]: #Ends at 2009
        print(f"Going into year: {year}")

        for link in year.find_all('li'): #Find months
            time.sleep(5)
            try:
                npr_links.union(grab_month_links(main_link + link.a.get("href")))
                "We put link.a to get the descendent of <li>"
                print("+"*45)
                print("Grabbed a bunch of MONTH links!")
                print("+"*45)
            except Exception as e:
                print(e, ">>>> MONTH link <<< Failed!")

    return npr_links

def main():
    "Under <main>, <section id = main-section>"
    archive_container = soup.find("nav", {"class": "archive-nav"})
    years = archive_container.find_all("div")[1:] #Remove year 2022 as it has no handwritten transcripts
    """
    Grabs all the years in archive
    """
    npr_links = search_months(years)

    with open('../NPR_scraped_links.csv', 'w', newline='', encoding='UTF8') as f:
        csv_writer = writer(f)
        for sent in npr_links:
            csv_writer.writerow(sent)


time.sleep(10)
driver.quit()