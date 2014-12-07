#!/usr/bin/env python
'''
Computing global alignment of sequences

Input: Strings X and Y over an alphabet and a penalty pattern
Output: An alignment of X and Y among all possible alignments
of X and Y such that penalty is minimum ie. X and Y are as similar as possible

Runtime = O(mn) where m = len(X) n = len(Y)
'''

import sys
PENALTY_GAP = 1
PENALTY_MISMATCH = 1
PENALTY_MATCH = -2


def compute_alignment_matrix(seq_x, seq_y, global_flag=True):
    '''
    Take as input two sequences seq_x and seq_y whose
    elements share a common alphabet.

    If global_flag is True, compute Global Alignment Matrix
    If global_flag is False, compute Local Alignment Matrix

    To compute a local alignment matrix, whenever a positive value is being
    assigned to alignment_matrix[i][j], replace with 0
    '''

    alignment_matrix = []

    # base case
    # if one string is empty and other contains 'i'
    # characters, then we pay a gap penalty = i * PENALTY_GAP

    if global_flag:
        base = [i * PENALTY_GAP for i in range(len(seq_y) + 1)]
    else:
        base = [0] * (len(seq_y) + 1)

    # initialize first row of matrix
    alignment_matrix.insert(0, base)

    # the first column of every row will have a value =
    # i * PENALTY_GAP

    for row in range(1, len(seq_x) + 1):
        if global_flag:
            val = row * PENALTY_GAP
        else:
            val = 0
        alignment_matrix.insert(row, [val])

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

            val = min(val1, val2, val3)
            if not global_flag and val > 0:
                val = 0
            alignment_matrix[i].insert(j, val)

    return alignment_matrix


def compute_local_alignment(matrix, seq_x, seq_y):
    '''
    Given the alignment matrix and the two sequences,
    return the optimal local alignment

    **Principle**
    Start the traceback from the entry in the local alignment matrix that has
    the smallest value over the entire matrix and trace backwards
    similar to compute global alignment.
    Stop the traceback when the first entry with value 0 is encountered.
    If the local alignment matrix has more than one entry that has the smallest
    value, any one of those may be used as the starting entry
    '''

    row, col = _get_index_smallest_value(matrix)

    align_x = ''
    align_y = ''
    while(row > 0 and col > 0):
        optimal_score = matrix[row][col]

        if optimal_score == 0:
            break

        # consider rightmost characters of seq_x and seq_y
        x = seq_x[row - 1]        # zero-based indexing
        y = seq_y[col - 1]        # zero-based indexing

        # Case1 - either they match or mismatch
        score = PENALTY_MATCH if x == y else PENALTY_MISMATCH
        val1 = score + matrix[row - 1][col - 1]

        # Case2 - x matches with a gap
        val2 = PENALTY_GAP + matrix[row - 1][col]

        # Case3 - y matches with a gap
        val3 = PENALTY_GAP + matrix[row][col - 1]

        if optimal_score == val1:
            align_x += x
            align_y += y
            row -= 1
            col -= 1

        elif optimal_score == val2:
            align_x += x
            align_y += '-'
            row -= 1

        else:
            align_x += '-'
            align_y += y
            col -= 1

    # since we read results from right to left
    # reverse the alignments
    return (align_x[::-1], align_y[::-1])


def _get_index_smallest_value(matrix):
    '''
    Return index of smallest value
    '''
    min_val = float('inf')
    index = None
    for i in range(len(matrix)):
        val = min(matrix[i])
        if val < min_val:
            min_val = val
            row = i
            col = matrix[i].index(val)
            index = (row, col)

    return index


def compute_global_alignment(matrix, seq_x, seq_y):
    '''
    Given the alignment matrix and the two sequences,
    return the optimal global alignment
    '''

    row = len(matrix) - 1  # zero-based indexing
    col = len(matrix[0]) - 1  # zero-based indexing

    align_x = ''
    align_y = ''

    while (row > 0 and col > 0):
        optimal_score = matrix[row][col]

        # consider rightmost characters of seq_x and seq_y
        x = seq_x[row - 1]        # zero-based indexing
        y = seq_y[col - 1]        # zero-based indexing

        # Case1 - either they match or mismatch
        score = PENALTY_MATCH if x == y else PENALTY_MISMATCH
        val1 = score + matrix[row - 1][col - 1]

        # Case2 - x matches with a gap
        val2 = PENALTY_GAP + matrix[row - 1][col]

        # Case3 - y matches with a gap
        val3 = PENALTY_GAP + matrix[row][col - 1]

        if optimal_score == val1:
            align_x += x
            align_y += y
            row -= 1
            col -= 1

        elif optimal_score == val2:
            align_x += x
            align_y += '-'
            row -= 1

        else:
            align_x += '-'
            align_y += y
            col -= 1

    # since we read results from right to left
    # reverse the alignments
    return (align_x[::-1], align_y[::-1])


def main():
    x = sys.argv[1]
    y = sys.argv[2]

    # Global Alignment
    alignment_mat = compute_alignment_matrix(x, y)

    global_alignment = compute_global_alignment(alignment_mat, x, y)
    msg = 'Global Alignment of {} and {}'.format(x, y)
    msg += ' is {} with a score of {}'.format(global_alignment,
                                              alignment_mat[-1][-1])
    print msg

    # Local Alignment
    alignment_mat = compute_alignment_matrix(x, y, global_flag=False)
    local_alignment = compute_local_alignment(alignment_mat, x, y)
    msg = 'Local Alignment of {} and {}'.format(x, y)
    msg += ' is {} with a score of {}'.format(local_alignment,
                                              alignment_mat[-1][-1])

    print msg


if __name__ == '__main__':
    main()
