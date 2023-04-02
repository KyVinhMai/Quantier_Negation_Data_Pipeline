import sqlite3
from pydub import AudioSegment
from mutagen.mp3 import MP3
from spacy.tokens import Doc
import math
import en_core_web_sm
import re
nlp = en_core_web_sm.load()

# conn = sqlite3.connect(r'D:\AmbiLab_data\quant_neg_data.db')
# cursor = conn.cursor()

def query_data(cursor) -> iter:
    table_data = cursor.execute('''SELECT transcript, utterance, context FROM links INNER JOIN qn_sentences qs ON links.link = qs.url;''')
    table_data = iter([line for line in table_data])
    return table_data

def write_audio(halved_audio: AudioSegment, audio_dir:str) -> str:
    title = audio_dir.split("\\")[-1].split(".")[0] + "_halved" + ".wav"
    halved_audio.export(title, format="wav")#todo check for wav
    return title

def segment_audio(audio_len: int) -> int:
    """
    Returns the middle of the audio duration
    """
    new_length = math.floor(audio_len / 2)

    return new_length * 1000

def split_audio(audio_dir:str, segment: int) -> AudioSegment:
    audio_len = math.floor(MP3(audio_dir).info.length)
    new_length = segment_audio(audio_len)

    audio_file = AudioSegment.from_mp3("npr_evictions.mp3") #todo change

    "if segment is 1, take the first half, else take the 2nd half"
    trimmed_audio =  audio_file[:new_length] if segment == 1 else audio_file[new_length:] #todo check if this correct

    return trimmed_audio

def localize_segment(row: tuple[str, str, str], utterance) -> int:
    """
    Finds the location of utterance by searching through the document

    Returns whether the utterance is in the first half of the audio by taking
    the average of the amount of sentences in the doc and splitting it.
    """
    doc_file = Doc(nlp.vocab).from_json(eval(row[0])) # is a string of the strung together sentences
    sentences = [str(sent) for sent in doc_file.sents]
    transcript_len = len(sentences)
    avg = math.floor(transcript_len / 2)
    index = sentences.index(utterance)

    return 2 if index > avg else 1

def transform_transcript(utterance:str, quant:str) -> tuple[str, int]:
    """
    The wav2vec model requires transcripts to be uppercase and have
    vertical lines between each word.

    Ex: FINANCIAL|HELP|IS|AVAILABLE

    The function also returns the location of the quantifier
    """
    utterance_list = re.sub(r'[!|?|.|,|[|]|]', '', utterance).split(" ")
    index = utterance_list.index(quant)
    transcript = "|".join([word.upper() for word in utterance_list])

    return transcript, index


if __name__ == "__main__":
    audio = MP3("test_file.mp3")
    print(audio.info.length)