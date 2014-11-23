#!/usr/bin/env python
'''
Programming Assignment - 1
Implement Prim's minimum spanning tree algorithm on an
undirected weighted graph containing 500 nodes and 2184 edges
'''
import os
from heapq import heappush, heappop, heapify
GRAPH_FILE = os.path.expanduser('~/coursera/algorithms2/week1/edges.txt')


def create_graph(graph_file):
    '''
    Given the graph file, create an undirected graph
    using the adjacency list representation.
    The graph is keyed on the node with value being a list of tuples.
    First element is the node to which the key node is connected,
    while the second element is the weight of the edge.
    eg. {1:[(2, 10)]} -> node 1 connected to node 2 with an edge of weight 10
    '''
    ugraph = {}
    with open(graph_file, 'r') as f:
        lines = f.readlines()
        # since first line contains number of nodes and edges
        for line in lines[1:]:
            node1, node2, cost = map(int, line.split())
            if node1 in ugraph:
                ugraph[node1].append((node2, cost))
            else:
                ugraph[node1] = [(node2, cost)]

            # since graph is undirected
            if node2 in ugraph:
                ugraph[node2].append((node1, cost))
            else:
                ugraph[node2] = [(node1, cost)]

    return ugraph


def run_prims(graph):
    '''
    Given an undirected graph,
    run Prim's minimum spanning tree algorithm on this graph,
    to compute the minimum spanning tree and its correponding cost
    Running time O(nm) where n = number of nodes, m = number of edges
    '''

    visited = set()
    # initially all nodes are unvisited
    unvisited = set(graph.keys())

    # select an arbitrary node to start
    visited.add(unvisited.pop())

    # minimum spanning tree
    mst = []

    while unvisited:
        #(node1, node2, cost)
        min_cost = (None, None, float('inf'))
        for _node in visited:
            for neigh, wt in graph[_node]:
                if neigh not in visited and wt <= min_cost[2]:
                    min_cost = (_node, neigh, wt)

        unvisited.remove(min_cost[1])
        visited.add(min_cost[1])
        mst.append(min_cost)

    cost = _return_cost_of_mst(mst)
    return (mst, cost)


def run_prims_heap(graph):
    '''
    Given an undirected graph,
    run Prim's minimum spanning tree algorithm on this graph,
    to compute the minimum spanning tree and its correponding cost
    Since using heap-based implementation, Run time O(mlogn)
    where n = number of nodes, m = number of edges
    '''

    visited = set()
    # initially all nodes are unvisited
    unvisited = set(graph.keys())

    # select an arbitrary node to start
    node = unvisited.pop()
    visited.add(node)

    # initialize the heap,
    h = _initialize_heap(node, unvisited, graph)

    # minimum spanning tree
    mst = [(node, 0)]

    while unvisited:
        wt, node = heappop(h)
        h = _manage_heap(h, node, graph, unvisited)

        unvisited.remove(node)
        visited.add(node)
        mst.append((node, wt))

    cost = [i[1] for i in mst]
    return (mst, sum(cost))


def _manage_heap(heap, node, graph, unvisited):
    '''
    When a node is popped from the heap(ie. moved
    from the unvisited set to visited),
    we need to recompute the cheapest edge of all its neighbours
    '''
    for neigh, wt in graph[node]:
        if neigh in unvisited:
            index = _compute_heap_index(heap, neigh)
            cost, _node = heap.pop(index)
            heapify(heap)
            new_cost = min(cost, wt)
            heappush(heap, (new_cost, _node))

    return heap


def _initialize_heap(source, nodes, graph):
    '''
    to initialize the heap,
    find the cost of the edge from every node
    among the unvisited nodes to the visited node.
    Every item of the heap is a tuple of form (cost, node)
    '''
    edges = graph[source]
    h = []
    for node, wt in edges:
        heappush(h, (wt, node))

    neighs = set([item[0] for item in edges])

    # now insert all non-neighbours of source in the heap
    for node in nodes:
        if node not in neighs:
            heappush(h, (float('inf'), node))

    return h


def _compute_heap_index(heap, node):
    '''
    return the index of node in the heap
    '''
    for i in range(len(heap)):
        if heap[i][1] == node:
            return i


def _return_cost_of_mst(tree):
    '''
    Given the minimum spanning tree,
    return its cost
    '''
    cost = 0
    for node1, node2, edge_wt in tree:
        cost += edge_wt

    return cost


def main():
    mygraph = create_graph(GRAPH_FILE)
    min_tree, cost = run_prims(mygraph)
    print 'Cost of minimum spanning tree {}'.format(cost)
    min_tree, cost = run_prims_heap(mygraph)
    print 'Cost of minimum spanning tree using heap {}'.format(cost)


if __name__ == '__main__':
    main()
