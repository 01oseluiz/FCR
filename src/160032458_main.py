#!/usr/bin/env python

import rospy
import data
import graph
import coords_calc as calc
import move_logic as move
import occupational_map as map


# Function that runs once, just in start of execution
def setup():
    data.initialize()
    graph.initialize()

    while not data.is_data_initialized() or not graph.is_grapho_initialized():
        rate.sleep()

    data.set_params('coord_x', data.abs_position_x)
    data.set_params('coord_y', data.abs_position_y)

    move.new_waypoint()


# Function that runs in loop until rospy is turn off
# In this function you can consider that all data are already updated, once the 'setup' makes this action
def main_loop():
    print "\n---------------Menu----------------"
    print "1 - Ir ate um no, criando o mapa ocupacional"
    print "2 - Ir ate um ponto, exibindo o mapa ocupacional"
    print "0 - Sair"

    option = raw_input("> ")

    if option == '1':
        walk_and_scan()
    elif option == '2':
        walk_and_show_map()
    elif option == '0':
        exit(0)
    else:
        print 'opcao invalida!'

    rate.sleep()


# Move the robot from actual node to B node, calculating the route, and scanning the nodes,
# creating the occupational map
def walk_and_scan():

    # Get the initial node, and set aux variables
    my_node = graph.my_node()
    old_node = my_node
    old_position = (data.abs_position_x, data.abs_position_y)

    if my_node:
        # Get the final node and the scale to create the occupational maps
        print "Estamos no numero: " + str(my_node)
        final_node = raw_input("Entre com o numero do no final desejado: ")
        scala = float(raw_input("Entre com o tamanho da escala para os mapas ocupacionais: "))

        # Calculate the route to reach the final node
        nodes = graph.calc_route(int(final_node))

        if not nodes:
            print "Nao ha um rota para este no ou ele ainda nao foi mapeado!\n"
            return

        print "DETALHES DA ROTA: " + str(nodes)

        # Initialize the occupational map, to create a new map to my actual node
        map.initialize_new_map(graph.arr_nodes[my_node], scala)
        # Makes the first scanning, looking around and taking samples
        map.scanner()

        # Move the robot for each node until last, that is the final node
        for node in nodes:
            print "Agora estamos indo para o numero: " + str(node)

            # Defines as goal, the center of the actual node to be visited
            data.params['coord_x'] = graph.arr_nodes[node]['center'][0]
            data.params['coord_y'] = graph.arr_nodes[node]['center'][1]

            # Move robot until reach the center of the node
            while not move.move():
                # Verify if the actual node exist, if not keep the last node, because between nodes there are gaps
                temp_my_node = graph.my_node()
                if temp_my_node:
                    my_node = temp_my_node

                # Verify if robot already walked a little, and takes a scanning
                if calc.distance_between_points(old_position, (data.abs_position_x, data.abs_position_y)) > 0.3:
                    old_position = (data.abs_position_x, data.abs_position_y)
                    map.scanner_once()

                # Verify if robot reached another node
                # If yes, print the map, initialize another occupational map and reset the aux variables
                if old_node != my_node:
                    old_node = my_node
                    print "Agora estamos no numero: " + str(old_node)
                    map.scanner_once()
                    map.print_map()
                    map.initialize_new_map(graph.arr_nodes[my_node], 0.3)
                    old_position = (data.abs_position_x, data.abs_position_y)
                    map.scanner_once()

                # Verify if user interrupted the program
                verify_interruption()

        # Makes the last scanner and print the map, for the last node
        map.scanner_once()
        map.print_map()

    else:
        print "Este no nao e um no valido\n Por favor mova o robo para um no valido!\n"


# Move the robot from actual position to final position, received by terminal, calculating the route
# and showing the occupational map and his position inside it for each node on the route
def walk_and_show_map():
    print '\n'

    # Get the initial node, and set aux variables
    my_node = graph.my_node()
    old_node = my_node
    old_position = (data.abs_position_x, data.abs_position_y)

    # Wait until the initial node be valid
    while not my_node:
        print "Este no nao e um no valido\n Por favor mova o robo para um no valido!\n"
        my_node = graph.my_node()
        rate.sleep()

    print "Estamos no numero: " + str(my_node)

    # Try read occupational map for this node
    try:
        map.read_node_map(graph.arr_nodes[my_node])
    except:
        print "Nao foi possivel ler o mapa ocupacional deste no!"
        return

    # Get the coordinates to final point
    coord_x = float(raw_input("Entre com a coordenada X do ponto final = "))
    verify_interruption()
    coord_y = float(raw_input("Entre com a coordenada Y do ponto final = "))
    verify_interruption()
    final_node = graph.node_from_point([coord_x,coord_y])

    # If final node is valid, calculate the route
    if final_node:
        nodes = graph.calc_route(int(final_node))

    # Repeat until the final node and the route be valid
    while not (final_node and (nodes or final_node == my_node)):
        print 'Este ponto nao esta em nenhum no, nao foi mapeado, ou nao possui uma rota!\n'
        coord_x = float(raw_input("Entre com a coordenada X do ponto final = "))
        verify_interruption()
        coord_y = float(raw_input("Entre com a coordenada Y do ponto final = "))
        verify_interruption()
        final_node = graph.node_from_point([coord_x, coord_y])

        if final_node:
            nodes = graph.calc_route(int(final_node))

        verify_interruption()

    print 'Este ponto esta no numero ' + str(final_node)

    print "DETALHES DA ROTA: " + str(nodes)

    # Move the robot for each node until last, that is the final node
    for node in nodes:
        print "Agora estamos indo para o numero: " + str(node)

        # Defines as goal, the center of the actual node to be visited
        data.params['coord_x'] = graph.arr_nodes[node]['center'][0]
        data.params['coord_y'] = graph.arr_nodes[node]['center'][1]

        # Move robot until reach the center of the node
        while not move.move():
            # Verify if the actual node exist, if not keep the last node, because between nodes there are gaps
            temp_my_node = graph.my_node()
            if temp_my_node:
                my_node = temp_my_node

            # Verify if robot already walked a little, and print the actual position of robot in the occupational map
            if calc.distance_between_points(old_position, (data.abs_position_x, data.abs_position_y)) > 0.3:
                old_position = (data.abs_position_x, data.abs_position_y)
                map.print_map_terminal()
                print '\n'

            # Verify if robot reached another node
            # If yes, try read another occupational map and reset the aux variables
            if old_node != my_node:
                old_node = my_node
                print "Agora estamos no numero: " + str(old_node)
                old_position = (data.abs_position_x, data.abs_position_y)

                try:
                    map.read_node_map(graph.arr_nodes[my_node])
                except:
                    print "Nao foi possivel ler o mapa ocupacional deste no!"

            # Verify if user interrupted the program
            verify_interruption()

    # Move robot until reach the final point in the final node
    data.params['coord_x'] = coord_x
    data.params['coord_y'] = coord_y

    while not move.move():
        # Verify if robot already walked a little, and print the actual position of robot in the occupational map
        if calc.distance_between_points(old_position, (data.abs_position_x, data.abs_position_y)) > 0.3:
            old_position = (data.abs_position_x, data.abs_position_y)
            map.print_map_terminal()

        # Move robot until reach the final point in the final node
        verify_interruption()


def verify_interruption():
    if rospy.is_shutdown():
        raise rospy.ROSInterruptException


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
