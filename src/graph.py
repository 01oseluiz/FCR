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


def is_inside_of_node((p_x, p_y), edges):
    points_in_x = map(lambda p: p[0], edges)
    points_in_y = map(lambda p: p[1], edges)
    is_in_x = min(points_in_x) <= p_x <= max(points_in_x)
    is_in_y = min(points_in_y) <= p_y <= max(points_in_y)

    return is_in_x and is_in_y


def print_all_nodes():
    for node in arr_nodes:
        if node != '':
            print "Node: " + str(node['node'])
            print "Connected: " + str(node['connected_nodes'])
            print "Center: " + str(node['center'])
            print "Edges: " + str(node['edges'])
