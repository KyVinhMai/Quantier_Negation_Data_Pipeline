from pydub import AudioSegment
from mutagen.mp3 import MP3
import math
import re
from spacy.tokens import Doc
import en_core_web_sm
nlp = en_core_web_sm.load(disable = ['ner', 'lemmatizer'])
# Removing pipeline components allows spacy to run faster

def segment_audio(audio_len: int, amount:float) -> int:
    "Multiply by 1000 as AudioSegment measures in milliseconds"
    # new_length = math.floor(audio_len / amount)
    new_length = math.floor(audio_len * amount)

    return new_length * 1000

def splice_audio(audio_dir:str, loc: tuple[float,float]) -> AudioSegment:
    assert None not in loc, "Splice_audio: Location Indices have no value"
    audio_len = math.floor(MP3(audio_dir).info.length)
    audio_file = AudioSegment.from_mp3(audio_dir)

    def padding(loc: tuple[float,float]) -> list:
        indices = list(loc)
        indices[0] = indices[0] - 0.1 if not indices[0] - 0.1 < 0 else indices[0]
        indices[1] = indices[1] + 0.1 if not indices[1] + 0.1 > 1 else indices[1]
        return indices

    indices = padding(loc)
    start_ts = segment_audio(audio_len, indices[0])
    end_ts = abs(segment_audio(audio_len, indices[1]) - audio_len * 1000)
    trimmed_audio = audio_file[start_ts:end_ts]
    # if loc[0] <= 0.3 and loc[1] <= 0.3: # Split into first half
    #     split_length = segment_audio(audio_len, 2)
    #     trimmed_audio = audio_file[:split_length]
    #
    # elif loc[0] >= 0.7 and loc[1] >= 0.7: # Split into second half
    #     split_length = segment_audio(audio_len, 2)
    #     trimmed_audio = audio_file[split_length:]
    #
    # else: # Audio clips is somewhere in the middle. Split into middle third
    #     first_third = segment_audio(audio_len, 3)
    #     last_third = math.floor(audio_len * 0.6) * 1000
    #     trimmed_audio = audio_file[first_third:last_third]

    return trimmed_audio

def insert_vertical(utterance:str, quant:str) -> tuple[str, int]:
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

def split_rm_punct(sentence) -> list[str]:
    "Remove comma and periods. Also lowers the str"
    sentence = sentence.replace(",", "").replace(".", "")
    sentence = sentence.lower()
    return sentence.split()

def load_jsondoc(json_transcript) -> list[str]:
    """
    Loads json nlp transcript and returns segmented sentences

    :param json_transcript:  str doc json object
    :return: sentences
    """
    doc_file = Doc(nlp.vocab).from_json(eval(json_transcript))
    doc_file = nlp(rm_nonlexical_items(doc_file.text))
    sentences = [str(sent) for sent in doc_file.sents]

    return sentences

def sentencify(context: str) -> list[str]:
    """
    Loads json nlp transcript and returns segmented sentences

    :param context:  str doc json object
    :return: sentences
    """
    doc_file = nlp(rm_nonlexical_items(context))
    sentences = [str(sent) for sent in doc_file.sents]

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

