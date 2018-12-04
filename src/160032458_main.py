#!/usr/bin/env python

import rospy
import data
import graph
import cords_calc as calc
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

    my_node = graph.my_node()
    old_node = my_node
    old_position = (data.abs_position_x,data.abs_position_y)

    if my_node:
        print "Estamos no numero: " + str(my_node)
        final_node = raw_input("Entre com o numero do no final desejado: ")

        nodes = graph.calc_route(int(final_node))

        if not nodes:
            print "Nao ha um rota para este no ou ele ainda nao foi mapeado!\n"
            return

        print "DETALHES DA ROTA: " + str(nodes)

        map.initialize_new_map(graph.arr_nodes[my_node], 0.3)
        map.scanner()

        for node in nodes:
            print "Agora estamos indo para o numero: " + str(node)

            data.params['cord_x'] = graph.arr_nodes[node]['center'][0]
            data.params['cord_y'] = graph.arr_nodes[node]['center'][1]

            while not move.move():
                temp_my_node = graph.my_node()
                if temp_my_node:
                    my_node = temp_my_node

                if calc.distance_between_points(old_position, (data.abs_position_x, data.abs_position_y)) > 0.3:
                    old_position = (data.abs_position_x, data.abs_position_y)
                    map.scanner_once()

                if old_node != my_node:
                    old_node = my_node
                    print "Agora estamos no numero: " + str(old_node)
                    map.scanner_once()
                    map.print_map()
                    map.initialize_new_map(graph.arr_nodes[my_node], 0.3)
                    old_position = (data.abs_position_x, data.abs_position_y)
                    map.scanner_once()

                if rospy.is_shutdown():
                    raise rospy.ROSInterruptException



    else:
        print "Este no nao e um no valido\n Por favor mova o robo para um no valido!\n"

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
