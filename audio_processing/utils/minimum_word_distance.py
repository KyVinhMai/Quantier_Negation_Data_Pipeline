
def minimum_word_length(segment:[str], utterance:[str], first_word:str) -> bool:
    """
    Assumptions:
        > Whispher will have accurate transcription, but the punctuation marks
        are inaccurate
        > Periods will either be commas or periods
        > The utterance itself is a sentence, so we just need to match a sentence
        to a sentence

    Both sentences should be processed, and punctuation marks should be removed
    """
    print(utterance, segment)
    index = segment.index(first_word)
    if index == None:
        print("Index not found")
        return False

    result = True
    for i in range(len(utterance)):
        if utterance[i] != segment[index]:
            result = False
            break
        index += 1

    return result