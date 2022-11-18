# Quantifier Negation Sentence Identifier
import spacy
from spacy.matcher import  DependencyMatcher
spacy.prefer_gpu()
import en_core_web_sm
import Quantifier_Phrase_Segmentation as qps
nlp = en_core_web_sm.load()
print('INFO: spaCy initialized successfully.')


def get_quantifier(sentence: str, quantifiers: list[str]):
    """
    sentence: Doc
    quantifiers: List of quantifiers
    returns: quantifier token
    """
    doc = nlp(sentence)

    for token in doc:
        for quantifier in quantifiers:
            if quantifier in token.text.lower():
                return qps.find_quantifier_category(token, quantifier, doc)

    return None

def dependency_exists(sentence):
    doc = nlp(sentence)
    debugging = False
    matcher = DependencyMatcher(nlp.vocab)
    aux_pattern = [
        {
            "RIGHT_ID": "anchor_is",
            "RIGHT_ATTRS": {"POS": "AUX"}
        },
        {
            "LEFT_ID": "anchor_is",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": "nsubj"},
        },
        {
            "LEFT_ID": "anchor_is",
            "REL_OP": ">",
            "RIGHT_ID": "negation_particle",
            "RIGHT_ATTRS": {"DEP": "neg"},
        },
        {
            "LEFT_ID": "anchor_is",
            "REL_OP": ">",
            "RIGHT_ID": "associated_word",
            "RIGHT_ATTRS": {"DEP": {"IN": ["amod", "compound"]}},
        }
    ]

    verb_pattern = [
        {
            "RIGHT_ID": "anchor_verb",
            "RIGHT_ATTRS": {"POS": "VERB"}
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "noun_subject",
            "RIGHT_ATTRS": {"DEP": "nsubj"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "aux_word",
            "RIGHT_ATTRS": {"DEP": "aux"},
        },
        {
            "LEFT_ID": "anchor_verb",
            "REL_OP": ">",
            "RIGHT_ID": "negation_word",
            "RIGHT_ATTRS": {"DEP": "neg", "POS": "PART"},
        }
    ]
    matcher.add("find aux sentence type", [aux_pattern])
    matcher.add("find verb sentence type", [verb_pattern])

    matches = matcher(doc)

    if debugging:
        match_id, token_ids = matches[0]
        print(token_ids)
        for i in range(len(token_ids)):
            print(verb_pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)

    if matches: #Truthy/ Falsy Value
        return True

    return False


def is_quantifier_negation(sentence: str, quantifiers: list[str]):
    if get_quantifier(sentence, quantifiers) is None:
        return False

    if dependency_exists(sentence):
        return True

    return False

def validate_quant_neg(transcript: list[str], quantifiers):
    for sentence in transcript:
        if is_quantifier_negation(sentence, quantifiers):
            return True

    return False

def is_standalone():
    pass

def find_quantifier_negation(sentences, quantifiers):
    print('INFO: Beginning search for quantifier + negation statements.')
    quants = []
    sents = []
    standalone = []
    i = 0
    indices = []
    for sentence in sentences:
        if is_quantifier_negation(sentence, quantifiers):
            quants.append(qps.find_quantifier_category(sentence, quantifiers, sentence)) #todo change into quantifier category
            sents.append(sentence)
            indices.append(i)
            print("> ", sentence)
            # standalone.append("True" if is_standalone(sentence, quantifiers) else "False")

        i = i+1

    print('INFO: Search completed with ' + str(len(sents)) + ' potential quantifier + negations.')
    print("\n")
    return quants, sents, indices

def get_context(sentences, indices):
    ret = []
    for index in indices:
        start = index - 3
        end = index + 2
        if start <= 0:
            start = 0
        elif end > len(sentences):
            end = len(sentences)
        for i in range(start, end):
            ret.append(sentences[i])
        ret.append('**********')
    return ret

if __name__ == '__main__':
    sentence = "everybody didn't have body armor"
    print(is_quantifier_negation(sentence, ['every', 'some', 'no']))
