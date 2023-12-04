from operator import itemgetter
from utils.text_preprocessing_functions import split_sentence_with_numbers

def minimum_word_length(segments: list[dict], target: list[str], first_word:str, index: int) -> tuple[float, float, float]:
    """
    The whisper transcript structure can be a little tricky. Be careful of how you
    index into the segment and into each segment (In the test files there is an
    example transcript)

    Assumptions:
        > Whisper will have accurate transcription, but the punctuation marks
        are inaccurate
        > Periods will either be commas or periods
        > The utterance itself is a sentence, so we just need to match a sentence
        to a sentence

    Both sentences should be processed, and punctuation marks should be removed

    Loops through both sentences simultaneously
    """
    debugging = False
    seg = split_sentence_with_numbers(segments[index]["text"])
    word_i = seg.index(first_word)

    i = 0
    score = 0
    total_score = len(target)
    terminate_loop = False

    start = segments[index]["words"][word_i]["start"]

    while i != len(target) and not terminate_loop:
        try:
            if debugging: print(f"{i, target[i]} | {word_i, seg[word_i]} : {target[i] == seg[word_i]}")
            if target[i] == seg[word_i]:
                score += 1 / total_score

            i += 1
            word_i += 1

        except IndexError:
            if index + 1 == len(segments): # If window reaches the end of the transcript: break
                terminate_loop = True
                break

            index += 1
            seg = split_sentence_with_numbers(segments[index]["text"]) #moves window to the next segment
            word_i = 0 # reset word index

            if target[i] == seg[word_i]: # Check the words again since window moved
                score += 1 / total_score

    end = segments[index]["words"][word_i - 1]["end"]

    return start, end, score


def whisper_time_stamps(utterance: str, whisper_transcript: dict) -> tuple[float, float, float]:
    """
    Finds the sentence segment in the whisper transcript which contains the
    first word, and then matches the rest of the utterance sentence to the
    sentence.

    the transcript and utterance should already have their punctuation removed.
    """

    print("> Getting time stamps from whisper")
    scores = []

    first_word = split_sentence_with_numbers(utterance.lower())[0]
    for index, segment in enumerate(whisper_transcript["segments"]):

        if first_word in split_sentence_with_numbers(segment["text"]): #Apparently "and" in a string counts as True?
            target = split_sentence_with_numbers(utterance)
            score = minimum_word_length(whisper_transcript["segments"], target, first_word, index)

            if score[-1] >= 1:
                return score[0] * 1000, score[1] * 1000, score[-1]

            scores.append(score)

    try:
        result = max(scores, key=itemgetter(2))
    except ValueError:
        print("ERROR: No Alignments to be found! Trying again")
        new_utterance = " ".join(utterance.split()[1:])
        start, end, score = whisper_time_stamps(new_utterance, whisper_transcript)
        return start - 400, end + 300, score

    return result[0] * 1000, result[1] * 1000, result[-1]

if __name__ == "__main__":

    def calculate_similarity_score(sentence1, sentence2):
        words1 = sentence1.split()
        words2 = sentence2.split()

        distance_matrix = [[0] * (len(words2) + 1) for _ in range(len(words1) + 1)]

        for i in range(len(words1) + 1):
            for j in range(len(words2) + 1):
                if i == 0:
                    distance_matrix[i][j] = j
                elif j == 0:
                    distance_matrix[i][j] = i
                elif words1[i - 1] == words2[j - 1]:
                    distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
                else:
                    distance_matrix[i][j] = 1 + min(
                        distance_matrix[i - 1][j],  # Deletion
                        distance_matrix[i][j - 1],  # Insertion
                        distance_matrix[i - 1][j - 1]  # Substitution
                    )

        levenshtein_distance = distance_matrix[len(words1)][len(words2)]
        similarity_score = 1 - (levenshtein_distance / len(words2))

        return similarity_score


    # Example usage:
    target_sentence = "congress approved nearly 50 billion to help renters pay back rent"
    potential_sentence = "congress approved nearly billion to help renters pay back rent"

    score = calculate_similarity_score(potential_sentence, target_sentence)
    print(f"The similarity score is: {score}")


