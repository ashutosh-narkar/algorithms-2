#!/usr/bin/env python
'''
Programming Assignment - 1
Implement a greedy algorithm that schedules jobs
in decreasing order of
1) difference between weight of a job - length of a job
2) ratio of weight/length
'''
import os
FILE_PATH = os.path.expanduser('~/coursera/algorithms2/week1/jobs.txt')


def read_data(path):
    '''
    Read the file data containing the weight and length of jobs
    and return a list of tuples of form (weight, length)
    '''
    weight_length = []
    with open(path) as f:
        lines = f.readlines()
        # since first line contains number of jobs
        for line in lines[1:]:
            weight, length = line.split()
            weight_length.append((int(weight), int(length)))
    return weight_length


def order_job(job_data, difference=True):
    '''
    Given the job data ie(weight, length) arrange the jobs
    in decreasing order of difference(if difference=True) or ratio.
    If two jobs have equal difference(or ratio) of weight and length,
    schedule the job with higher weight first
    '''
    # dict keyed on difference(or ratio) between weight and length
    # value is list of jobs
    metric_job = {}
    for weight, length in job_data:
        metric = weight - length if difference else weight / float(length)
        if metric not in metric_job:
            metric_job[metric] = [(weight, length)]
        else:
            # if multiple jobs have same difference(or ratio),
            # higher weight jobs scheduled first
            current = metric_job[metric]
            current.append((weight, length))
            metric_job[metric] = sorted(current, key=lambda x: x[0],
                                   reverse=True)

    # arrange jobs in decreasing order of difference(or ratio)
    ordered_data = sorted(metric_job.items(), key=lambda x: x[0], reverse=True)
    time = _compute_weighted_completion_time(ordered_data)
    return time


def _compute_weighted_completion_time(data):
    '''
    Given job data in decreasing order of difference/ ratio,
    calculate weighted completion time using formula:
    Wi * Ci, where Wi = weight of job i
    and Ci = sum of job lengths upto and including i
    '''
    current_time = 0
    weighted_time = 0
    for diff, jobs in data:
        for job in jobs:
            current_time += job[1]          # (weight, length)
            weighted_time += job[0] * current_time
    return weighted_time


def main():
    '''
    Return the sum of weighted completion time for the jobs
    '''
    data = read_data(FILE_PATH)
    competion_time_difference = order_job(data)
    print 'Weighted completion time based on difference {}'.\
                              format(competion_time_difference)

    competion_time_ratio = order_job(data, difference=False)
    print 'Weighted completion time based on ratio {}'.\
                              format(competion_time_ratio)


if __name__ == '__main__':
    main()
