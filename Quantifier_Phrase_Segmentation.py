import spacy
from spacy.matcher import Matcher, DependencyMatcher
spacy.prefer_gpu()
import en_core_web_sm
import dependency_patterns as dp
nlp = en_core_web_sm.load()

"""
The goal of the Quantifier Phrase Segmentation is to find the full quantifier 
phrase in length. This includes any possessive's or conjunctions. This is so that
the QNI can definitely say that the negation dependency is being applied to 
the quantifier itself
"""


def is_quantifier_word(token, quantifier: str) -> str or None:
    if token.text.lower() == quantifier + "body":
        return token.text

    if token.text.lower() == quantifier + "thing":
        return token.text

    if token.text.lower() == quantifier + "one":
        return token.text

    if token.text.lower() == quantifier + "where":
        return token.text

    return None

def find_index(token, doc: nlp) -> int:
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": token.text.lower()}]
    matcher.add("Word_index", [pattern])

    _, index, _ = matcher(doc)[0]

    return index

def neighbor_is_adverb(token, doc: nlp) -> bool:
    """
    Rejects the if second word is adverb ex. Every now and then...
    """
    index = find_index(token, doc)
    word_neighbor = doc[index].nbor()

    if word_neighbor.pos_ == "ADV" and token.pos_ == "advmod":
        return True

def possessive_exists(token, doc: nlp):
    index = find_index(token, doc)
    neighbor = doc[index].nbor()

    if neighbor.dep_ == "case" and neighbor.pos_ == "PART":
        return



def is_quantifier_noun(token, doc: nlp):#Todo use matcher to find the index
    """
    Detects if the quantifier is quantifying a noun.
    """
    index = find_index(token, doc)
    word_neighbor = doc[index].nbor()

    #check for conjunctions
    "If there is a 'conj' and 'cc' in the depenencies of the children, it signifies a conjunction"
    if "conj" in [child.dep_ for child in word_neighbor.children]:
        for token in doc:
            if token.dep_ == "conj":
                return doc[index: token.i + 1].text

    #Check for noun
    """
    Checks if the neighboring tokens are nouns or if it's ancestors are nouns.
    """
    ancestors_dep = [word.dep_ for word in doc[index].ancestors]

    if 'nsubj' in ancestors_dep or 'nsubjpass' in ancestors_dep\
        and doc[index].pos_ == "DET" and doc[index].dep_ == "det":

            "Finds the noun that has the nsubj or nsubjpass dependency"
            for token in doc:
                if token.dep_ == "nsubj" or token.dep_ == "nsubjpass":
                    return doc[index: token.i + 1].text

def is_quantifier_phrase(quantifier: str, doc: nlp):
    """
    quantifier: token
    sentence: doc object

    Final check to validate if it is a quantifier.
    We're assuming now that the phrase takes the form of:

                            '[quantifier] of them...'

                        quantifier = {Every one, Any, Some, etc.}

    And there is an adpositive word, 'of', referring to the pronoun.

    For each token
        1. Check that there is an "of" word, and it's speech tag is an "adposition"
        2. See that if that token then has a dependency of "prep" and that it extends a dependency
        of "pbj" to it's children
    """
    dep_matcher = DependencyMatcher(nlp.vocab)
    dep_matcher.add("quantifier_phrase", [dp.of_pattern])
    matches = dep_matcher(doc)
    _, token_id = matches[0] #token id returns the indices of the anchors


    phrase = doc[token_id[0]:token_id[-1] + 1].text #We want the span of the dependency

    return phrase if quantifier in phrase else quantifier + " " + phrase

def find_quantifier_category(token, quantifier: str,  doc: nlp) -> str or None:
    """
    token: Word detected, which contains the quantifier inside the string
    quantifier: The quantifier we are searching for
    sentence: The sentence which the token was found in

    Sorts each quantifier in to...
    > Quantifier Compound = Everything, everybody, everyone
    > Quantifier Noun = Every {Parent, Dog, Cowboy}
    > Quantifier Phrase = Every one of them
    """
    if neighbor_is_adverb(token, doc):
        return None

    if is_quantifier_word(token, quantifier):
        return token.text
        # return possessive_exists(token, doc)
    else:
        check_noun = is_quantifier_noun(token, doc)

    if check_noun is not None:
        return check_noun
    else:
        return is_quantifier_phrase(quantifier, doc)

if __name__ == "__main__":
    sentence = nlp("everyone's competing memoirs don't open up all the debates we've been talking about")
    word = nlp("everyone")[0]
    print(find_quantifier_category(word, "every", sentence))