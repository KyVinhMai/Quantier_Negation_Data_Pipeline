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

"SQL Database"
conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

"TOR SESSION"
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
session = tor.get_tor_session()
hub_url = "https://www.npr.org/programs/all-things-considered/archive?date=10-31-2020"
page = session.get(hub_url, headers = headers)
soup = BeautifulSoup(page.content, "html.parser")

def audio_to_dir(title:str, soup) -> str:
    """
    https://www.codingem.com/python-download-file-from-url/
    https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
    """
    audio_link = npr.grab_audio_link(soup)
    response = session.get(audio_link)
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
    page = session.get(day_link, headers = headers)
    day = BeautifulSoup(page.content, "html.parser")
    errors = []
    for transcript_page in day.find_all("li", {"class": "audio-tool audio-tool-transcript"}):
        try:
            link = transcript_page.find('a').get('href')
            page = session.get(link, headers=headers)
            article_soup = BeautifulSoup(page.content, "html.parser")

            transcript = nlp("".join(npr.extract_transcript(article_soup)))
            title = npr.extract_metadata(article_soup)
            audio_dir = audio_to_dir(title, article_soup)
            clauses = doc_count_clauses(transcript)
            #todo implement latest batch

            try:
                sql.export_Link(cursor, link, audio_dir, clauses, str(transcript.to_json()), 1, str(article_soup))
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

def grab_episode_list_links(month_link: str):
    page = session.get(month_link, headers = headers) # <-- await asyncio.gather_tasks()
    month_soup = BeautifulSoup(page.content, "html.parser")
    episode_list = month_soup.find(id="episode-list")

    for article in episode_list.find_all("h2", {"class": "program-show__title"}):
        time.sleep(20)
        try:
            grab_daylinks(article.find('a').get('href'))
            print("=" * 45)
            print("Grabbed a bunch of day links!")
            print("=" * 45)
        except requests.exceptions.ConnectionError as e:
            print("Connection refused by the server.. |DAY LINKS|")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(20)
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
    while("2009" not in scroll_link):
        time.sleep(20)
        month_soup = grab_episode_list_links(scroll_link) # <-- creates task
        scroll_link = main_link + new_scroll_link(month_soup)
        print(">Created new scroll link: ", {scroll_link})

def main():
    "Under <main>, <section id = main-section>"
    # grab_episode_list_links("https://www.npr.org/programs/all-things-considered/archive?date=2022-12-27&eid=1145553073")
    scroll_link = new_scroll_link(soup)
    get_scroll_links("https://www.npr.org/" + scroll_link)
    conn.close()

# async def get_page(session, url):
#     async with session.get(url) as r:
#         return await r.text()
#
# async def get_all(session, scroll_url: str):
#     tasks = []
#     main_link = "https://www.npr.org/"
#     while("2009" not in scroll_url):
#         task = asyncio.create_task(get_page(session, scroll_url))
#         tasks.append(task)
#         scroll_url = main_link + new_scroll_link(scroll_url)
#     results = await asyncio.gather(*tasks)
#     return results
#
# async def main(hub_url):
#     async with aiohttp.ClientSession() as session:
#         data = await get_all(session,hub_url)
#         return data

if __name__ == "__main__":
    main()
