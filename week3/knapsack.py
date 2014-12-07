#!/usr/bin/env python
'''
Programming Assignment - 3
Implement the Knapsack Algorithm.

Input contains items in a knapsack with an associated value and weight
[value_1] [weight_1]
'''

import os
import copy
FILE_NAME = os.path.expanduser('~/coursera/algorithms2/week3/knapsack1.txt')


def read_input(_file):
    '''
    Read the file that contains contains the knapsack info
    and	return a list of tuples
    '''

    data = []
    capacity = 0  # capacity of the knapsack
    total_items = 0  # total items

    with open(_file, 'r') as f:
        lines = f.readlines()
        capacity, total_items = map(int, lines[0].split())

        data.append((0, 0))  # insert dummy value
                             # so that item number will
                             # be an index for its value and weight

        for line in lines[1:]:
            val, wt = map(int, line.split())
            data.append((val, wt))

    return data, capacity, total_items


def gen_val_matrix(data, total_wt, total_items):
    '''
    Given the values and weights of all items,
    total capacity of the knapsack and total number of items,
    calculate the value of the optimal solution
    '''
    item_wt_matrix = []  # (total_items + 1) * (total_wt + 1) matrix

    # base case
    # if num_item is 0, then the val is 0 for all weights
    base = [0] * (total_wt + 1)

    # initialize first row of matrix
    item_wt_matrix.insert(0, base)

    for i in range(1, total_items + 1):
        val_item, wt_item = data[i]

        row = []
        for j in range(total_wt + 1):

            if wt_item > j:
                row.insert(j, item_wt_matrix[i - 1][j])

            else:
                # including item
                val1 = val_item + item_wt_matrix[i - 1][j - wt_item]

                # not including item
                val2 = item_wt_matrix[i - 1][j]

                row.insert(j, max(val1, val2))

        item_wt_matrix.insert(i, row)

    return item_wt_matrix


def get_optimal_sol(matrix, data):
    '''
    Given the optimal solutiion matrix, find the actual
    items that resulted in the opimal value
    Rows indicate the items and columns indicate weights
    '''

    rows = len(matrix) - 1     # since zero indexing
    cols = len(matrix[0]) - 1  # since zero indexing

    result = []
    while(rows > 0 and cols > 0):
        optimal_val = matrix[rows][cols]

        item_val, item_wt = data[rows]

        # there are 2 possible ways to generate the value current cell
        val1 = item_val + matrix[rows - 1][cols - item_wt]
        val2 = matrix[rows - 1][cols]

        if optimal_val == val1:
            result.append(rows)
            cols -= item_wt

        rows -= 1

    result.reverse()  # since we read results from right to left
    return result


def main():
    iteminfo, cap, num_items = read_input(FILE_NAME)

    res = gen_val_matrix(iteminfo, cap, num_items)
    print 'Optimal value of solution is {}'.format(res[-1][-1])

    res_items = get_optimal_sol(res, iteminfo)
    print 'Items resulting in optimal solution are {}'.format(res_items)


if __name__ == '__main__':
    main()
