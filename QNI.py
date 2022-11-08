# Quantifier Negation Sentence Identifier
import spacy
spacy.prefer_gpu()
import en_core_web_sm
import Quantifier_Phrase_Segmentation as qsp
nlp = en_core_web_sm.load()
print('INFO: spaCy initialized successfully.')


def get_quantifier(sentence, quantifiers: list[str]):
    """
    sentence: Doc
    quantifiers: List of quantifiers
    returns: quantifier token
    """
    doc = nlp(sentence)

    for token in doc:
        for quantifier in quantifiers:
            if quantifier in token.text.lower():
                return qsp.find_quantifier_category(token, quantifier, sentence)

    return None

def assoc_negation_exists(sentence, q_root) -> bool:
    """
    sentence: doc object
    q_root: token
    returns: bool
    """
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == 'neg':
            if (token.head.text == q_root.text and token.head.i == q_root.i) or (
                    token.head.head.text == q_root.text and token.head.head.i == q_root.i):
                return True
    return False


def get_q_root(quantifier):
    case_1 = ['nsubj', 'nsubjpass']
    case_2 = ['det', 'poss', 'advmod', 'nmod']
    dep = quantifier.dep_

    q_head = quantifier.head
    if dep in case_1:
        if q_head.dep_ == 'nsubj' or q_head.dep_ == 'auxpass':
            return q_head.head
        else:
            return q_head
    elif dep in case_2:
        return q_head.head


def reversed_traversal(sentence, quantifiers):
    """
    sentence: doc object
    """
    doc = nlp(sentence)
    negation = None
    for token in doc:
        if token.dep_ == 'neg' or token.dep_ == 'preconj':
            negation = token
    if negation == None:
        return False

    print(f"Negation: {negation}")
    ancestor = negation
    while ancestor != ancestor.head:
        ancestor = ancestor.head

    print(f"Ancestor: {ancestor}")
    for quantifier in quantifiers:

        if ancestor.dep_ == 'ROxOT' and quantifier in ancestor.text:
            return True
        for token in doc:
            if token.head == ancestor and quantifier in token.text and token.i < ancestor.i:
                return True

    return False


def is_quantifier_negation(sentence: str, quantifiers):
    quantifier = get_quantifier(sentence, quantifiers)
    if quantifier is None:
        return False
    if reversed_traversal(sentence, quantifiers):
        return True

    "Second Check"
    q_root = get_q_root(quantifier)
    print("Hello")
    print(q_root)
    if assoc_negation_exists(sentence, q_root):
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
            quants.append(get_quantifier(sentence, quantifiers).text) #todo change into quantifier category
            sents.append(sentence)
            indices.append(i)
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
