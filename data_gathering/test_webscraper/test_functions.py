import requests
from bs4 import BeautifulSoup
import string


url = "https://www.npr.org/programs/all-things-considered/2018/12/31/681120133?showDate=2018-12-31"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
for episode_transcript in soup.find_all("h3", {"class": "rundown-segment__title"}):
    link = episode_transcript.find('a').get('href')
    print(link)