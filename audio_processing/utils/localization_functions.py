from pydub import AudioSegment
import math

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

