from bs4 import BeautifulSoup
import SQL_functions as sql
from typing import Type, Callable
from functools import partial
from utils.data_formatting import link_init, link_item
import sqlite3
import logging
import quant_neg_detection.QNI as QNI
from data_gathering.webcrawler import NPR_webscraper as npr

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

def validate_quant_neg(r: Type[link_item], extract_meta_data: Callable, ID: int):
    """
    article_url: actual url to website
    extract_transcript: function
    extract_meta_data: function
    """
    soup = BeautifulSoup(r.html, "html.parser")

    try:
        print(f"- Reading {r.link}")
        title = extract_meta_data(soup)

        # Jordan: Replace find_quantifier_negation with find_not_because when doing not-because sentences.
        quants, matches, indices = QNI.find_not_because(r.sentences, quantifiers)

        if matches:
            context = QNI.get_context(r.sentences, indices)
            print(f" + Found an Article '{title}' with {quants} \n")

            try:
                for i in range(len(quants)):
                    export_QN(ID, quants[i], "NONE", context, title, r.clauses, r.link, "NONE", matches[i])
                    conn.commit()

                    ID += 1

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
        logging.error(f"Issue with article: {r.link}")

    return ID

def main():
    data_iter = iter([row for row in sql.select_batch(cursor, conn)])
    ID = sql.QN_last_ID(cursor)

    articles = 0
    for link in data_iter:
        row = link_init(link)
        ID = validate_quant_neg(row, npr.extract_metadata, ID)
        articles += 1

    print(f"Read {articles} articles!")
    print("Quantifier-Negation Extraction Complete!")

if __name__ == "__main__":
    main()
