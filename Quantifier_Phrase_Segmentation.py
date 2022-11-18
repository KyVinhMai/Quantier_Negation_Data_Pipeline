import spacy
from spacy.matcher import Matcher, DependencyMatcher
spacy.prefer_gpu()
import en_core_web_sm
nlp = en_core_web_sm.load()

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

def neighbor_is_adverb(token, sentence: nlp) -> bool:
    """
    Rejects the if second word is adverb ex. Every now and then...
    """
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": token.text.lower()}]
    matcher.add("Word_index", [pattern])

    _, index, _ = matcher(sentence)[0]
    word_neighbor = sentence[index].nbor()

    if word_neighbor.pos_ == "ADV" and token.pos_ == "advmod":
        return True

def is_quantifier_noun(word, sentence: nlp):#Todo use matcher to find the index
    """
    Detects if the quantifier is being applied to a noun.
    """
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": word.text.lower()}]
    matcher.add("Word_index", [pattern])

    _, index, _ = matcher(sentence)[0]
    word_neighbor = sentence[index].nbor()

    # Rejects the if second word is adverb ex. Every now and then...
    if word_neighbor.pos_ == "ADV":
        return None

    #check for conjunctions
    "If there is a 'conj' and 'cc' in the depenencies of the children, it signifies a conjunction"
    if "conj" in [child.dep_ for child in word_neighbor.children]:
        for token in sentence:
            if token.dep_ == "conj":
                return sentence[index: token.i + 1].text

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
                    return sentence[index: token.i + 1].text

def is_quantifier_phrase(quantifier: str, sentence: nlp):
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
    matcher = DependencyMatcher(nlp.vocab)
    pattern = [
        {
            "RIGHT_ID": "anchor",
            "RIGHT_ATTRS": {}
        },
        {
            "LEFT_ID": "anchor",
            "REL_OP": ">",
            "RIGHT_ID": "anchor_of",
            "RIGHT_ATTRS": {"DEP": "prep"},
        },
        {
            "LEFT_ID": "anchor_of",
            "REL_OP": ">",
            "RIGHT_ID": "noun_pronoun",
            "RIGHT_ATTRS": {"DEP": "pobj"},
        }
    ]
    matcher.add("quantifier_phrase", [pattern])
    matches = matcher(sentence)
    _, token_id = matches[0] #token id returns the indices of the anchors


    phrase = sentence[token_id[0]:token_id[-1] + 1].text #We want the span of the dependency

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
    else:
        check_noun = is_quantifier_noun(token, doc)

    if check_noun is not None:
        return check_noun
    else:
        return is_quantifier_phrase(quantifier, doc)

if __name__ == "__main__":
    #377,643
    sentence = nlp("And the weirdest thing - they're homesick. We want to think, oh, if you live in a horrible place that's had, you know, where your parents have died of starvation or where you're given dead-end jobs or where there's no food, many of these miss their homeland. And if you don't feel at home in Seoul or somewhere else, you're going to miss a place that everyone else on earth is going that's living hell, you should leave. But it's not a Hollywood ending, that's for sure, for them.  ")
    word = nlp("everyone")[0]
    print(find_quantifier_category(word, "every", sentence))