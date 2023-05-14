import quant_neg_detection.dependency_patterns as dp
import en_core_web_trf
import quant_neg_detection.Quantifier_Phrase_Segmentation as qps
import spacy
from spacy.tokens.doc import Doc
from spacy.matcher import DependencyMatcher
spacy.prefer_gpu()
nlp = en_core_web_trf.load(exclude=["lemmatizer"])
print('INFO: spaCy initialized successfully.')
# Quantifier Negation Sentence Identifier

"Initialize Dependency Matcher"
dependency_matcher = DependencyMatcher(nlp.vocab)
dependency_matcher.add("find aux sentence type", [dp.aux_pattern])
dependency_matcher.add("find ccomp sentence type", [dp.ccomp_pattern])


def get_quantifier(sentence: str, quantifiers: list[str]) -> tuple[Doc, str, str, str] or None:
    def get_negation(doc: Doc) -> int:
        """
        Splits the sentence in half up till the negation. Helps with computation and preventing QPS
        from grabbing of multiple unintended quantifiers.
        """
        neg_matcher = DependencyMatcher(nlp.vocab)
        neg_matcher.add("find neg particle", [dp.neg_pattern])
        matches = neg_matcher(doc)

        if matches:
            match_id, token_ids = matches[-1] #Matches is [-1] to grab the latest negation.
            return token_ids[0]

    doc = nlp(sentence)

    for token in doc:
        for quantifier in quantifiers:

            if quantifier in token.text.lower():
                neg_index = get_negation(doc) #Making the assumption that the quantifier comes before the negation

                if neg_index:
                    quant_text = qps.find_quantifier_category(token, quantifier, doc[:neg_index])

                    if quant_text: #Get the splice of the sentence before negation
                        return token, quantifier, doc[:neg_index], quant_text

    return None, None, None, None

def dependency_exists(sentence: str, quant_segment: str):
    debugging = False
    doc = nlp(sentence)
    matches = dependency_matcher(doc)
    quant_segment = quant_segment.split(" ")

    if matches:
        for match in matches: # Looks through all case of matches
            match_id, token_ids = match
            noun_subject_index = token_ids[1]

            if debugging:
                    print("-"*36)
                    print(token_ids)
                    for i in range(len(token_ids)):
                        print(dp.aux_pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
                    print("-" * 36)

            # if doc[noun_subject_index].text == token.text:
            #     return True

            if doc[noun_subject_index].text in quant_segment:
                return True

            else:
                pass

    return False

def is_standalone(sentence, quantifiers):
    pass

def find_quantifier_negation(sentences: list[str], quantifiers) -> tuple[list, list, list]:
    print('INFO: Beginning search for quantifier + negation statements.')
    print("=" * 60, "\n")
    quants = []; sents = []; standalone = []; indices = []; errors = []
    i = 0

    for candidate in sentences:
        token, quant, neg_fragment, quant_text = get_quantifier(candidate, quantifiers)
        if token is not None and dependency_exists(candidate, quant_text):
            quants.append(quant_text) #todo change into quantifier category
            sents.append(candidate)
            indices.append(i)

            i = i+1
            print(">>>>>> ", candidate, "<<<<<<<")

    print("\n", "="*60)
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

    return " ".join(ret)

#For Testing
def is_quantifier_negation(sentence: str, quantifiers: list[str]) -> bool:
    token, quantifier, neg_index, quant_text = get_quantifier(sentence, quantifiers)
    if token is None:
        return False

    return dependency_exists(sentence, quant_text)



if __name__ == '__main__':
    sentence = ["And right now, well, I have to begin with a confession: I love maps.", " Because everybody who knew her and her kids thought she was highly devoted to them and can not conceive of her leaving her kids for any reason whatsoever. "]
    no_sentence = ["No! That isn't right."]
    some_sentence = ['some of us might not notice']
    every_sentence = ["everyone else's fairy tale story - mine - really wasn't quite what they thought it was-"]
    any_sentence = ["Xi Jinping wants to make it very clear that he's not going anywhere and that people shouldn't spend time speculating about who comes next."]
    print(find_quantifier_negation(any_sentence, ["any"]))

