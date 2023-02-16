import selenium
import time
import requests
import sqlite3
import spacy
import os.path
import tor_session as tor
from bs4 import BeautifulSoup
from clause_counter import doc_count_clauses
import SQL_functions as sql
import NPR_webscraper as npr
spacy.prefer_gpu()
import en_core_web_sm
nlp = en_core_web_sm.load()
from selenium.webdriver.firefox.options import Options as options
from selenium.webdriver.firefox.service import Service

"SQL Database"
conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

"TOR SESSION"
session = tor.get_tor_session()
hub_url = "https://www.npr.org/programs/all-things-considered/archive?date=12-31-2021"
page = session.get(hub_url)
soup = BeautifulSoup(page.content, "html.parser")

#///////////////// Init binary & driver
new_driver_path = r'C:\Users\kyvin\SeleniumDrivers\geckodriver.exe'
new_binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

ops = options()
ops.add_argument('--disable-blink-features=AutomationControlled') #https://stackoverflow.com/questions/71885891/urllib3-exceptions-maxretryerror-httpconnectionpoolhost-localhost-port-5958
ops.binary_location = new_binary_path
serv = Service(new_driver_path)
driver = selenium.webdriver.Firefox(service=serv, options=ops)

def scroll(url: str):
    driver.get(url)
    SCROLL_PAUSE_TIME = 10

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(7):
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

def audio_to_dir(title:str, soup) -> str:
    """
    https://www.codingem.com/python-download-file-from-url/
    https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
    """
    audio_link = npr.grab_audio_link(soup)
    response = requests.get(audio_link, headers=headers)
    save_path = 'D:\AmbiLab_data\Audio\\'
    name_of_file = "_".join(title.split(" "))
    completeName = os.path.join(save_path, name_of_file + ".mp3")
    file1 = open(completeName, "wb")
    file1.write(response.content)
    file1.close()

    return completeName

def write_errors(errors: list):
    import csv
    with open('errors.csv', 'w') as file:
        writer = csv.writer(file)
        for i in errors:
            writer.writerow([i])

def grab_daylinks(day_link: str):
    num_of_links = 0
    page = session.get(day_link)
    day = BeautifulSoup(page.content, "html.parser")
    errors = []
    for transcript_page in day.find_all("li", {"class": "audio-tool audio-tool-transcript"}):
        try:
            link = transcript_page.find('a').get('href')
            page = session.get(link)
            article_soup = BeautifulSoup(page.content, "html.parser")

            transcript = nlp("".join(npr.extract_transcript(article_soup)))
            title = npr.extract_metadata(article_soup)
            audio_dir = audio_to_dir(title, article_soup)
            clauses = doc_count_clauses(transcript)
            #todo implement latest batch

            try:
                sql.export_Link(cursor, link, audio_dir, clauses, str(transcript.to_json()), 1, page)
                conn.commit()
                print("~", title)
            except sqlite3.Error as er:
                print("_" * 40)
                print("Article ~ link db:", title)
                print("@ SQL", (' '.join(er.args)), "@")
                print("_" * 40)

            num_of_links += 1
        except Exception as e:
            print("!ERROR!", link,"\n", e)
            errors.append((link,e))

    print(f" ++ Found {num_of_links} links from a day ++")

    if len(errors) == 0:
        write_errors(errors)
    tor.renew_connection()

def grab_month_links(month_link: str):
    tor.renew_connection()
    page_source = scroll(month_link) #Scroll all the way to the bottom before grabbing the links
    month = BeautifulSoup(page_source, "html.parser")
    episode_list = month.find(id="episode-list")

    for article in episode_list.find_all("h2", {"class": "program-show__title"}):
        time.sleep(15)
        try:
            grab_daylinks(article.find('a').get('href'))
            print("="*45)
            print("Grabbed a bunch of day links!")
            print("="*45)
        except requests.exceptions.ConnectionError as e:
            print("Connection refused by the server.. |DAY LINKS|")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(20)
            print("Was a nice sleep, now let me continue...")
            continue

def search_months(year_list: list):
    main_link = "https://www.npr.org/"
    for year in year_list[:13]: #Ends at 2009
        print(f"Going into year: {str(year)[:29]}")

        for link in year.find_all('li'): #Find months
            time.sleep(15)
            grab_month_links(main_link + link.a.get("href"))
            "We put link.a to get the descendent of <li>"
            print("+"*45)
            print("Grabbed a bunch of MONTH links!")
            print("+"*45)

def main():
    "Under <main>, <section id = main-section>"
    archive_container = soup.find("nav", {"class": "archive-nav"})
    years = archive_container.find_all("div")[1:] #Remove year 2022 as it has no handwritten transcripts
    """
    Grabs all the years in archive
    """
    search_months(years)
    conn.close()
    driver.quit() # Had to move driver here or else all connection is lost

if __name__ == "__main__":
    main()