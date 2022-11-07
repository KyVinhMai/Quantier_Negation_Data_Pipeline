import spacy
spacy.prefer_gpu()
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from argparse import doc, token
import en_core_web_sm
nlp = en_core_web_sm.load()


def is_quantifier_noun(word, sentence):
    index = 0
    for token in sentence:
        if word.text == token.text:
            index = token.i

    if sentence[index + 1].pos_ == "NOUN" and sentence[index].pos_== "DET" and sentence[index].dep_ == "det":
        return sentence[index: index+2]

def is_quantifier_word(token, quantifier):
    if token.text.lower() == quantifier + "body":
        return token

    if token.text.lower() == quantifier + "thing":
        return token

    if token.text.lower() == quantifier + "one":
        return token

    return None


def find_quantifier_category(token, quantifier, sentence):
    """
    Sorts each quantifier in to...
    #Quantifier Compound = Everything, everybody, everyone
    #Quantifier Noun = Every {Parent, Dog, Cowboy}
    #Quantifier Phrase = Every one of them
    :param token:
    :param quantifier:
    :param sentence:
    :return:
    """

    if is_quantifier_word(token, quantifier):
        return token

sentence = nlp("Every vote doesn't count")
word = nlp("every")[0]
print(is_quantifier_noun(word, sentence))