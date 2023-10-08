from bs4 import BeautifulSoup
import NPR_webscraper as npr
import SQL_functions as sql
from spacy.tokens import Doc
import spacy
spacy.require_gpu()
import en_core_web_sm
from functools import partial
import sqlite3
import logging
import sys
sys.path.insert(0, r'D:\Research_Projects\Quantifer-Negation\Quantier_Negation_Data_Pipeline\quant_neg_detection')
import QNI
import json
import re

nlp = en_core_web_sm.load()

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()
export_QN = partial(sql.export_QuantNeg, cursor)

"Logging Configuration"
logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(levelname)s %(messages)s",
    filename= "dependency_matching.log",
    filemode= "w"
)

quantifiers = ['every', 'any', "some"] #todo clean this up

link_table_keys = {
    "link": [0],
    "audio_dir": [1],
    "clauses": [2],
    "transcript":[3],
    "batches":[4]
}

def rm_nonlexical_items(text: str) -> str:
    """
    Removes items like speaker, words inbetween parentheses, etc.
     examples:

     ANDREW LIMBONG, HOST:
     (SOUNDBITE OF MUSIC)
     RONALD DEIBERT:
     MICHEL MARTIN, BYLINE:
     (SOUNDBITE OF GENERATOR WHIRRING)TIM MAK, BYLINE:
    """
    pattern = re.compile("(([A-Z]+(\-| )[A-Z]+)+(?:\, [A-Z]+)*|[A-Z]+)\:|\([^)]*\)")
    return re.sub(pattern, "", text)


def validate_quant_neg(link_row: str, extract_meta_data, ID: int):
    """
    article_url: actual url to website
    extract_transcript: function
    extract_meta_data: function
    """
    article_url = link_row[0]; clauses = link_row[2]; doc_json = json.loads(link_row[3]); html = link_row[-1]
    soup = BeautifulSoup(html, "html.parser")

    #todo inefficient, why are we converting doc.text into the function if we already have the doc?
    try:
        print(f"- Reading {article_url}")
        transcript = Doc(nlp.vocab).from_json(doc_json)
        sentences = [rm_nonlexical_items(sentence.text) for sentence in transcript.sents]
        title = extract_meta_data(soup)

        quants, matches, indices = QNI.find_quantifier_negation(sentences, quantifiers) #todo remove all text
        if matches:
            context = QNI.get_context(sentences, indices)
            print(f" + Found an Article '{title}' with {quants} \n")
            try:
                for i in range(len(quants)):
                    export_QN(ID, quants[i], "NONE", context, title, clauses, article_url, "NONE", matches[i])
                    ID += 1
                    conn.commit()

            except sqlite3.Error as er:
                logging.error(
                f"""{'_'*40}
                Article ~ qn_sentences db: {title}
                SQL {(' '.join(er.args))}
                {'_'*40}""",
                exc_info=True
                )

    #Custom except for finding no quantifier negations
    except AttributeError:
        logging.error(f"Issue with article: {article_url}")

    return ID

def main():
    data_iter = iter([row for row in sql.select_batch(cursor, conn, batch_num="2")])
    ID = sql.QN_last_ID(cursor)
    if ID == None:
        ID = 440
    else:
        ID = ID[0]

    articles = 0
    for link in data_iter:
        ID = validate_quant_neg(link, npr.extract_metadata, ID)
        articles += 1

    print(f"Read {articles} articles!")


def crawl_NPR_archives(batch_num):
    # main(sql.select_batch(cursor, conn, batch_num))
    # main()
    main()
    print("Quantifier-Negation Extraction Complete!")

if __name__ == "__main__":
    crawl_NPR_archives("1") #<---------------------- Insert batch num
