import data

# ---------- GLOBAL HASH VARIABLE ------------
# arr_nodes[node]:
#   - center
#   - connected_nodes
#   - edges
#   - node

arr_nodes = []


def is_grapho_initialized():
    return arr_nodes > 1


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


def my_node():
    for node in arr_nodes:
        if node != '' and is_inside_of_node([data.abs_position_x, data.abs_position_y], node['edges']):
            return node['node']

    return False


def is_connected_node(n_grapho):
    return n_grapho in arr_nodes[n_grapho]['connected_nodes']


# TODO - Melhorar esta logica
def is_inside_of_node((p_x, p_y), edges):
    points_in_x = map(lambda p: p[0], edges)
    points_in_y = map(lambda p: p[1], edges)
    is_in_x = min(points_in_x) <= p_x <= max(points_in_x)
    is_in_y = min(points_in_y) <= p_y <= max(points_in_y)

    return is_in_x and is_in_y


# Calc a route from A to X node
def calc_route(final_node):
    actual_node = arr_nodes[my_node()]['node']
    py_graph = convert_graph_to_py_format()

    return find_path(py_graph, actual_node, final_node)[1:]


# Convert actual data structure to python graph
def convert_graph_to_py_format():
    py_graph = {}

    for node in arr_nodes:
        if node != '':
            py_graph[node['node']] = node['connected_nodes']

    return py_graph


# Return an array of nodes to archive the X node
def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None


def print_all_nodes():
    for node in arr_nodes:
        if node != '':
            print "Node: " + str(node['node'])
            print "Connected: " + str(node['connected_nodes'])
            print "Center: " + str(node['center'])
            print "Edges: " + str(node['edges'])
