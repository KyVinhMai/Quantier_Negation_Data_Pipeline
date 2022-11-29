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

header = ["ID", "Title", "Quant", "Match","Context", "Speakers", "Date", "Link"] #todo will add standalone vs continous
quant_count = {
    "every": 0,
    "some": 0,
    "all": 0,
    "any": 0
}

found_sentences = []

quantifiers = ['every', "any", "all", "some"]

def segement_sentences(variable_amount: list[str]) -> list[str]:
    """
    Need to ensure that sentences are properly segmented
    """
    new_sentences= []
    for group in variable_amount:
        doc = nlp(group)
        for line in doc.sents:
            new_sentences.append(" " + line.text)

    return new_sentences


def validate_quant_neg(article_url: str, extract_transcript, extract_meta_data ) -> int:
    """
    article_url: actual url to website
    extract_transcript: function
    extract_meta_data: function
    """
    articles = 0
    clauses = 0
    ID = 400

    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        sentences = segement_sentences(extract_transcript(soup))

        quants, matches, indices = qn.find_quantifier_negation(sentences, quantifiers)
        if matches:
            context = qn.get_context(sentences, indices)
            #todo grab audiofile
            title, date = extract_meta_data(soup)
            print(f" + Found an Article '{title}' with {quants} \n")

            for i in range(len(quants)):

                for quant in quant_count.keys(): #Adds to quant_count
                    if quant in quants[i]:
                        quant_count[quant] += 1

                found_sentences.append([ID, title, quants[i], matches[i], context, "Ratatouie", date, article_url])
                ID += 1

        articles += 1
        clauses += count_clauses(sentences)

    #Custom except for finding no quantifier negations
    except AttributeError:
        print('Issue with')
        print("ARTICLE URL")
        print(article_url)

    return clauses

def write_csv():
    with open('../NPR_quantneg_sentences.csv', 'w', newline='', encoding='UTF8') as f:
        csv_writer = writer(f)
        csv_writer.writerow(header)
        for sent in found_sentences:
            csv_writer.writerow(sent)

def main() -> int:
    clauses = 0
    links = []
    with open("hodge_podge_list.txt", "r") as file:
        for line in file:
            links.append(line.rstrip('\n'))

    for link in links:
        clauses = validate_quant_neg(link, npr.extract_transcript, npr.extract_metadata)

    return clauses


def crawl_NPR_archives():
    clauses = 0
    try:
        clauses = main()
    except Exception as e:
        print(e, ">>>>>>>>>>>>>>> Main function failed! <<<<<<<<<<<<<<<<<<<<<<")
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
        Any Counts: {quant_count['any']}
        All Counts: {quant_count['all']}

        Total sentences = {len(found_sentences)}
        --------------------------------------------------
        In total, parsed through {clauses} clauses!

        """

    print(presentation_stats)
    print("Webcrawler Complete!")

if __name__ == "__main__":
    crawl_NPR_archives()