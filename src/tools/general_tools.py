# author : Philippe Vo
# date   : Sat 09 Jul 2022 06:42:12 PM

# 3rd party imports
from difflib import SequenceMatcher

def string_similar(strA, strB):
    return SequenceMatcher(None, strA.lower(), strB.lower()).ratio()

def get_most_likely_str(target, options):
    mostLikelyStrIdx = 0
    highestSimiliarScore = 0
    similiarScore = 0
    for idx, option in enumerate(options):
        similiarScore = string_similar(target, option)
        if similiarScore > highestSimiliarScore:
            highestSimiliarScore = similiarScore
            mostLikelyStrIdx = idx

    return mostLikelyStrIdx

def print_center(msg: str, columns):
    print(msg.center(columns))
