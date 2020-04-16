__author__ = 'roloprogramating'
import nltk
from collections import defaultdict


def bag_of_word_count_diff(bag1, bag2):
    dist = 0
    bag1_freq = defaultdict(int)
    for word in bag1.split():
        bag1_freq[word] += 1
    bag2_freq = defaultdict(int)
    for word in bag2.split():
        bag2_freq[word] += 1
    all_words = list(set(bag1.split() + bag2.split()))
    for word in all_words:
        dist += abs(bag1_freq.get(word, 0) - bag2_freq.get(word, 0))
    return dist