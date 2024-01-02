from fastDamerauLevenshtein import damerauLevenshtein as edit_dist
from operator import itemgetter

context = "Michael Jackson is who you're talking about. Thank you, yeah - because he's shy. And everybody didn't want to approach him anyway because he's so shy. But he and I would sit and have lunch together."
match = "everybody didn't want to approach him anyway"

with open("life_happens.txt") as f:
    transcript = f.read().split(".")

def edit_distance(match, context, transcript_list):
    scores = []
    rankings = ()
    context_ranks = []

    for index, sentence in enumerate(transcript):
        score = edit_dist(match, sentence, similarity=True)
        print(score, sentence)  # expected result: 2.0
        scores.append([match, sentence, index, score])

    rankings = sorted(scores, key=itemgetter(3), reverse=True)[:3] # Top 3

    for candidate in rankings:
        match_i = candidate[2]
        context_start = match_i - 3 if match_i != 0 else 0
        context_end = match_i + 1 if match_i != len(transcript) else len(transcript)
        result = edit_dist(context, "".join(transcript[context_start:context_end + 1]), similarity=True)
        context_ranks.append((context_start, context_end, result))

    print(context_ranks)


edit_distance(match, context, transcript)