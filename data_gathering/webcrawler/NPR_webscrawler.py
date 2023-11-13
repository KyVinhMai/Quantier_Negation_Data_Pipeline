import time
import requests
import sqlite3
import spacy
import os.path
from bs4 import BeautifulSoup
from clause_counter import doc_count_clauses
import data_gathering.SQL_functions as sql
from data_gathering.webcrawler import NPR_webscraper as npr
from data_gathering.other_utils import *

spacy.prefer_gpu()
import en_core_web_sm
import logging
import random
nlp = en_core_web_sm.load()

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
# hub_url = "https://www.npr.org/programs/all-things-considered/archive?date=12-31-2021"
# page = requests.get(hub_url, headers = headers)
# soup = BeautifulSoup(page.content, "html.parser")

"LOGGING"
logging.basicConfig(
    level=logging.INFO,
    filename= "nprwebcrawler_issues.log",
    filemode= "w"
)

def audio_to_dir(title:str, soup) -> str or None:
    """
    https://www.codingem.com/python-download-file-from-url/
    https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
    """
    audio_link = npr.grab_audio_link(soup)
    if check_filetype(audio_link):

        response = requests.get(audio_link)
        save_path = 'E:\\AmbiLab_data\\Audio\\'
        name_of_file = "_".join(title.split(" "))
        completeName = os.path.join(save_path, name_of_file + ".mp3")
        file1 = open(completeName, "wb")
        file1.write(response.content)
        file1.close()

    else:
        return None

    return completeName


def grab_daylinks(day_link: str):
    num_of_links = 0
    page = requests.get(day_link, headers = headers)
    day = BeautifulSoup(page.content, "html.parser")
    for transcript_page in day.find_all("li", {"class": "audio-tool audio-tool-transcript"}):

        if check_url(transcript_page.find('a').get('href')):

            try:
                link = transcript_page.find('a').get('href')
                page = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(page.content, "html.parser")

                transcript = nlp("".join(npr.extract_transcript(article_soup)))
                title = npr.extract_metadata(article_soup)
                audio_dir = audio_to_dir(title, article_soup)
                if audio_dir is None:
                    raise Exception("Audio Link did not work. Likely because of forbidden audio type")

                clauses = doc_count_clauses(transcript)
                #todo implement latest batch

                try:
                    sql.export_Link(cursor, link, audio_dir, clauses, str(transcript.to_json()), 2, str(article_soup), "Fresh Air")
                    conn.commit()
                    print("~", title)
                except sqlite3.Error as er:
                    print("_" * 40)
                    print("Article ~ link db:", title)
                    print("@ SQL ERROR", (' '.join(er.args)), "@")
                    print("_" * 40)

                num_of_links += 1
            except Exception as e:
                print("!ERROR!", link,"\n", e)
                logging.error(e, link)

        else:
            print("URL was in the list of exceptions")
            logging.info(link)

    print(f" ++ Found {num_of_links} links from a day ++")


def grab_episode_list_links(month_link: str):
    page = requests.get(month_link, headers = headers) # <-- await asyncio.gather_tasks()
    month_soup = BeautifulSoup(page.content, "html.parser")
    episode_list = month_soup.find(id="episode-list")

    for article in episode_list.find_all("h2", {"class": "program-show__title"}):
        time_num =random.randint(10, 30)
        time.sleep(time_num)
        print(f"Slept {time_num}")
        if check_url(article.find('a').get('href')):
            try:
                grab_daylinks(article.find('a').get('href'))
                print("=" * 45)
                print("Grabbed a bunch of day links!")
                print("=" * 45)
            except requests.exceptions.ConnectionError as e:
                print("Connection refused by the server.. |DAY LINKS|")
                print(f"Let me sleep for {time_num} seconds")
                print("ZZzzzz...")
                time.sleep(time_num)
                print("Was a nice sleep, now let me continue...")
                continue

    return month_soup

def new_scroll_link(month_soup) -> str:
    sl = month_soup.find("div", "scrolllink").find('a').get('href')
    return sl

def get_scroll_links(scroll_link):
    """
    The central hub the web crawler. Due to NPR's archive website, we need to
    sequentially grab the scroll link which allows us to progress to the next
    section of links.
    Hence the main goal of the while loop is to continously grab the next
    scroll link, but the subgoal is processing that year. We use
    asyncio.create_task() to push the processing of the html data to the
    background... so that the loop can continue get the next scroll link
    without interruption.
    """
    main_link = "https://www.npr.org/"
    while("=2008-" not in scroll_link):
        time_num = random.randint(10, 30)
        time.sleep(time_num)
        month_soup = grab_episode_list_links(scroll_link) # <-- creates task
        scroll_link = main_link + new_scroll_link(month_soup)
        print(">Created new scroll link: ", {scroll_link})

def main():
    "Under <main>, <section id = main-section>"
    # grab_episode_list_links("https://www.npr.org/programs/all-things-considered/archive?date=2022-12-27&eid=1145553073")
    scroll_link = "/programs/fresh-air/archive?date=2012-12-20&eid=167700597"
    get_scroll_links("https://www.npr.org/" + scroll_link)
    conn.close()


if __name__ == "__main__":
    main()