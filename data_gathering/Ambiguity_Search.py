from bs4 import BeautifulSoup
import SQL_functions as sql
from functools import partial
from utils.text_preprocessing_functions import *
import spacy
# spacy.require_gpu()
import en_core_web_sm
import sqlite3
import logging
import quant_neg_detection.QNI as QNI
nlp = en_core_web_sm.load()

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()
export_QN = partial(sql.export_QuantNeg, cursor)

"Logging Configuration"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s %(messages)s",
    filename="dependency_matching.log",
    filemode="w"
)

quantifiers = ['every', 'any', "some"] #todo clean this up

def validate_quant_neg(link_row: str, extract_meta_data, ID: int):
    """
    article_url: actual url to website
    extract_transcript: function
    extract_meta_data: function
    """
    article_url = link_row[0]; clauses = link_row[2]; doc_json_str = link_row[3]; html = link_row[-1]
    soup = BeautifulSoup(html, "html.parser")

    try:
        print(f"- Reading {article_url}")
        sentences = load_jsondoc(doc_json_str)
        title = extract_meta_data(soup)

        # Jordan: Replace find_quantifier_negation with find_not_because when doing not-because sentences.
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
    data_iter = sql.select_batch(cursor, conn)
    for row in data_iter:
        print(row)
    # ID = sql.QN_last_ID(cursor)
    # if ID == None:
    #     ID = 440
    # else:
    #     ID = ID[0]
    #
    # articles = 0
    # for link in data_iter:
    #     ID = validate_quant_neg(link, npr.extract_metadata, ID)
    #     articles += 1
    #
    # print(f"Read {articles} articles!")
    # print("Quantifier-Negation Extraction Complete!")

if __name__ == "__main__":
    main()
