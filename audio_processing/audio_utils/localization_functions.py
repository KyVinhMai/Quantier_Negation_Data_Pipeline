from pydub import AudioSegment
from fastDamerauLevenshtein import damerauLevenshtein as edit_dist
from operator import itemgetter
import logging

"Logging Configuration"
logging.basicConfig(
    level=logging.INFO,
    filename= "localize_context.log",
    filemode= "w"
)

def extract_sentence(start:float, end:float, audio_dir: str) -> AudioSegment:
    "Segments the audio given the timestamps"
    audio_file = AudioSegment.from_wav(audio_dir)
    return audio_file[start:end] if end else audio_file[start:]

def fa_return_timestamps(waveform, trellis, word_segments) -> tuple[float, float]:
    sample_rate = 44100
    ratio = waveform.size(1) / (trellis.size(0) - 1)
    word = word_segments[0]
    x0 = int(ratio * word.start)
    x1 = int(ratio * word.end)

    return float(f"{x0 / sample_rate:.3f}") * 1000, float(f"{x1 / sample_rate:.3f}") * 1000

def edit_distance(match: str, context: str, transcript_list: list[str], context_length: int) -> [int, int, float]:
    """
    Uses the Damerau Levenshtein Edit distance.
    1) Scores each sentence and their distance from the match sentence.
    2) Grabs the first 3 highest ranking match sentences  and then finds which of the 3
    has the surronding context that is the same as the match context sentence.

    :param match: The target sentence itself (Is a string)
    :param context: Context sentence (Is a string)
    :param transcript_list: List of the transcript sentences split by punctuation
    :return: Context start and end indexes in the transcript list. The third float value is the score
    """
    scores = []
    rankings = ()
    context_ranks = []

    for index, sentence in enumerate(transcript_list):
        score = edit_dist(match, sentence, similarity=True)
        scores.append([match, sentence, index, score])

    rankings = sorted(scores, key=itemgetter(3), reverse=True)[:3] # Top 3

    for candidate in rankings:
        match_i = candidate[2]
        context_start = match_i - context_length if match_i > 0 else 0
        context_end = match_i + 1 if match_i != len(transcript_list) else len(transcript_list)
        result = edit_dist(context, "".join(transcript_list[context_start:context_end + 1]), similarity=True)
        context_ranks.append((context_start, context_end, result))

    return max(context_ranks, key=itemgetter(2))

def localize_context(sentences: list[str], context_target: list[str], match_sentence: str, context_length: int) -> tuple[float, float]:
    """
    Searches for the start and end indexes for the context.

    :param sentences: list of sentences split by punctuation
    :param context_target: the sentence we want to match to
    :return: Floats in the range of between 0-1, indicating which normalized location
                of the audio the utterance lies
    """
    transcript_len = len(sentences)
    initial_index = None
    end_index = None

    try:
        initial_index = sentences.index(context_target[0])
        end_index = sentences.index(context_target[-1])
    except ValueError:

        print("@ Could not index in! Using Damerau Levenshtein")
        initial_index, end_index, _ = edit_distance(match_sentence, "".join(context_target), sentences, context_length)

    return round(initial_index/transcript_len, 3), round(end_index/transcript_len, 3)

