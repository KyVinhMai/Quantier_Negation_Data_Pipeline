import time
import asyncio
import requests
from aiohttp import ClientSession
import aiofiles
import sqlite3
import spacy
import os.path
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

async def audio_to_dir(session, title:str, soup: BeautifulSoup) -> str:
    """
    https://www.codingem.com/python-download-file-from-url/
    https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
    """
    audio_link = npr.grab_audio_link(soup)
    response = await session.get(audio_link)
    save_path = 'D:\AmbiLab_data\Audio\\'
    name_of_file = "_".join(title.split(" "))
    completeName = os.path.join(save_path, name_of_file + ".mp3")

    with open(completeName, "wb") as file1:
        file1.write(await response.read())

    return completeName

def write_errors(errors: list):
    import csv
    with open('errors.csv', 'w') as file:
        writer = csv.writer(file)
        for i in errors:
            writer.writerow([i])

async def gather_episodes(session: ClientSession, day_link: BeautifulSoup) -> list[tuple[str, BeautifulSoup]]:
    "Collects each episode transcript that was released in the associated day"
    tasks = []
    for episode_transcript in day_link.find_all("h3", {"class": "rundown-segment__title"}):
        link = episode_transcript.find('a').get('href')
        try:
            response = await session.get(link)
            html = await response.text()
            article_soup = BeautifulSoup(html, "html.parser")
            tasks.append((link, article_soup))
            print("~", link)
        except Exception as e:
            print("ERROR: in grabbing episode", link, "\n", e)

    return tasks

async def grab_day_catalogue_links(session: ClientSession, day_link: str):
    num_of_links = 0
    response = await session.get(day_link)
    html = await response.text()
    day = BeautifulSoup(html, "html.parser")

    errors = []
    soups = await gather_episodes(session, day)

    for link, article_soup in soups:
        try:
            transcript = nlp("".join(npr.extract_transcript(article_soup)))
            title = npr.extract_metadata(article_soup)
            audio_task = await audio_to_dir(session, title, article_soup)
            audio_dir = audio_task
            clauses = doc_count_clauses(transcript)
            #todo implement latest batch

            try:
                sql.export_Link(cursor, day_link, audio_dir, clauses, str(transcript.to_json()), 1, str(article_soup))
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
            errors.append((link, e))

    print(f"INFO: ++ Found {num_of_links} links from a day ++")

    if len(errors) != 0:
        write_errors(errors)

async def collect_section_list_links(month_link: str, session: ClientSession) -> BeautifulSoup:
    """
    Each scroll link leads to another section of the month catalogue.
    Typically these are just a 4-6 days ahead.
    """
    def collect_tasks(session: ClientSession, episode_list: BeautifulSoup) -> list:
        tasks = []
        for article in episode_list.find_all("h2", {"class": "program-show__title"}):
            try:
                day_links = article.find('a').get('href')
                tasks.append(asyncio.create_task(grab_day_catalogue_links(session, day_links)))
                # print("=" * 45)
                # print("Grabbed a bunch of day links!")
                # print("=" * 45)
            except requests.exceptions.ConnectionError as e:
                print("Connection refused by the server.. |DAY LINKS|")
                continue

        return tasks

    response = await session.get(month_link)
    html = await response.text()
    month_soup = BeautifulSoup(html, "html.parser")
    episode_list = month_soup.find(id="episode-list")

    tasks = collect_tasks(session, episode_list)
    await asyncio.gather(*tasks)

    return month_soup

def new_scroll_link(month_soup: BeautifulSoup) -> str:
    "At the end of main section in html, you can find the scroll link"
    sl = month_soup.find("div", "scrolllink").find('a').get('href')
    return sl

async def get_scroll_links(scroll_link):
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
        main_tasks = []
        async with ClientSession() as session:
            while ("2021" not in scroll_link):

                main_tasks.append(asyncio.create_task(collect_section_list_links(scroll_link, session)))

                "Getting the scroll link will occur in parallel"
                response = await session.get(scroll_link)
                html = await response.text()
                month_soup = BeautifulSoup(html, "html.parser")
                scroll_link = main_link + new_scroll_link(month_soup)
                print("> Created new scroll link! ", {scroll_link})

        await asyncio.gather(*main_tasks)

def main():
    start = time.time()

    scroll_link = "/programs/all-things-considered/archive?date=2022-12-27&eid=1145553073"
    asyncio.run(get_scroll_links("https://www.npr.org/" + scroll_link))
    conn.close()

    end = time.time()
    total_time = end - start
    print("It took {} seconds to complete the NPR webcrawler".format(total_time))
    print('You did it!')

if __name__ == "__main__":
    main()
    # async def foo():
    #     async with ClientSession() as session:
    #         page = await session.get("https://www.npr.org/2018/12/31/681286858/encore-the-history-of-government-shutdowns-in-the-u-s")
    #         html = await page.text()
    #         day = BeautifulSoup(html, "html.parser")
    #         await audio_to_dir(session, "testing", day)
    #
    # asyncio.run(foo())
