from fastDamerauLevenshtein import damerauLevenshtein
from operator import itemgetter

context = "Michael Jackson is who you're talking about. Thank you, yeah - because he's shy. And everybody didn't want to approach him anyway because he's so shy. But he and I would sit and have lunch together."
match = "everybody didn't want to approach him anyway"

with open("life_happens.txt") as f:
    transcript = f.read().split(".")

scores = []
# Search for the maximum score
for index, sentence in enumerate(transcript):
    score = damerauLevenshtein(match, sentence, similarity=True)
    print(score, sentence) # expected result: 2.0
    scores.append([match, sentence, index, score])

rankings = sorted(scores, key=itemgetter(3), reverse=True)
highest = rankings[0]

print(highest)

#Checking for validity and tiebreaking
match_i = highest[2]
context_start = match_i - 4 if match_i != 0 else 0
context_end = match_i + 1 if match_i != len(transcript) else len(transcript)

print(transcript[context_start:context_end + 1])

print(damerauLevenshtein(context, transcript[context_start:context_end + 1], similarity=True))
