import spacy
from spacy.matcher import Matcher, DependencyMatcher
spacy.prefer_gpu()
import en_core_web_sm
nlp = en_core_web_sm.load()

def is_quantifier_word(token, quantifier):
    if token.text.lower() == quantifier.text + "body":
        return token

    if token.text.lower() == quantifier.text + "thing":
        return token

    if token.text.lower() == quantifier.text + "one":
        return token

    if token.text.lower() == quantifier.text + "where":
        return token

    return None

def is_quantifier_noun(word, sentence):
    """
    Detects if the quantifier is being applied to a noun.
    """
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": word.text}]
    matcher.add("Word_index", [pattern]) # Use matcher to find the index

    _, index, _ = matcher(sentence)[0]
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

def is_quantifier_phrase(quantifier, sentence):
    """
    quantifier: token
    sentence: doc object

    Final check to validate if it is a quantifier.
    We're assuming now that the phrase takes the form of:

                            '[quantifier] of them...'

                Where quantifier = {Every one, Any, Some, etc.}

    And there is an adpositive word, 'of', referring to the pronoun.
    """
    for token in sentence:
        if token.text.lower() == "of" and token.pos_ == "ADP":

            if token.dep_ == "prep" and "pobj" in [child.dep_ for child in token.children]:

                "Checks if the quantifier is to the left of the adposition_word"
                if quantifier.text in sentence[:token.i].text:#todo make more efficient
                    for term in sentence:
                        if term.dep_ == 'pobj' and term.pos_ == ("NOUN" or "PRON"):
                            return sentence[token.i - 2: term.i + 1]


def find_quantifier_category(token, quantifier, sentence):
    """
    Sorts each quantifier in to...
    > Quantifier Compound = Everything, everybody, everyone
    > Quantifier Noun = Every {Parent, Dog, Cowboy}
    > Quantifier Phrase = Every one of them
    """
    #todo reject first round if second word is adverb? ... Every now and then

    if is_quantifier_word(token, quantifier):
        return token

sentence = nlp("every one of these organizations who have endorsed you did not agree with everything you did or every word you've spoken")
word = nlp("every")[0]
print(is_quantifier_phrase(word, sentence))