import quant_neg_detection.dependency_patterns as dp
from quant_neg_detection.not_because_dependency_patterns import not_because_match_patterns, not_because_forbidden_patterns
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
# dependency_matcher.add("find aux sentence type", [dp.aux_pattern])
# dependency_matcher.add("find ccomp sentence type", [dp.ccomp_pattern])
# dependency_matcher.add("find xcomp sentence type", [dp.xcomp_pattern])
# dependency_matcher.add("find advmod pattern sentence", [dp.advmod_on_neg_pattern])
dependency_matcher.add("find all negations", dp.qn_patterns("all"))
# dependency_matcher.add("find all negations", dp.qn_patterns("every"))
# dependency_matcher.add("find all negations", dp.qn_patterns("each"))

# "Initialize Not-Because Dependency Matcher"
# not_because_matcher = DependencyMatcher(nlp.vocab)
# not_because_matcher.add("find match patterns", not_because_match_patterns)
# not_because_forbidden = DependencyMatcher(nlp.vocab)
# not_because_forbidden.add("find forbidden patterns", not_because_forbidden_patterns)

print("INFO: Dependency matchers initialized successfully.")

debugging = False

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
    doc = nlp(sentence)
    quant_segment = quant_segment.split(" ")

    # Hardcoding to weed out sentences with certain phrases
    forbidden_phrases = []

    if quant_segment[0].lower().startswith("all"):
        forbidden_phrases.append("y'all")

    for word in ["nearly", "almost", "most", "most of"]:
        forbidden_phrases.append(word + " " + quant_segment[0])

    forbidden_phrase_in_sentence = False
    for phrase in forbidden_phrases:
        if phrase in sentence.lower():
            forbidden_phrase_in_sentence = True

    if not forbidden_phrase_in_sentence:
        matches = dependency_matcher(doc)
    else:
        matches = False

    if matches:
        for match in matches: # Looks through all case of matches
            _, token_ids = match
            noun_subject_index = doc[token_ids[1]]

            if debugging:
                print("-"*36)
                print(token_ids)
                print(quant_segment)
                for i in range(len(token_ids)):
                    print(dp.aux_pattern[i]["RIGHT_ID"] + ":", doc[token_ids[i]].text)
                print("-" * 36)

            # if doc[noun_subject_index].text == token.text:
            #     return True

            if noun_subject_index.text in quant_segment \
                    and token_ids[1] < token_ids[0]:
                return True

    return False

def is_standalone(sentence, quantifiers):
    pass

def find_quantifier_negation(sentences: list[str], quantifiers) -> tuple[list, list, list]:
    print('INFO: Beginning search for quantifier + negation statements.')
    print("=" * 60, "\n")
    quants = []; sents = []; standalone = []; indices = []
    i = 0

    for candidate in sentences:
        token, quant, neg_fragment, quant_text = get_quantifier(candidate, quantifiers)
        if token is not None and dependency_exists(candidate, quant_text):
            quants.append(quant_text) #todo change into quantifier category
            sents.append(candidate)
            indices.append(i)

        i = i+1

    print("\n", "="*60)
    print('INFO: Search completed with ' + str(len(sents)) + ' potential quantifier + negations.')
    return quants, sents, indices

def get_context(sentences, indices) -> str:
    ret = []
    for index in indices:
        start = index - 4
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

# Jordan: function copied from NBI.py
def not_because_exists(doc: nlp) -> bool:
    """Ensure input sentence in nlp format has negation followed by "because" later in the sentence. """
    negation_i = -1
    because_i = -1
    doc_len = len(doc)
    # Get index of first negation
    for i, token in enumerate(doc):
        token_str = token.text.lower()
        if token_str == "not" or token_str == "n't":
            negation_i = i
            break
    # Get index of last because
    for i in range(doc_len - 1, -1, -1):
        token_str = doc[i].text.lower()
        if token_str == "because":
            because_i = i
            break
    if -1 < negation_i < because_i:
        return True
    else:
        return False

# Jordan: new function based on NBI.py lines 105-117
def not_because_dependency_exists(sentence: str):
    doc = nlp(sentence)
    match = not_because_matcher(doc) and not not_because_forbidden(doc) and not (
            "whether or not" in sentence) and not sentence.startswith(
            "Not because") and not_because_exists(doc)
    return match

# Jordan: Got rid of variables & function calls not needed for not-because.
# Jordan: Kept quants variable to prevent bugs down the line.
def find_not_because(sentences: list[str], quantifiers) -> tuple[list, list, list]:
    print('INFO: Beginning search for negation + because statements.')
    print("=" * 60, "\n")
    quants = []; sents = []; indices = []
    i = 0

    for candidate in sentences:
        if not_because_dependency_exists(candidate):
            quants.append("negation + because")
            sents.append(candidate)
            indices.append(i)

            i = i+1
            print(">>>>>> ", candidate, "<<<<<<<")

    print("\n", "="*60)
    print('INFO: Search completed with ' + str(len(sents)) + ' potential negation + because.')
    return quants, sents, indices


if __name__ == '__main__':
    sentence = ["And right now, well, I have to begin with a confession: I love maps.", " Because everybody who knew her and her kids thought she was highly devoted to them and can not conceive of her leaving her kids for any reason whatsoever. "]
    no_sentence = ["No! That isn't right."]
    anywhere_sentence = ["I mean, I don't think we'll ever feel comfortable with our kids being anywhere that isn't inside my home."]
    every_sentence = ["everyone else's fairy tale story - mine - really wasn't quite what they thought it was-"]
    any_sentence = ["Xi Jinping wants to make it very clear that he's not going anywhere and that people shouldn't spend time speculating about who comes next."]
    print(find_quantifier_negation(anywhere_sentence, ["anywhere"]))

