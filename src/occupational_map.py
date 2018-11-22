import math
import data
import graph

# --------- Class Variables - OCCUPATIONAL_MAP -------------

node = None  # node of occupational map
x_max_global = None     # max limit of area in x
x_min_global = None     # min limit of area in x
y_max_global = None     # max limit of area in y
y_min_global = None     # min limit of area in y
blocks_number_x = None  # number of blocks in x
blocks_number_y = None  # number of blocks in y
occ_map_mtx = [[]]      # matrix of occupational map -> occ_map_mtx[x_point][y_point]
margin_size = 10        # Margin of map
block_size = None       # Size of the division

# ---------------- END Class Variables --------------------


# Create a new empty occupational map
# Receive the node associated with this new occupational map and the resolutions of the map (his size)
def initialize_new_map(node_param, block_size_param):
    global node, block_size
    global x_max_global, x_min_global, y_max_global, y_min_global
    global blocks_number_x, blocks_number_y
    global occ_map_mtx

    node = node_param
    block_size = block_size_param

    temp_points_in_x = map(lambda p: p[0], node['edges'])
    temp_points_in_y = map(lambda p: p[1], node['edges'])
    x_max_global = max(temp_points_in_x)
    x_min_global = min(temp_points_in_x)
    y_max_global = max(temp_points_in_y)
    y_min_global = min(temp_points_in_y)

    blocks_number_x = int((x_max_global - x_min_global) / block_size)
    blocks_number_y = int((y_max_global - y_min_global) / block_size)

    occ_map_mtx = [[0.0 for y in range(blocks_number_y + 2 * margin_size)] for x in
                   range(blocks_number_x + 2 * margin_size)]


# Print he occupation map in the file with name of the node
def print_map():
    file = open('../assets/text/map_' + str(node['node']) + '.txt', 'w')

    # Header
    file.write("Tamanho: " + str(len(occ_map_mtx)) + "x" + str(len(occ_map_mtx[0])) + "\n")
    file.write("Margem: " + str(margin_size) + "\n")
    file.write("No: " + str(node['node']) + "\n\n")

    for p_y in reversed(range(len(occ_map_mtx[0]))):
        line = ""
        for p_x in range(len(occ_map_mtx)):
            if occ_map_mtx[p_x][p_y] >= 1:
                line += ' ' + u'\u2588'
            elif occ_map_mtx[p_x][p_y] <= -1:
                line += ' ' + " "
            else:
                line += ' ' + "X"

        file.write(line.encode('utf8') + "\n")

    file.close()
    print "Mapa criado com sucesso!"


# Makes one scanning from the current position of robot, and compose the occupational map
def scanner():
    for range_distance in data.hokuyo_ranges:
        ang = ((data.hokuyo_ranges.index(range_distance) * data.hokuyo_ang_inc) - (math.pi * 135 / 180)) + data.yaw
        p_x = ((data.abs_position_x + range_distance * math.cos(ang) - x_min_global) / block_size) + margin_size
        p_y = ((data.abs_position_y + range_distance * math.sin(ang) - y_min_global) / block_size) + margin_size

        if 0 <= p_x <= blocks_number_x and 0 <= p_y <= blocks_number_y:
            occ_map_mtx[int(p_x)][int(p_y)] += 0.25
