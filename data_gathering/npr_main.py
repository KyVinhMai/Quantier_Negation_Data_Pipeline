import requests
from csv import writer
from bs4 import BeautifulSoup
import QNI as qn
import NPR_webscraper as npr
from clause_counter import count_clauses
import spacy
spacy.prefer_gpu()
import en_core_web_sm
from functools import partial
import sqlite3
nlp = en_core_web_sm.load()

conn = sqlite3.connect('AmbiLab_data.db')
cursor = conn.cursor()

quant_count = {
    "every": 0,
    "some": 0,
    "all": 0,
    "any": 0
}

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
            title, date = extract_meta_data(soup)
            audio = npr.grab_audio_link(soup)
            print(f" + Found an Article '{title}' with {quants} \n")

            for i in range(len(quants)):

                for quant in quant_count.keys(): #Adds to quant_count
                    if quant in quants[i]:
                        quant_count[quant] += 1

                #todo replace exception with exception duplicate.
                try:
                    found_sentences.append([ID, title, quants[i], matches[i], context, "Ratatouie", date, article_url])
                except Exception:
                    print("*"*60 + "\n", "Oop, duplicate already exists in QuantNeg Database\n", "*"*60 )
                ID += 1

        try:
            found_sentences.append([ID, title, quants[i], matches[i], context, "Ratatouie", date, article_url])
        except Exception:
            print("*" * 60 + "\n", "Oop, duplicate already exists in Links Database\n", "*" * 60)

        articles += 1
        clauses += count_clauses(sentences)

    #Custom except for finding no quantifier negations
    except AttributeError:
        print('Issue with')
        print("ARTICLE URL")
        print(article_url)

    return clauses


def main(links: list[str]) -> int:
    clauses = 0
    for link in links:
        clauses = validate_quant_neg(link, npr.extract_transcript, npr.extract_metadata)

    conn.commit()
    return clauses


def crawl_NPR_archives(file_name):
    links = []
    with open(file_name, "r") as file:
        for line in file:
            links.append(line.rstrip('\n'))

    clauses = 0
    try:
        clauses = main(links)
    except Exception as e:
        print(e, ">>>>>>>>>>>>>>> Main function failed! <<<<<<<<<<<<<<<<<<<<<<")
        pass

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
    crawl_NPR_archives("npr_links.txt")