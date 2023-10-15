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

def extract_transcript(article_soup: BeautifulSoup) -> list[str]:
    text_container = article_soup.find(class_ = "transcript storytext")
    "Index 1 removes the sentence summary, Index -2 removes the disclaimers"
    text_tags = text_container.find_all("p")[1:-2]
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
    import spacy
    import en_core_web_sm
    spacy.prefer_gpu()
    nlp = en_core_web_sm.load()

    url = "https://www.npr.org/2012/03/27/149472829/trayvon-martins-death-sparks-difficult-conversations"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # with open("npr_trayvon_martin_transcript.txt", "w") as f:
    #     f.write(str(nlp("".join(extract_transcript(soup))).to_json()))

    # print(str(nlp("".join(extract_transcript(soup))).to_json()))

    print([str(sent) for sent in nlp("".join(extract_transcript(soup))).sents])


