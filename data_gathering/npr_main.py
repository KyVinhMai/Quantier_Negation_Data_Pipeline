import requests
from bs4 import BeautifulSoup
import QNI as qn
import NPR_webscraper as npr
import SQL_functions as sql
import json
from spacy.tokens import Doc
import spacy
spacy.prefer_gpu()
import en_core_web_sm
from functools import partial
import sqlite3
import os.path
import argparse
nlp = en_core_web_sm.load()

conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()
export_QN = partial(sql.export_QuantNeg, cursor)

quantifiers = ['every', "any", "all", "some"]

link_table_keys = {
    "link": [0],
    "audio_dir": [1],
    "clauses": [2],
    "transcript":[3],
    "batches":[4]
}

def validate_quant_neg(link_row: str, extract_meta_data, ID: int):
    """
    article_url: actual url to website
    extract_transcript: function
    extract_meta_data: function
    """
    article_url = link_row[0], clauses = link_row[2], doc_json = json.loads(link_row[3])

    page = requests.get(article_url)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        transcript = Doc(nlp.vocab).from_json(doc_json)
        sentences = [sentence.text for sentence in transcript.sents]
        title = extract_meta_data(soup)

        quants, matches, indices = qn.find_quantifier_negation(sentences, quantifiers) #todo remove all text
        if matches:
            context = qn.get_context(sentences, indices)
            print(f" + Found an Article '{title}' with {quants} \n")

            try:
                for i in range(len(quants)):
                    export_QN(ID, quants[i], matches[i], context, title, clauses, article_url, "NONE")
                    conn.commit()
            except sqlite3.Error as er:
                print("_" * 40)
                print("Article ~ qn_sentences db:", title)
                print("@", (' '.join(er.args)), "@")
                print("_" * 40)

            ID += 1

    #Custom except for finding no quantifier negations
    except AttributeError:
        print('Issue with')
        print("ARTICLE URL")
        print(article_url)


def main(data_iter: iter):
    ID = sql.QN_last_ID(cursor)
    if ID == None:
        ID = 400

    for link in data_iter:
        validate_quant_neg(link, npr.extract_metadata, ID)

    conn.close()


def crawl_NPR_archives(batch_num):
    try:
        main(sql.select_batch(cursor, batch_num))
    except Exception as e:
        print(e, ">>>>>>>>>>>>>>> Main function failed! <<<<<<<<<<<<<<<<<<<<<<")

    print("Quantifier-Negation Extraction Complete!")

if __name__ == "__main__":
    crawl_NPR_archives(1) #<---------------------- Insert batch num
