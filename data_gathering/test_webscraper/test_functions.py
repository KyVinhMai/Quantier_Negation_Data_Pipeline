import requests
from bs4 import BeautifulSoup
import string
import unittest


# url = "https://www.npr.org/programs/all-things-considered/2018/12/31/681120133?showDate=2018-12-31"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")
# for episode_transcript in soup.find_all("h3", {"class": "rundown-segment__title"}):
#     link = episode_transcript.find('a').get('href')
#     print(link)

website_exceptions = []
with open("cursed_websites.txt", "r") as f:
    for line in f:
        website_exceptions.append(line.rstrip())

filetype_exceptions = []
with open("cursed_filetypes.txt", "r") as f:
    for line in f:
        filetype_exceptions.append(line.rstrip())


def check_url(url:str) -> bool:
    for web_exc in website_exceptions:
        if web_exc in url:
            return False

    return True

def check_filetype(url: str) -> bool:
    for exc in filetype_exceptions:
        if exc in url:
            return False

    return True



class Test_webscraper(unittest.TestCase):
    def test_check_url(self):
        incorrect_urls = ["https://www.npr.org/programs/all-things-considered/mpx/archive?date=8-31-2020",
                          "https://www.npr.org/programs/all-things-considered/archive?date=8-31-2020/rundowns/segment.php?",
                          "https://www.npr.org/programs/rundowns/segment.php?"]
        for url in incorrect_urls:
            self.assertFalse(check_url(url))
