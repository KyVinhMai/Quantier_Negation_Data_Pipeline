import ast
import re
import spacy
from spacy.tokens.doc import Doc
import en_core_web_trf
spacy.prefer_gpu()
nlp = en_core_web_trf.load(exclude=["lemmatizer"])

def load_jsondoc(json_transcript: str) -> list[str]:
    """
    Loads json nlp transcript and returns segmented sentences

    :param json_transcript:  str doc json object
    :return: sentences
    """
    doc_file = Doc(nlp.vocab).from_json(ast.literal_eval(json_transcript))
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