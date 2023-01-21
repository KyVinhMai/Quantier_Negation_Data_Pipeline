import sqlite3
# import pyaudio
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
cursor = conn.cursor()

def query_text(cursor) -> iter:
    table_data = cursor.execute('''SELECT audio_dir, utterance, context FROM links INNER JOIN qn_sentences qs ON links.link = qs.url;''')
    table_data = iter([line for line in table_data])
    return table_data

def split_audio():
    pass

def localize_segment():
    table_data = query_text(cursor)
    for row in table_data:
        dir = row[0]; utterance = row[1]; context = row[2]


