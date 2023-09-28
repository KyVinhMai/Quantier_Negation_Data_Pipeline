import spacy
from spacy.tokens.doc import Doc
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

#todo list. Make sure no has no punctuation after
#Nobody who wears a blue coat, wasn't here.
def is_quantifier_word(token, quantifier: str) -> str or None:
    if token.text.lower() == quantifier + "body":
        return token.text

    if token.text.lower() == quantifier + "thing":
        return token.text

    if token.text.lower() == quantifier + "one":
        return token.text

    if token.text.lower() == quantifier + "where":
        return token.text

    if token.text.lower() == quantifier and token.pos_ == "PRON":
        return token.text

    return None

def find_index(token, doc: Doc) -> int or None:
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": token.text.lower()}]
    matcher.add("Word_index", [pattern])
    matches = matcher(doc)

    if matches:
        _, index, _ = matches[0]
        return index

    return None

def neighbor_is_adverb(token, index:int, doc: Doc) -> bool:
    """
    Rejects the if second word is adverb ex. Every now and then...
    """
    word_neighbor = doc[index].nbor()

    if word_neighbor.pos_ == "ADV" and token.pos_ == "advmod":
        return True

def possessive_exists(token, index:int, doc: Doc) -> str:
    neighbor = doc[index].nbor()

    """
    Checks to see if neighboring word is a possessive particle or has
    the else word next to it.
    """
    if (neighbor.dep_ == "case" and neighbor.pos_ == "PART") or \
            (neighbor.dep_ == "advmod" and neighbor.pos_ == "ADV"):
        poss_matcher = DependencyMatcher(nlp.vocab)
        poss_matcher.add("possessive_match", [dp.poss_pattern(token.text)])
        matches = poss_matcher(doc)

        if matches:
            _, anchors = matches[0]  # returns the indices of the anchors
            quant = anchors[1]
            poss_noun = anchors[0]
            return doc[quant:poss_noun + 1].text

    return token.text

def is_quantifier_noun(token, doc: Doc):#Todo use matcher to find the index
    """
    Detects if the quantifier is quantifying a noun.
    """
    #Check for noun
    det_matcher = DependencyMatcher(nlp.vocab)
    det_matcher.add("determiner_patter", [dp.det_pattern(token.text)])
    matches = det_matcher(doc)

    if matches:
        _, anchors = matches[0]
        quant = anchors[1]
        noun = anchors[0]
        return doc[quant:noun + 1].text

def is_quantifier_phrase(quantifier: str, doc: Doc):
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
    dep_matcher.add("quantifier_phrase", [dp.of_pattern(quantifier)])
    matches = dep_matcher(doc)
    if matches:
        _, token_id = matches[0] #token id returns the indices of the anchors
        phrase = doc[token_id[-1]:token_id[2] + 1].text #We want the span of the dependency
        return phrase

    return None

def find_quantifier_category(token, quantifier: str,  doc: Doc) -> str or None:
    """
    token: Word detected, which contains the quantifier inside the string
    quantifier: The quantifier we are searching for
    sentence: The sentence which the token was found in

    Sorts each quantifier in to...
    > Quantifier Compound = Everything, everybody, everyone
    > Quantifier Noun = Every {Parent, Dog, Cowboy}
    > Quantifier Phrase = Every one of them
    """

    index = find_index(token, doc)
    if index is None: return None;

    if neighbor_is_adverb(token, index, doc):
        return None

    if is_quantifier_word(token, quantifier):
        return possessive_exists(token, index, doc)
    else:
        check_noun = is_quantifier_noun(token, doc)

    if check_noun is not None:
        return check_noun
    else:
        return is_quantifier_phrase(quantifier, doc)

if __name__ == "__main__":
    sentence2 = nlp(" And not just the foldable, glove compartment variety, my living room wall features an enormous map of Europe and the poster of the famous New Yorker cover that shows Manhattan in close detail and everything west of it is")
    word = nlp("everything")[0]
    print(find_quantifier_category(word, "every", sentence2))

