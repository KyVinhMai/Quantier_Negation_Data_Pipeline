from pydub import AudioSegment
import math
from utils.minimum_word_distance import minimum_word_length
from utils.preprocessing_functions import process_text

def whisper_time_stamps(utterance: str, raw_result: dict) -> tuple[float,float]:
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
    for segment in raw_result["segments"]:
        if first_word in segment["text"].lower():
            if minimum_word_length(process_text(segment['text']), process_text(utterance), first_word):
                return segment["start"] * 1000, segment["end"] * 1000

def context_whisper_time_stamps(context):
    pass

def extract_sentence(start:float, end:float, audio_name: str) -> AudioSegment:
    "Segments the audio given the timestamps"
    audio_file = AudioSegment.from_wav(audio_name)
    return audio_file[start:end] if end else audio_file[start:]

def fa_return_timestamps(waveform, trellis, word_segments, i: int) -> tuple[float, float]:
    sample_rate = 44100
    ratio = waveform.size(1) / (trellis.size(0) - 1)
    word = word_segments[i]
    x0 = int(ratio * word.start)
    x1 = int(ratio * word.end)

    return float(f"{x0 / sample_rate:.3f}") * 1000, float(f"{x1 / sample_rate:.3f}") * 1000

def localize_match(sentences, utterance) -> int:
    """
    Finds the location of utterance by searching through the document

    Returns whether the utterance is in the first half of the audio by taking
    the average of the amount of sentences in the doc and splitting it.
    :param sentences:  list of sentences split by punctuation
    :param utternace: the sentence we want to match to
    :return: 1 or 2, indicating which half of the audio file
    """
    transcript_len = len(sentences)
    avg = math.floor(transcript_len / 2)

    index = 0
    for i, sent in enumerate(sentences):
        if utterance in sent:
            index = i
            break

    return 2 if index > avg else 1

def localize_context(sentences: [str], context_target: [str]) -> int:
    transcript_len = len(sentences)
    avg = math.floor(transcript_len / 2)

    index = 0
    for i, sent in enumerate(sentences):
        if context_target[0] in sent:
            index = i
            break

    return 2 if index > avg else 1

