import sqlite3
from pydub import AudioSegment
import spacy
from mutagen.mp3 import MP3
from spacy.tokens import Doc
import math
import en_core_web_sm
nlp = en_core_web_sm.load()

# conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
# cursor = conn.cursor()

def query_data(cursor) -> iter:
    table_data = cursor.execute('''SELECT transcript, utterance, context FROM links INNER JOIN qn_sentences qs ON links.link = qs.url;''')
    table_data = iter([line for line in table_data])
    return table_data

def write_audio(trimmed_audio: AudioSegment, audio_dir:str) -> str:
    title = audio_dir.split("\\")[-1].split(".")[0] + "_trimmed" + ".wav"
    trimmed_audio.export(title, format="wav")#todo check for wav
    return title

def segment_audio(audio_len: int, segment) -> int:
    """
    Splits the audio in different halves depending on where the sentence is located
    """
    if segment == 1:
        new_length = math.floor(audio_len / 2)
    else:
        new_length = audio_len - math.floor(audio_len / 2)

    return new_length

def split_audio(audio_dir:str, segment: int) -> AudioSegment:
    import os
    audio_len = math.floor(MP3(audio_dir).info.length)
    new_length = segment_audio(audio_len, segment)

    os.chdir("C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\audio_processing")
    audio_file = AudioSegment.from_mp3("npr_addiction.mp3") #todo change
    "if segment is 0, take the first half, else take the 2nd half"
    trimmed_audio =  audio_file[new_length:] if segment == 1 else audio_file[:new_length] #todo check if this correct

    return trimmed_audio

def localize_segment(row: tuple[str, str, str], utterance) -> int:
    """
    Finds if the utterance is in the first half of the audio by searching through
    the document
    """
    doc_file = Doc(nlp.vocab).from_json(eval(row[0]))
    sentences = list(doc_file.sents)
    transcript_len = len(sentences)
    avg = math.floor(transcript_len / 2)
    index = sentences.index(utterance)

    return 2 if index > avg else 1

if __name__ == "__main__":
    audio = MP3("test_file.mp3")
    print(audio.info.length)