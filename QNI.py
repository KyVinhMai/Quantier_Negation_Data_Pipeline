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
                if qps.find_quantifier_category(token, quantifier, doc):
                    return token, quantifier

    return None

def dependency_exists(sentence):
    doc = nlp(sentence)
    debugging = True
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
                token, quant = get_quantifier(sentence, quantifiers)
                quants.append(qps.find_quantifier_category(token, quant, nlp(sentence))) #todo change into quantifier category
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
    sentence = ["And I spent the next several weeks, every night, calling people, telling them it's not today.", "everybody in a bathrobe ain't just getting a massage"]
    print(find_quantifier_negation(sentence, ['every', 'some', 'no']))
