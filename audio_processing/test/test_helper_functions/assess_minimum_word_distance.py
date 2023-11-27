import json
import string
from datetime import datetime
from audio_processing.utils.minimum_word_distance import whisper_time_stamps
from utils.text_preprocessing_functions import sanitize_whisper_transcript, split_sentence_with_numbers

"""
Issues: 
Its a little too slow. Potentially change the sanitized function to be text replacement instead of loops

Whisper-ts pairs together words and numbers for whatever reason.  Ex ( nearly 50) for a single word

"""


start_time = datetime.now()

with open("npr_evictions_whisper_transcript.json", "r") as read_file:
    data = json.load(read_file)

transcript = sanitize_whisper_transcript(data)

def t_split():
    sentence = "last month the treasury department estimated that somewhere between 25 and 30 billion"
    correct = ['last', 'month', 'the', 'treasury', 'department', 'estimated', 'that', 'somewhere', 'between 25', 'and 30', 'billion']
    s = split_sentence_with_numbers(sentence)
    assert correct == s, "split failed"

def t_sanitization(transcript:dict = transcript):
    "Checks for any punctuation"
    punct = set(string.punctuation)

    segments = transcript["segments"]
    for index in range(len(segments)):

        txt = set(segments[index]["text"].split())
        if any(char in punct for char in txt):
            assert False, f"There is punctuation in the text : {txt}"

        for i in range(len(segments[index]["words"])):
            if any(char in punct for char in segments[index]["words"][i]):
                assert False, f"There is punctuation in the text : {segments[index]['words'][i]}"

def t_minimum_edit_distance():
    utterance = "billion has made it to renters and landlords but the money is finally getting out there what have the obstacles been" # 104020.0, 110540.0
    # utterance = "congress approved nearly 50 billion to help renters pay back rent"
    # utterance = "congress approved nearly billion to help renters pay back rent" # 3900.0 #7680.0
    print(whisper_time_stamps(utterance, transcript))



if __name__ == "__main__":
    t_sanitization()
    t_minimum_edit_distance()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
