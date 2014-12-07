#!/usr/bin/env python
'''
Given two strings, the edit distance corresponds to the
minimum number of single character
insertions, deletions, and substitutions
that are needed to transform one string into another.

Formula:

edit_distance = len(x) + len(y) + global_alignment_score(x, y)

In calculating the global_alignment_score we use:
PENALTY_GAP = 0
PENALTY_MISMATCH = -1
PENALTY_MATCH = -2

Question: Given a list of 79339 words, write a function
check_spelling(checked_word, dist, word_list)
that iterates through 'word_list' and returns the set
of all words that are within edit distance 'dist'
of the string 'checked_word'.
'''

import os
from alignment import compute_alignment_matrix
path = '~/coursera/algorithms2/week3/assets_scrabble_words3.txt'
FILE_NAME = os.path.expanduser(path)


def read_input(_file):
    '''
    Read the list of words from the file
    and return a list of words
    '''
    words = []
    with open(_file, 'r') as f:
        words = map(lambda x: x.strip(), f.readlines())
    return words


def check_spelling(checked_word, dist, word_list):
    result = set()

    for word in word_list:
        score = compute_alignment_matrix(word, checked_word)[-1][-1]
        edit_distance = len(word) + len(checked_word) + score
        if 0 <= edit_distance <= dist:
            result.add(word)

    return result


def main():
    words = read_input(FILE_NAME)

    res = check_spelling('humble', 1, words)
    msg = 'Words at edit distance 1 from "humble"'
    msg += ' are {}'.format(res)
    print msg

    res = check_spelling('firefly', 2, words)
    msg = 'Words at edit distance 2 from "firefly"'
    msg += ' are {}'.format(res)
    print msg


if __name__ == '__main__':
    main()
