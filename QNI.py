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
    returns: token, quantifier, neg_idex,  quant_orth
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
                neg_index = get_negation(sentence) #Making the assumption that the quantifier comes before the negation
                if neg_index:
                    quant_text = qps.find_quantifier_category(token, quantifier, doc[:neg_index])
                    if quant_text: #Get the splice of the sentence before negation
                        return token, quantifier, neg_index, quant_text

    return None, None, None, None

def dependency_exists(sentence: str, quant_segment: str):
    doc = nlp(sentence)
    debugging = False

    dependency_matcher = DependencyMatcher(nlp.vocab)
    dependency_matcher.add("find aux sentence type", [dp.aux_pattern])
    dependency_matcher.add("find verb sentence type", [dp.verb_pattern])

    matches = dependency_matcher(doc)

    if matches:
        for match in matches: # Looks through all case of matches
            match_id, token_ids = match
            noun_subject_index = token_ids[1]

            if debugging:
                    print("-"*36)
                    print(token_ids)
                    for i in range(len(token_ids)):
                        print(dp.verb_pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
                    print("-" * 36)

            if doc[noun_subject_index].text in quant_segment:
                return True

    return False

def is_quantifier_negation(sentence: str, quantifiers: list[str]) -> bool:
    token, quantifier, neg_index, quant_text = get_quantifier(sentence, quantifiers)
    if token is None:
        return False

    return dependency_exists(sentence, quant_text)

def validate_quant_neg(transcript: list[str], quantifiers):
    for sentence in transcript:
        if is_quantifier_negation(sentence, quantifiers):
            return True

    return False

def is_standalone():
    pass

def find_quantifier_negation(sentences: list[str], quantifiers=("every", "some", "all")):
    print('INFO: Beginning search for quantifier + negation statements.')
    print("=" * 60)
    quants = []
    sents = []
    standalone = []
    i = 0
    indices = []
    errors = []
    for sentence in sentences:
        try:
            if is_quantifier_negation(sentence, quantifiers):
                token, quant, neg_index, _ = get_quantifier(sentence, quantifiers)
                quants.append(qps.find_quantifier_category(token, quant, nlp(sentence)[:neg_index])) #todo change into quantifier category
                sents.append(sentence)
                indices.append(i)
                print(">>>>>> ", sentence, "<<<<<<<")
                # standalone.append("True" if is_standalone(sentence, quantifiers) else "False")

            i = i+1
        except IndexError as e:
            print("QNI Error with", sentence)
            errors.append(f"{sentence} + {e}")
            print(e)

        # if is_quantifier_negation(sentence, quantifiers):
        #     token, quant, neg_index, _ = get_quantifier(sentence, quantifiers)
        #     quants.append(qps.find_quantifier_category(token, quant, nlp(sentence)[
        #                                                              :neg_index]))  # todo change into quantifier category
        #     sents.append(sentence)
        #     indices.append(i)
        #     print(">>>>>> ", sentence, "<<<<<<<")
        #     # standalone.append("True" if is_standalone(sentence, quantifiers) else "False")

        # i = i + 1


    with open('Sentence_issues.csv', 'w', encoding='UTF16') as f:
        csv_writer = writer(f)
        for line in errors:
            csv_writer.writerow([line])

    print("="*60)
    print('INFO: Search completed with ' + str(len(sents)) + ' potential quantifier + negations.')
    return quants, sents, indices

def get_context(sentences, indices) -> str:
    ret = []
    for index in indices:
        start = index - 2
        end = index + 2
        if start <= 0:
            start = 0
        elif end > len(sentences):
            end = len(sentences)
        for i in range(start, end):
            ret.append(sentences[i])

    return "".join(ret)

if __name__ == '__main__':
    sentence = ["every one of those poor kids doesn't get the benefits that they have gotten before."]
    no_sentence = ["No! That isn't right."]
    print(find_quantifier_negation(sentence))
