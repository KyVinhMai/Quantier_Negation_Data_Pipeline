from utils.preprocessing_functions import split_rm_punct

def minimum_word_length(segment:[str], sentence_target:[str], first_word:str) -> bool:
    """
    Assumptions:
        > Whisper will have accurate transcription, but the punctuation marks
        are inaccurate
        > Periods will either be commas or periods
        > The utterance itself is a sentence, so we just need to match a sentence
        to a sentence

    Both sentences should be processed, and punctuation marks should be removed

    Loops through both sentences simultaneously
    """
    index = segment.index(first_word)
    assert index is not None, "Index not found"

    result = True
    for i in range(len(sentence_target)):
        # print(f"<{sentence_target[i], segment[index]}>", "\n", "sentence:", segment, sentence_target)
        try:
            if sentence_target[i] != segment[index]:
                result = False
                break
        except IndexError:
            result = False
            break
        index += 1

    return result


def whisper_time_stamps(utterance: str, whisper_transcript: dict) -> tuple[float,float]:
    """
    Finds the sentence segment in the whisper transcript which contains the
    first word, and then matches the rest of the utterance sentence to the
    sentence.

    raw_result[segments] = list of dictionaries
    segment["text"]

    Ex.  {'
    id': 3,
    'seek': 0,
    'start': 20.56,
    'end': 28.16,
    'text': " City, the average rent is over $2,000. Vanessa and her mom also face other barriers, like credit's",
    'tokens': [4392, 11, 264, 4274, 6214, 307, 670, 1848, 17, 11, 1360, 13, 27928, 293, 720, 1225, 611, 1851, 661, 13565, 11, 411, 5397, 311],
    'temperature': 0.0,
    'avg_logprob': -0.17815227336711711,
    'compression_ratio': 1.628099173553719,
    'no_speech_prob': 0.06631708890199661
    }
    """
    first_word = utterance.lower().split()[0]
    for segment in whisper_transcript["segments"]:
        if first_word in segment["text"].lower():
            if minimum_word_length(split_rm_punct(segment['text']), split_rm_punct(utterance), first_word):
                return segment["start"] * 1000, segment["end"] * 1000

def whisper_context(context_target: list[str], whisper_transcript: dict):
    """
    Uses only the first sentence and last sentence of the target context.
    1 . Finds the inital time marker for the first sentence
    2. Finds the last time marker for the last sentence

    Returns those time markers together, assuming everything in between is
    within the context
    """
    first_sent = context_target[0].lower()
    first_word = first_sent.lower().split()[0]

    last_sent = context_target[-1].lower()
    last_word = last_sent[-1].lower()

    start_ts = None
    end_ts = None

    whisper_iter = iter(whisper_transcript["segments"])

    while start_ts is None:
        segment = next(whisper_iter)
        if first_word in segment["text"].lower():
            if minimum_word_length(split_rm_punct(segment['text']), split_rm_punct(first_sent), first_word):
                start_ts = segment["start"] * 1000

    while end_ts is None:
        segment = next(whisper_iter)
        if last_word in segment["text"].lower():
            if minimum_word_length(split_rm_punct(segment['text']), split_rm_punct(last_sent), first_word):
                end_ts = segment["start"] * 1000

    return start_ts, end_ts





