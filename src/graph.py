import data
import coords_calc as calc
import itertools
from itertools import izip
import math

# ---------- GLOBAL HASH VARIABLE ------------
# arr_nodes[node]:
#   - center
#   - connected_nodes
#   - edges
#   - node

arr_nodes = []


def initialize():
    global arr_nodes
    arr_nodes = [''] * 200

    file_text = open('../assets/text/grafo.txt', 'r').readlines()

    for line in file_text:
        temp = line.split("\t")
        temp_node = int(temp[0])
        temp_connected_nodes = eval(temp[1])
        temp_center = eval(temp[2])
        temp_edges = eval(temp[3])
        arr_nodes[temp_node] = {'node': temp_node,
                                'connected_nodes': temp_connected_nodes,
                                'center': temp_center,
                                'edges': temp_edges}


def is_grapho_initialized():
    return arr_nodes > 1


# Return my current Node
def my_node():
    return node_from_point([data.abs_position_x, data.abs_position_y])


# Return the node that contain the point
def node_from_point((p_x,p_y)):
    for node in arr_nodes:
        if node != '' and is_inside_of_edges([p_x, p_y], node['edges'], node['node']):
            return node['node']

    return False


# Return if a given number of the grapho is connected to the current Node
def is_connected_node(n_grapho):
    return n_grapho in arr_nodes[n_grapho]['connected_nodes']


# Return if a given point is inside of node (inside of his edges)
def is_inside_of_edges(p, edges, node):
    count = 0
    # if node != 57:
    #     return False

    for a, b in pairwise(edges + [edges[0]]):
        if before_on_segment(p, a, b):
            count += 1

    # if node == 57:
    #     print count

    if count % 2 == 1:
        return True
    else:
        return False


# Given three colinear points p, a, b, the function checks if
# point p lies before one line segment 'ab'
# where p[0] is p.x and p[1] is p.y
def before_on_segment(p, a, b):
    if p[0] <= max(a[0], b[0]) and min(a[1], b[1]) < p[1] < max(a[1], b[1]):
        p_x_intersection = (p[1] - min(a[1], b[1])) * abs(b[0] - a[0]) / abs(b[1] - a[1])

        if p_x_intersection >= p[0] - min(a[0], b[0]):
            return True

    return False


# Calc a route from A to X node
def calc_route(final_node):
    actual_node = arr_nodes[my_node()]['node']
    py_graph = convert_graph_to_py_format()

    return find_shortest_path(py_graph, actual_node, final_node)[1:]


# Convert actual data structure to python graph
def convert_graph_to_py_format():
    py_graph = {}

    for node in arr_nodes:
        if node != '':
            py_graph[node['node']] = node['connected_nodes']

    return py_graph


# Return an array of nodes to archive the X node
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def print_all_nodes():
    for node in arr_nodes:
        if node != '':
            print "Node: " + str(node['node'])
            print "Connected: " + str(node['connected_nodes'])
            print "Center: " + str(node['center'])
            print "Edges: " + str(node['edges'])


# function that return an interator in pair
# s -> (s0,s1), (s1,s2), (s2, s3), ...
def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return izip(a, b)
