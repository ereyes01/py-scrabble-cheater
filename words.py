#!/usr/bin/env python

import sys
from collections import Counter


scores = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4,
          'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3,
          'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8,
          'y': 4, 'z': 10}


def word_score(word):
    return sum(scores[char] for char in word)


def _word_find_comparator(word, letter_count):
    word_count = Counter(word)

    for letter in word_count:
        if letter not in letter_count or \
           word_count[letter] > letter_count[letter]:
            return False

    return True


class ScrabbleCheater:
    def __init__(self, path=None, words=None):
        if words is None:
            self.words = []
        else:
            self.words = words

        if path is not None:
            with open(path) as f:
                for line in f.read().split("\n"):
                    if len(line) > 0:
                        self.words.append(unicode(line).lower())

    def __repr__(self):
        return repr(self.words)

    def __search(self, search, comparator):
        found = set()

        for word in self.words:
            if comparator(word, search):
                found.add(word)

        return sorted(found, key=word_score, reverse=True)

    def find(self, letters):
        found_words = self.__search(Counter(letters), _word_find_comparator)

        return ScrabbleCheater(words=found_words)

    def ends_with(self, suffix):
        comparator = lambda word, ending: word.endswith(ending)
        found_words = self.__search(suffix, comparator)

        return ScrabbleCheater(words=found_words)

    def starts_with(self, prefix):
        comparator = lambda word, prefix: word.startswith(prefix)
        found_words = self.__search(prefix, comparator)

        return ScrabbleCheater(words=found_words)

    def contains(self, substring):
        comparator = lambda word, substring: substring in word
        found_words = self.__search(substring, comparator)

        return ScrabbleCheater(words=found_words)
