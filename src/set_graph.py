#!/usr/bin/env python

#
# Este script tem como objetivo facilitar a captura dos nos do grafo
# uma vez executado o arquivo ira pedir um numero para aquele no em questao
# e seus nos adjacentes
# em seguida deve-se mover o robo nos limites do quadrante,
# voltando a posicao inicial, fechando assim o quadrante do no em questao.
# O no sera salvo no arquivo grafo.txt, mude o nome do diretorio abaixo para salvar em outro local
#

import rospy
import math
import operator
from nav_msgs.msg import Odometry  # To /pose


# ------------------ CallBacks ------------------

def callback_pose(odometry):
    global global_position

    global_position['pos_x'] = odometry.pose.pose.position.x
    global_position['pos_y'] = odometry.pose.pose.position.y

# ------------------ End CallBacks ------------------


# Add to grafo file the new node created
def append_to_file(msg_str):
    file = open('../assets/text/grafo.txt', 'a')

    file.write(msg_str)

    file.close()

    return


# Logic to create and save a new node in the file
def save_new_node(node_number, connected_nodes):
    # p_x and p_y
    first_edge = [0, 0]
    edges = []
    center = [0, 0]
    p_range = 0.5

    first_edge[0] = global_position['pos_x']
    first_edge[1] = global_position['pos_y']

    edges.append([first_edge[0], first_edge[1]])
    print "Ponto x:", edges[-1][0], "y:", edges[-1][1], "Computado"

    # Se tem menos de 3 ou nao esta no ponto de inicio
    while (not (len(edges) > 3 and is_in_range(first_edge, p_range))):

        # Se nao esta parado no  mesmo lugar
        if (not is_in_range(edges[-1], p_range)):
            edges.append([global_position['pos_x'], global_position['pos_y']])
            print "Ponto x:", edges[-1][0], "y:", edges[-1][1], "Computado"

        rate.sleep()

    # Se tem 3 ou mais pontas e esta parado no inicio, calcula ponto medio e salva tudo
    message = str(node_number) + "\t"
    message = message + str(connected_nodes) + "\t"
    message = message + str(calc_middle(edges)) + "\t"
    message = message + str(edges) + "\n"

    append_to_file(message)
    print "No " + str(node_number) + " Salvo!"

    return

# Verify if the given point is in the range
def is_in_range((p_x, p_y), p_range):
    is_in_x = p_x - p_range <= global_position['pos_x'] <= p_x + p_range
    is_in_y = p_y - p_range <= global_position['pos_y'] <= p_y + p_range

    return is_in_x and is_in_y


# Calculates the middle of the node, based on his edges
def calc_middle(arr_points):
    points_in_x = map(lambda p: p[0], arr_points)
    points_in_y = map(lambda p: p[1], arr_points)
    middle_x = (max(points_in_x) + min(points_in_x)) / 2
    middle_y = (max(points_in_y) + min(points_in_y)) / 2

    return [middle_x, middle_y]


def listener():
    global global_position
    global rate

    global_position = {}

    temp_input = ""

    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(1)

    rospy.Subscriber("pose", Odometry, callback_pose)

    # Wait until data is loaded
    while (len(global_position) < 2):
        rate.sleep()

    while not rospy.is_shutdown():
        temp_input = raw_input("Press NUMBER of the new node : ")

        if (temp_input != ''):
            save_new_node(temp_input, map(int, raw_input("Enter connected nodes ex: 7 1 3: ").split(' ')))

        rate.sleep()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
