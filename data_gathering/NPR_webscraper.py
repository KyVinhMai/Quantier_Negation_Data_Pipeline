import requests
from bs4 import BeautifulSoup
import string

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


def move_audio_to_harddrive(ID, soup):
    import os
    audio_link = grab_audio_link(soup)
    save_path = "D:\AmbiLab_data\Audio"
    name = str(ID) + ".mp3"
    with open(os.path.join(save_path, ID), "w") as file1:
        file1.write(audio_link.content)

def grab_audio_link(soup):
    """We can find the audio download button under wrapper > primary audio >
    audio-module-tools > audio-tool audio-tool-download ...."""
    audio_container = soup.find("li", class_ ="audio-tool audio-tool-download")
    attributes = audio_container.find("a")
    return attributes['href']

def extract_transcript(soup) -> list[str]:
    audio_tool_transcript = soup.find("li", class_="audio-tool audio-tool-transcript").a.get("href")

    page = requests.get(audio_tool_transcript, headers = headers)
    transcript_soup = BeautifulSoup(page.content, "html.parser")

    text_container = transcript_soup.find(class_ = "transcript storytext")
    text_tags = text_container.find_all("p")[:-2] # Last two lines are just disclaimers and copyright
    sentences = []
    for lines in text_tags:
        sentences.append(lines.text)

    return sentences

def extract_metadata(soup) -> str:
    title = soup.find("div", class_ = 'storytitle').get_text().strip("\n").strip("< ").translate(str.maketrans('', '', string.punctuation))
    # todo add speakers
    # date = soup.find("span", attrs={"class":"date"}).text.strip().split('/')[0]
    return title


if __name__ == "__main__":
    url = "https://www.npr.org/transcripts/141908779"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(extract_transcript(soup))


