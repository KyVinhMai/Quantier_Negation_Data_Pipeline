from pydub import AudioSegment
from mutagen.mp3 import MP3
import math
import re
from spacy.tokens import Doc
import en_core_web_sm
nlp = en_core_web_sm.load()

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

def process_text(sentence) -> [str]:
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

def transform_string(context: str) -> list[str]:
    """
    Loads json nlp transcript and returns segmented sentences

    :param context:  str doc json object
    :return: sentences
    """
    doc_file = nlp(rm_nonlexical_items(context))
    sentences = [str(sent) for sent in doc_file.sents]

    return sentences

def rm_nonlexical_items(text):
    "Items like SOUNDBITE or speaker titles will be removed"
    pattern = re.compile("(([A-Z]+(\-| )[A-Z]+)+(?:\, [A-Z]+)*|[A-Z]+)\:|\([^)]*\)")
    return re.sub(pattern, "", text)


if __name__ == "__main__":
    print(rm_nonlexical_items("CHRISTOPHER-JOYCE: Along the coast of Fiji's big island, Viti Levu, resort hotels and small fishing villages share the same view of the wide, blue Pacific. You will find local musicians in both places. Music is a social lubricate, like the greeting, bula, which can mean many things but mostly everything is just fine. But everything isn't just fine. Fijians are noticing changes in their environment."))