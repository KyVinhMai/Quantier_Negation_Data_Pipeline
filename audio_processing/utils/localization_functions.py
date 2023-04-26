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

def localize_context(sentences: list[str], context_target: str) -> tuple[float, float]:
    """
    Finds the location of utterance by searching through the document.

    :param sentences: list of sentences split by punctuation
    :param context_target: the sentence we want to match to
    :return: a range between 0-1, indicating which normalized location
                of the audio the utterance lies
    """
    transcript_len = len(sentences)
    sent_iter = iter(sentences)

    initial_index = None
    end_index = None
    index = 0

    while initial_index is None:
        sent = next(sent_iter)
        index += 1
        if context_target[0] in sent:
            initial_index = index
            break

    while end_index is None:
        sent = next(sent_iter)
        index += 1
        if context_target[-1] in sent:
            end_index = index
            break

    return transcript_len / initial_index, transcript_len / end_index

