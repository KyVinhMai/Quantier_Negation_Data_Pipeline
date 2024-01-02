from pydub import AudioSegment
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

def localize_context(sentences: list[str], context_target: list[str]) -> tuple[float, float]:
    """
    Finds the location of utterance by searching through the document. Attempts
    syntactic matching before using vector embeddings.

    :param sentences: list of sentences split by punctuation
    :param context_target: the sentence we want to match to
    :return: Floats in the range of between 0-1, indicating which normalized location
                of the audio the utterance lies
    """
    transcript_len = len(sentences)
    sent_iter = iter(sentences)

    initial_index = None
    end_index = None

    try:
        initial_index = sentences.index(context_target[0])
        end_index = sentences.index(context_target[-1])
    except ValueError:

        print("@ Could not index in! Finding through looping")
        index = 0

        while initial_index is None:
            sent = next(sent_iter)
            logging.info(f"{index} : {sent}")
            index += 1
            if context_target[0].strip() in sent:
                initial_index = index
                break

        while end_index is None:
            sent = next(sent_iter)
            logging.info(f"{index} : {sent}")
            index += 1
            if context_target[-1].strip() in sent:
                end_index = index
                break
        #Try using Cosine Similarity

    return round(initial_index/transcript_len, 3), round(end_index/transcript_len, 3)

