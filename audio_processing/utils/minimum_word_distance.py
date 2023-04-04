
def minimum_word_length(segment:[str], utterance_target:[str], first_word:str) -> bool:
    """
    Assumptions:
        > Whisper will have accurate transcription, but the punctuation marks
        are inaccurate
        > Periods will either be commas or periods
        > The utterance itself is a sentence, so we just need to match a sentence
        to a sentence

    Both sentences should be processed, and punctuation marks should be removed
    """
    index = segment.index(first_word)
    if index is None:
        raise Exception("Index not found")

    result = True
    for i in range(len(utterance_target)):
        if utterance_target[i] != segment[index]:
            result = False
            break
        index += 1

    return result