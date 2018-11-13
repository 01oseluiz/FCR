#!/usr/bin/env python

import rospy
import data
import graph
import move_logic as move


def listener_talker():
    rospy.init_node('listener_talker', anonymous=True)
    rate = rospy.Rate(100)

    data.initialize()
    graph.initialize()

    while not data.is_data_initialized() or not graph.is_grapho_initialized():
        rate.sleep()

    data.set_params('cord_x', data.abs_position_x)
    data.set_params('cord_y', data.abs_position_y)

    move.new_waypoint()

    while not rospy.is_shutdown():

        if move.move():
            if graph.my_node():
                my_node = graph.my_node()
                my_connected_nodes = graph.arr_nodes[my_node]['connected_nodes']
                print "Estamos no numero: " + str(my_node)
                print "Podemos ir para os numeros: " + str(my_connected_nodes)

                temp_input = ""
                while temp_input not in my_connected_nodes:
                    try:
                        temp_input = int(raw_input("Digite um dos numeros para definir como novo caminho: "))
                    except:
                        print "Input incorreto...\n...Encerrando"
                        exit(-1)

                try:
                    data.set_params('cord_x', graph.arr_nodes[temp_input]['center'][0])
                    data.set_params('cord_y', graph.arr_nodes[temp_input]['center'][1])
                    print "Indo para o ponto " + str(temp_input) + ": " + str([data.params['cord_x'], data.params['cord_y']])
                except:
                    data.set_params('cord_x', data.abs_position_x)
                    data.set_params('cord_y', data.abs_position_y)
                    print "Este no ainda nao foi mapeado!"

            else:
                print "Nao estamos em um no existente...\n...Encerrando"
                exit(-1)

        rate.sleep()


if __name__ == '__main__':
    try:
        listener_talker()
    except rospy.ROSInterruptException:
        pass
