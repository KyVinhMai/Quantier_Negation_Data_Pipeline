import pytest
import pandas as pd
import en_core_web_sm
nlp = en_core_web_sm.load()
from audio_processing.audio_utils import audio_preprocessing_functions as pf, \
    localization_functions as lf
import sqlite3

df = pd.read_csv("allthingsconsidered_every_neg_TRUEHITS - allthingsconsidered_every_neg_hits.csv")

"SQL Database"
conn = sqlite3.connect(r'E:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()
def query_test_data(cursor, link) -> iter:
    table_data = cursor.execute(f'''SELECT transcript, utterance, context FROM links INNER JOIN qn_sentences qs ON links.link = qs.url WHERE link LIKE {link};''')
    table_data = iter([line for line in table_data])
    return table_data

def test_localize_context():


    data = query_test_data(cursor, link)
    for row in data:
        audio_dir = row[0]
        json_transcript = row[1]
        quant = row[2]
        utterance = row[3]
        context = row[4]

def test_transform_transcript_function():
    input = "the fox jumped over the lazy dog"
    correct = "THE|FOX|JUMPED|OVER|THE|LAZY|DOG"

    answer, _ = pf.insert_vertical(input, "the")
    print(answer)
    assert answer == correct

def test_rm_nonlexical():
    text1 = ""
    text2 = ""
    with open("../data/raw_text_1") as file:
        for line in file:
            text1 = line

    with open("../data/raw_text_2") as file:
        for line in file:
            text2 = line

    correct1 = "  Over the weekend, several buses from Texas arrived here in Washington. They dropped off  Inside a steamy home kitchen in northwest Washington, Ana Monge is busy making tamales. . Monge's been making hundreds of tamalesbuses. The immediate sensation was, like, how can I help? Coming to this country as  finding something better. It definitely hit home."
    correct2 = " All eyes turn to the Senate now. How quickly might they act?  Well, there are interesting dynamics at play in the Senate. Some Republicans and even progressives are not willing to support just one bill that forces the contract agreement, but they're inclined to support it if it comes with a bill to provide seven days of sick leave. Here's Missouri GOP Senator Josh Hawley."
    assert pf.rm_nonlexical_items(text1) == correct1
    assert pf.rm_nonlexical_items(text2) == correct2


