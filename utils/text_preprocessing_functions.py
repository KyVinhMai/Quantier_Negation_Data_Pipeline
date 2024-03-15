import ast
import re
import string
import spacy
from spacy.tokens.doc import Doc
import en_core_web_trf
spacy.prefer_gpu()
nlp = en_core_web_trf.load(exclude=["lemmatizer"])

def load_json(json_transcript: str, include_speaker_info=False) -> list[str]:
    """
    Loads json nlp transcript and returns segmented sentences

    :param json_transcript:  str doc json object
    :return: sentences
    """
    doc_file = Doc(nlp.vocab).from_json(ast.literal_eval(json_transcript))
    if include_speaker_info:
        sentences = [sent.text for sent in doc_file.sents if sent.text]
    else:
        sentences = [rm_nonlexical_items(sent.text) for sent in doc_file.sents]
        sentences = [sent for sent in sentences if sent]

    return sentences

def load(sentence: str) -> list[str]:
    doc_file = nlp(sentence)
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
    if text[0] == " ":
        text = text[1:]
    pattern = re.compile("(([A-Z]+(\-| )[A-Z]+)+(?:\, [A-Z]+)*|[A-Z]+)\:|\([^)]*\)")
    return re.sub(pattern, "", text)

def rm_punct(sentence:str) -> str:
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    sentence = sentence.lower()
    return sentence

def sanitize_whisper_transcript(transcript: dict) -> dict:
    #convert to regex and replace text strings with regex. 2 loops is too slow
    "Removes all punctuation in text components of the transcripts"
    segments = transcript["segments"]
    for index in range(len(segments)):

        segments[index]["text"] = rm_punct(segments[index]["text"])

        for i in range(len(segments[index]["words"])):
            segments[index]["words"][i]["text"] = rm_punct(segments[index]["words"][i]["text"])

    return transcript

def split_sentence_with_numbers(sentence):
    "Used for odd edge cases for whisper-ts word number pairing"
    words = sentence.split()
    result = []

    i = 0
    while i < len(words):
        # Check if the current word has a neighboring number
        if i < len(words) - 1 and re.match(r'\d+', words[i + 1]):
            result.append(words[i] + ' ' + words[i + 1])
            i += 2  # Skip the neighboring number
        else:
            result.append(words[i])
            i += 1

    return result