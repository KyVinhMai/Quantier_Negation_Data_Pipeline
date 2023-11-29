import json
import string
import timeit
from audio_processing.audio_utils.minimum_word_distance import whisper_time_stamps
from utils.text_preprocessing_functions import sanitize_whisper_transcript, split_sentence_with_numbers

"""
Issues: 
Its a little too slow. Potentially change the sanitized function to be text replacement instead of loops

Whisper-ts pairs together words and numbers for whatever reason.  Ex ( nearly 50) for a single word

"""


start = timeit.default_timer()
def t_split():
    sentence = "last month the treasury department estimated that somewhere between 25 and 30 billion"
    correct = ['last', 'month', 'the', 'treasury', 'department', 'estimated', 'that', 'somewhere', 'between 25', 'and 30', 'billion']
    s = split_sentence_with_numbers(sentence)
    assert correct == s, "split failed"

def t_sanitization(transcript:dict):
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

def t_npr_evictions():
    import ast
    with open("test_npr_evictions_time_stamps.txt") as f:
        tests = f.readlines()

    for line in tests:
        line = ast.literal_eval(line)
        start, end, _ = whisper_time_stamps(line[0], evictions_transcript)
        output = (start, end)
        assert (line[1], line[2]) == output, f"{(line[1], line[2])} != {output}"

    # utterance = "billion has made it to renters and landlords but the money is finally getting out there what have the obstacles been" # 104020.0, 110540.0
    # utterance = "congress approved nearly 50 billion to help renters pay back rent"
    # utterance = "congress approved nearly billion to help renters pay back rent" # 3900.0 #7680.0
    # utterance = "and in nearby san diego city the average rent is over 2000 vanessa and her mom also face other barriers like credit scores a lot of these places say they want your credit rate has to be like 600"
    # print(whisper_time_stamps(utterance, transcript))

def t_trayvon():
    utterance = "We begin with Hassan Adib. He teaches world history, African history, and African-American history at Westlake High School in Waldorf, Maryland, and joins us by phone from the school. Nice to have you with us today."
    print(whisper_time_stamps(utterance, trayvon_transcript))

if __name__ == "__main__":
    with open("npr_evictions_whisper_transcript.json", "r") as read_file:
        data = json.load(read_file)

    evictions_transcript = sanitize_whisper_transcript(data)

    with open("npr_trayvon_martin_transcript.json", "r") as read_file:
        data = json.load(read_file)

    trayvon_transcript = sanitize_whisper_transcript(data)

    # t_sanitization(evictions_transcript)
    # t_npr_evictions()

    t_sanitization(trayvon_transcript)
    t_trayvon()

    # All the program statements
    stop = timeit.default_timer()
    execution_time = stop - start

    print("Program Executed in " + str(execution_time))  # It returns time in seconds
