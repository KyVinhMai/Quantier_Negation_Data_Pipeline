import tqdm
import requests
from csv import writer
from bs4 import BeautifulSoup
import QNI as qn
import NPR_webscraper as npr
from clause_counter import count_clauses
import spacy
spacy.prefer_gpu()
import en_core_web_sm
nlp = en_core_web_sm.load()

clauses = 0
ID = 400
header = ["ID", "Title", "Quant", "Match","Context", "Speakers", "Date", "Link"] #todo will add standalone vs continous
quant_count = {
    "every": 0,
    "some":0,
    "no":0
}

found_sentences = []

quantifiers = ['every']



hub_url = "https://www.npr.org/programs/all-things-considered/archive?date=12-31-2021"
page = requests.get(hub_url)
soup = BeautifulSoup(page.content, "html.parser")

def segement_sentences(variable_amount: list[str]) -> list[str]:
    new_sentences= []

    for group in variable_amount:
        doc = nlp(group)
        for line in doc.sents:
            new_sentences.append(line.text)

    return new_sentences



def validate_quant_neg(article_url: str) -> None:
    global ID
    global clauses #Cardinal Sins

    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        sentences = segement_sentences(npr.extract_transcript(soup))

        quants, matches, indices = qn.find_quantifier_negation(sentences, quantifiers)
        if matches:
            context = qn.get_context(sentences, indices)
            #todo grab audiofile
            title, date = npr.extract_metadata(soup)
            print(f"Found an Article '{title}' with {quants}")

            for i in range(len(quants)):

                for quant in quant_count.keys(): #Adds to quant_count
                    if quant in quants[i]:
                        quant_count[quant] += 1

                found_sentences.append([ID, title, quants[i], matches[i], context, "Ratatouie", date, article_url])
                ID += 1

        clauses += count_clauses(sentences)

    #Custom except for finding no quantifier negations
    except AttributeError:
        print('Issue with')
        print("ARTICLE URL")
        print(article_url)


def grab_day_links(month_link: str):
    page = requests.get(month_link)
    month = BeautifulSoup(page.content, "html.parser")
    episode_list = month.find(id="episode-list")

    for article in episode_list.find_all("article", {"class": "program-segment"}):
        validate_quant_neg(article.find('a').get('href'))

def search_months(year_list: list):
    main_link = "https://www.npr.org/"
    for year in year_list[:13]: #Ends at 2009

        print(f"Going into year: {year}")

        for link in year.find_all('li'):

            grab_day_links(main_link + link.a.get("href"))
        "We put link.a to get the descendent of <li>"

def write_csv():
    with open('NPR_quantneg_sentences.csv', 'w', encoding='UTF8') as f:
        csv_writer = writer(f)
        csv_writer.writerow(header)
        for sent in found_sentences:
            csv_writer.writerow(sent)

def main():
    archive_container = soup.find("nav", {"class": "archive-nav"})
    years = archive_container.find_all("div")[1:] #Remove year 2022 as it has no handwritten transcripts
    search_months(years)

def crawl_NPR_archives():
    try:
        main()
    except Exception as e:
        print(e, ">>>>>>>>>>>>> Main function failed! <<<<<<<<<<<<<<<<<<<<<<")
        pass

    try:
        write_csv()
    except:
        print("Shit whoops")

    presentation_stats = f"""
        Found Quantifiers
        --------------------------------------------------
        Every Counts: {quant_count['every']}
        Some Counts: {quant_count['some']}

        All sentences = {len(found_sentences)}
        --------------------------------------------------
        In total, parsed through {clauses} clauses!

        """

    print(presentation_stats)
    print("Webcrawler Complete!")

if __name__ == "__main__":
    crawl_NPR_archives()