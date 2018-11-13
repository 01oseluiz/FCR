#!/usr/bin/env python

import rospy
import data
import graph
import move_logic as move
import occupational_map as map


# Function that runs once, just in start of execution

def setup():
    data.initialize()
    graph.initialize()

    while not data.is_data_initialized() or not graph.is_grapho_initialized():
        rate.sleep()

    data.set_params('cord_x', data.abs_position_x)
    data.set_params('cord_y', data.abs_position_y)

    move.new_waypoint()


# Function that runs in loop until rospy is turn off
# In this function you can consider that all data are already updated, once the 'setup' makes this action

def main_loop():

    raw_input("Precione qualquer tecla para iniciar a criacao de um mapa de ocupacao: ")

    my_node = graph.my_node()

    if my_node:
        print "Estamos no numero: " + str(my_node)
        print "Iniciando criacao do mapa de ocupacao."

        map.initialize_new_map(graph.arr_nodes[my_node], 0.3)
        map.print_map()
        exit(1)

        points = graph.arr_nodes[my_node]['edges']
        data.params['cord_range'] = 2.5

        for point in points:
            data.params['cord_x'] = point[0]
            data.params['cord_y'] = point[1]

            while not move.move():
                if rospy.is_shutdown():
                    raise rospy.ROSInterruptException

    else:
        print "Este no nao e um no valido\n Por favor mova o robo para um no valido!"

    rate.sleep()


def listener_talker():
    global rate
    rospy.init_node('listener_talker', anonymous=True)
    rate = rospy.Rate(100)

    setup()

    while not rospy.is_shutdown():

        main_loop()


if __name__ == '__main__':
    try:
        listener_talker()
    except rospy.ROSInterruptException:
        print "\nOcorreu uma interrupcao inesperada.\n...Encerrando programa\n"
        pass
