import sqlite3
import pyaudio
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

def query_text(cursor):
    table_data = cursor.execute('''SELECT url FROM qn_sentences;''')
    return table_data

def split_audio():
    pass

def localize_segment():
    pass

