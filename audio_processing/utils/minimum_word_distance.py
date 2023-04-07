from utils.preprocessing_functions import process_text

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


def whisper_time_stamps(utterance: str, whisper_transcript: dict) -> tuple[float,float]:
    """
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
            if minimum_word_length(process_text(segment['text']), process_text(utterance), first_word):
                return segment["start"] * 1000, segment["end"] * 1000

def whisper_context(target:[str], whisper_transcript: dict):
    first_sent = target[0].lower()
    for segment in whisper_transcript["segments"]:
        if first_sent in segment["text"].lower():
            pass