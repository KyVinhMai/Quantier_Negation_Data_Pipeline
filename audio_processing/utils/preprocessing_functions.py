from pydub import AudioSegment
from mutagen.mp3 import MP3
import math
import re
from spacy.tokens import Doc
import en_core_web_sm
nlp = en_core_web_sm.load(disable = ['ner', 'lemmatizer'])
# Removing pipeline components allows spacy to run faster

def segment_audio(audio_len: float, amount:float) -> int:
    "Multiply by 1000 as AudioSegment measures in milliseconds"
    new_length = math.floor(audio_len * amount)

    return new_length * 1000

def return_audio_len(audio_dir: str) -> float:
    "Returns the duration of the audio file in seconds"
    audio_len = math.floor(MP3(audio_dir).info.length)
    return audio_len

def splice_audio(audio_dir:str, audio_len: float, loc: tuple[float,float]): #-> AudioSegment:
    assert None not in loc, "Splice_audio: Location Indices have no value"
    audio_file = AudioSegment.from_mp3(audio_dir)

    def padding(loc: tuple[float, float]) -> list:
        indices = list(loc)
        indices[0] = indices[0] - 0.1 if not (indices[0] - 0.1) < 0 else indices[0]
        indices[1] = indices[1] + 0.1 if not (indices[1] + 0.1) > 1 else indices[1]
        return indices

    indices = padding(loc)
    start_ts = segment_audio(audio_len, indices[0])
    end_ts = segment_audio(audio_len, indices[1])
    trimmed_audio = audio_file[start_ts:end_ts]

    return trimmed_audio

def insert_vertical(utterance: str = None, context: str = None, quant: str = None) -> tuple[str, int] or str:
    """
    The wav2vec model requires transcripts to be uppercase and have
    vertical lines between each word.

    Ex: FINANCIAL|HELP|IS|AVAILABLE

    The function also returns the location of the quantifier
    """
    if utterance and quant:
        utterance_list = re.sub(r'[!|?|.|,|[|]', '', utterance).split(" ") # Removes punctuation
        index = utterance_list.index(quant)
        transcript = "|".join([word.upper() for word in utterance_list])

        return transcript, index

    else:
        context_list = re.sub(r'[!|?|.|,|[|]', '', context).split(" ")  # Removes punctuation
        transcript = "|".join([word.upper() for word in context_list])
        return transcript

def split_rm_punct(sentence) -> list[str]:
    "Remove comma and periods. Also lowers the str"
    sentence = sentence.replace(",", "").replace(".", "")
    sentence = sentence.lower()
    return sentence.split()

def load_jsondoc(json_transcript: str) -> list[str]:
    """
    Loads json nlp transcript and returns segmented sentences

    :param json_transcript:  str doc json object
    :return: sentences
    """
    doc_file = Doc(nlp.vocab).from_json(eval(json_transcript))
    sentences = [rm_nonlexical_items(sent.text) for sent in doc_file.sents]
    sentences = [sent for sent in sentences if sent]

    return sentences

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

