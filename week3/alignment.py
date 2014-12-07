#!/usr/bin/env python
'''
Computing global alignment of sequences

Input: Strings X and Y over an alphabet and a penalty pattern
Output: An alignment of X and Y among all possible alignments
of X and Y such that penalty is minimum ie. X and Y are as similar as possible
'''

import sys
PENALTY_GAP = 0
PENALTY_MISMATCH = -1
PENALTY_MATCH = -2


def compute_alignment_matrix(seq_x, seq_y):
    '''
    Take as input two sequences seq_x and seq_y whose
    elements share a common alphabet.

    Returns the global alignment matrix for seq_x and seq_y
    '''

    alignment_matrix = []

    # base case
    # if one string is empty and other contains 'i'
    # characters, then we pay a gap penalty = i * PENALTY_GAP

    base = [i * PENALTY_GAP for i in range(len(seq_y) + 1)]

    # initialize first row of matrix
    alignment_matrix.insert(0, base)

    # the first column of every row will have a value =
    # i * PENALTY_GAP

    for row in range(1, len(seq_x) + 1):
        alignment_matrix.insert(row, [row * PENALTY_GAP])

    for i  in range(1, len(seq_x) + 1):
        for j in range(1, len(seq_y) + 1):

            # consider rightmost characters of seq_x and seq_y

            # Case1 - either they match or mismatch
            x = seq_x[i - 1]        # zero-based indexing
            y = seq_y[j - 1]        # zero-based indexing

            score = PENALTY_MATCH if x == y else PENALTY_MISMATCH
            val1 = score + alignment_matrix[i - 1][j - 1]

            # Case2 - x matches with a gap
            val2 = PENALTY_GAP + alignment_matrix[i - 1][j]

            # Case3 - y matches with a gap
            val3 = PENALTY_GAP + alignment_matrix[i][j - 1]

            alignment_matrix[i].insert(j, min(val1, val2, val3))

    return alignment_matrix


def compute_global_alignment(matrix, seq_x, seq_y):
    '''
    Given the alignment matrix and the two sequences,
    return the optimal global alignment
    '''

    rows = len(matrix) - 1  # zero-based indexing
    cols = len(matrix[0]) - 1  # zero-based indexing

    align_x = ''
    align_y = ''

    while (rows > 0 and cols > 0):
        optimal_score = matrix[rows][cols]

        # consider rightmost characters of seq_x and seq_y
        x = seq_x[rows - 1]        # zero-based indexing
        y = seq_y[cols - 1]        # zero-based indexing

        # Case1 - either they match or mismatch
        score = PENALTY_MATCH if x == y else PENALTY_MISMATCH
        val1 = score + matrix[rows - 1][cols - 1]

        # Case2 - x matches with a gap
        val2 = PENALTY_GAP + matrix[rows - 1][cols]

        # Case3 - y matches with a gap
        val3 = PENALTY_GAP + matrix[rows][cols - 1]

        if optimal_score == val1:
            align_x += x
            align_y += y
            rows -= 1
            cols -= 1

        elif optimal_score == val2:
            align_x += x
            align_y += '-'
            rows -= 1

        else:
            align_x += '-'
            align_y += y
            cols -= 1

    # since we read results from right to left
    # reverse the alignments
    return (align_x[::-1], align_y[::-1])


def main():
    x = sys.argv[1]
    y = sys.argv[2]

    alignment_mat = compute_alignment_matrix(x, y)

    global_alignment = compute_global_alignment(alignment_mat, x, y)
    msg = 'Global Alignment of {} and {}'.format(x, y)
    msg += ' is {} with a score of {}'.format(global_alignment,
                                              alignment_mat[-1][-1])
    print msg


if __name__ == '__main__':
    main()
