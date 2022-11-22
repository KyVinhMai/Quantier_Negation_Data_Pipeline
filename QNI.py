# Quantifier Negation Sentence Identifier
import spacy
from spacy.matcher import DependencyMatcher
spacy.prefer_gpu()
import dependency_patterns as dp
import en_core_web_sm
import Quantifier_Phrase_Segmentation as qps
nlp = en_core_web_sm.load()
from csv import writer
print('INFO: spaCy initialized successfully.')


def get_quantifier(sentence: str, quantifiers: list[str]) -> tuple[str, str] or None:
    """
    sentence: Doc
    quantifiers: List of quantifiers
    returns: quantifier token
    """
    def get_negation(sentence: str) -> int:
        doc = nlp(sentence)
        neg_matcher = DependencyMatcher(nlp.vocab)
        neg_matcher.add("find neg particle", [dp.neg_pattern])
        matches = neg_matcher(doc)

        if matches:
            match_id, token_ids = matches[0]
            return token_ids[0]

    doc = nlp(sentence)

    for token in doc:
        for quantifier in quantifiers:
            if quantifier in token.text.lower():
                neg_index = get_negation(sentence)
                if neg_index:
                    if qps.find_quantifier_category(token, quantifier, doc[:neg_index]): #Get the splice of the sentence before negation
                        return token, quantifier, neg_index

    return None

def dependency_exists(sentence: str):
    doc = nlp(sentence)
    debugging = False

    dependency_matcher = DependencyMatcher(nlp.vocab)
    dependency_matcher.add("find aux sentence type", [dp.aux_pattern])
    dependency_matcher.add("find verb sentence type", [dp.verb_pattern])

    matches = dependency_matcher(doc)

    if debugging:
        if matches:
            match_id, token_ids = matches[0]
            print(token_ids)
            for i in range(len(token_ids)):
                print(dp.verb_pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)

    if matches: #Truthy/ Falsy Value
        return True

    return False


def link_quantifier_to_dep():
    pass

def is_quantifier_negation(sentence: str, quantifiers: list[str]) -> bool:
    if get_quantifier(sentence, quantifiers) is None:
        return False

    return dependency_exists(sentence)

def validate_quant_neg(transcript: list[str], quantifiers):
    for sentence in transcript:
        if is_quantifier_negation(sentence, quantifiers):
            return True

    return False

def is_standalone():
    pass

def find_quantifier_negation(sentences: list[str], quantifiers):
    print('INFO: Beginning search for quantifier + negation statements.')
    quants = []
    sents = []
    standalone = []
    i = 0
    indices = []
    errors = []
    for sentence in sentences:
        try:
            if is_quantifier_negation(sentence, quantifiers):
                token, quant, neg_index = get_quantifier(sentence, quantifiers)
                quants.append(qps.find_quantifier_category(token, quant, nlp(sentence)[:neg_index])) #todo change into quantifier category
                sents.append(sentence)
                indices.append(i)
                print(">>>>> ", sentence)
                # standalone.append("True" if is_standalone(sentence, quantifiers) else "False")

            i = i+1
        except IndexError as e:
            print("Error with", sentence)
            errors.append(f"{sentence} + {e}")
            print(e)


    with open('Sentence_issues.csv', 'w', encoding='UTF16') as f:
        csv_writer = writer(f)
        for line in errors:
            csv_writer.writerow(line)

    print('INFO: Search completed with ' + str(len(sents)) + ' potential quantifier + negations.')
    print("\n")
    return quants, sents, indices

def get_context(sentences, indices) -> str:
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
    return "".join(ret)

if __name__ == '__main__':
    sentence = ["everyone else's fairy tale story - mine - really wasn't quite what they thought it was-", "everybody in a bathrobe ain't just getting a massage"]
    print(find_quantifier_negation(sentence, ['every', 'some', 'no']))
