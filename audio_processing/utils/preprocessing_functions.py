from pydub import AudioSegment
from mutagen.mp3 import MP3
import math
import re

def segment_audio(audio_len: int) -> int:
    """
    Returns the middle of the audio duration
    """
    new_length = math.floor(audio_len / 2)

    return new_length * 1000

def split_audio(audio_dir:str, segment: int) -> AudioSegment:
    audio_len = math.floor(MP3(audio_dir).info.length)
    new_length = segment_audio(audio_len)

    audio_file = AudioSegment.from_mp3("npr_evictions.mp3") #todo change

    "if segment is 1, take the first half, else take the 2nd half"
    trimmed_audio =  audio_file[:new_length] if segment == 1 else audio_file[new_length:] #todo check if this correct

    return trimmed_audio

def transform_transcript(utterance:str, quant:str) -> tuple[str, int]:
    """
    The wav2vec model requires transcripts to be uppercase and have
    vertical lines between each word.

    Ex: FINANCIAL|HELP|IS|AVAILABLE

    The function also returns the location of the quantifier
    """
    utterance_list = re.sub(r'[!|?|.|,|[|]|]', '', utterance).split(" ")
    index = utterance_list.index(quant)
    transcript = "|".join([word.upper() for word in utterance_list])

    return transcript, index

def process_text(sentence) -> [str]:
    sentence = sentence.replace(",", "").replace(".", "")
    sentence = sentence.lower()
    return sentence.split()

if __name__ == "__main__":
    audio = MP3("test_file.mp3")
    print(audio.info.length)