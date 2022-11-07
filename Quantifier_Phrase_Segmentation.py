import spacy
spacy.prefer_gpu()
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from argparse import doc, token
import en_core_web_sm
nlp = en_core_web_sm.load()

def is_quantifier_word(token, quantifier):
    if token.text.lower() == quantifier.text + "body":
        return token

    if token.text.lower() == quantifier.text + "thing":
        return token

    if token.text.lower() == quantifier.text + "one":
        return token

    return None

def is_quantifier_noun(word, sentence):
    """
    Detects if the quantifier is being applied to a noun.
    """
    index = 0
    for token in sentence:
        if word.text == token.text: #Can't find a better way to find the index
            index = token.i

    word_neighbor = sentence[index].nbor()

    #check for conjunctions
    "If there is a 'conj' and 'cc' in the depenencies of the children, it signifies a conjunction"
    if "conj" in [child.dep_ for child in word_neighbor.children]:
        for token in sentence:
            if token.dep_ == "conj":
                return sentence[index: token.i + 1]

    #Check for noun
    """
    Checks if the neighboring tokens are nouns or if it's ancestors are nouns.
    """
    ancestors_dep = [word.dep_ for word in sentence[index].ancestors]

    if 'nsubj' in ancestors_dep or 'nsubjpass' in ancestors_dep\
        and sentence[index].pos_ == "DET" and sentence[index].dep_ == "det":

            "Finds the noun that has the nsubj or nsubjpass dependency"
            for token in sentence:
                if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
                    return sentence[index: token.i + 1]

def is_quantifier_phrase(token, quantifier, sentence):
    adposition_word = nlp("of")[0]

    for token in sentence:
        if token.text == adposition_word.text and token.pos_ == "adv":

            if token.dep == "Prep" and token.children.dep_ == "pobj"\
                    and (token.children.pos_ == "PRON" or token.children.pos_ == "NOUN"):

                "Checks if the quantifier is to the left of the adposition_word"
                if quantifier.text in [word for word in token.lefts]: #Fix
                    pass


def find_quantifier_category(token, quantifier, sentence):
    """
    Sorts each quantifier in to...
    > Quantifier Compound = Everything, everybody, everyone
    > Quantifier Noun = Every {Parent, Dog, Cowboy}
    > Quantifier Phrase = Every one of them
    """

    if is_quantifier_word(token, quantifier):
        return token

sentence = nlp("Any Tomahawk missile does not hit-")
word = nlp("any")[0]
print(is_quantifier_noun(word, sentence))