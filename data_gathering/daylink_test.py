import time
import requests
from bs4 import BeautifulSoup

def grab_daylinks(day_link: str):
    npr_links = set()
    page = requests.get(day_link)
    day = BeautifulSoup(page.content, "html.parser")
    for transcript in day.find_all("li", {"class": "audio-tool audio-tool-transcript"}):
        npr_links.add(transcript.find('a').get('href'))

    return npr_links

print(grab_daylinks("https://www.npr.org/programs/all-things-considered/2021/11/30/1060185811/all-things-considered-for-november-30-2021?showDate=2021-11-30"))