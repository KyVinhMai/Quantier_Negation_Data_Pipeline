import requests
from bs4 import BeautifulSoup
import QNI as qn
import NPR_webscraper as npr
from clause_counter import count_clauses
import SQL_functions as sql
import spacy
spacy.prefer_gpu()
import en_core_web_sm
from functools import partial
import sqlite3
import os.path
import argparse
nlp = en_core_web_sm.load()

conn = sqlite3.connect(r'C:\Users\kyvin\PycharmProjects\quant_neg_data.db')
cursor = conn.cursor()
export_QN = partial(sql.export_QuantNeg, cursor)
export_Links = partial(sql.export_Link, cursor)

quant_count = {
    "every": 0,
    "some": 0,
    "all": 0,
    "any": 0
}

quantifiers = ['every', "any", "all", "some"]

def segment_sentences(variable_amount: list[str]) -> list[str]:
    """
    Need to ensure that sentences are properly segmented
    """
    new_sentences= []
    for group in variable_amount:
        doc = nlp(group)
        for line in doc.sents:
            new_sentences.append(" " + line.text)

    return new_sentences

def increment_quant_count(quants):
    for i in range(len(quants)):
        for quant in quant_count.keys():  # Adds to quant_count
            if quant in quants[i]:
                quant_count[quant] += 1

def validate_quant_neg(article_url: str, extract_transcript, extract_meta_data, ID: int) -> int:
    """
    article_url: actual url to website
    extract_transcript: function
    extract_meta_data: function
    """
    articles = 0
    clauses = 0

    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        """
        After extracting sentences, check to see if there is a quantifier negation sentence.
        If there is, by checking that match is not none, we then grab all the
        necessary data to insert its values into the sql database. There is a 
        try and exception block just in case the sql function throws a duplicate
        error.
        """
        sentences = segment_sentences(extract_transcript(soup))
        json_document = nlp("".join(sentences)).to_json()
        title = extract_meta_data(soup)
        audio_dir = write_audio_to_dir(ID, soup)
        new_clauses = count_clauses(sentences)
        clauses += new_clauses

        try:
            export_Links(article_url, json_document, audio_dir, new_clauses)
        except sqlite3.Error as er:
                print("_" * 40)
                print("Article ~ link db:", title)
                print("@", (' '.join(er.args)), "@")
                print("_" * 40)

        quants, matches, indices = qn.find_quantifier_negation(sentences, quantifiers)
        if matches:
            #Add standalone function model
            context = qn.get_context(sentences, indices)
            print(f" + Found an Article '{title}' with {quants} \n")

            #todo replace exception with exception duplicate.
            try:
                for i in range(len(quants)):
                    export_QN(ID, quants[i], matches[i], context, title, article_url, clauses, "NONE")
                    conn.commit()
            except sqlite3.Error as er:
                print("_" * 40)
                print("Article ~ qn_sentences db:", title)
                print("@", (' '.join(er.args)), "@")
                print("_" * 40)

            increment_quant_count(quants)
            ID += 1

        conn.commit()
        articles += 1

    #Custom except for finding no quantifier negations
    except AttributeError:
        print('Issue with')
        print("ARTICLE URL")
        print(article_url)

    return clauses


def main(links: list[str]) -> int:
    clauses = 0
    ID = 400
    for link in links:
        clauses = validate_quant_neg(link, npr.extract_transcript, npr.extract_metadata, ID)

    conn.close()
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