#Example usage of gridmap and automaton_creator scripts

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from gridmap import *
from automaton_creator import *



if __name__ == '__main__':
    constraint_locations = [(0,4),(3,3)]
    obstacles = [(3,5),(4,5)]


    environment_rows = 8
    environment_columns = 8

    transition_system = create_grid_graph(environment_rows, environment_columns, display=False)
    environment_modifier(transition_system,obstacles,constraint_locations, environment_rows, display = True)


    buchi_automaton, initial_buchi_state = buchi_automaton_creator('notAorBuntilCandD.txt')

    product_automaton = create_product_automaton(transition_system, buchi_automaton, initial_buchi_state)


    initial_state = ((7,7),initial_buchi_state)
    final_state = ((0,4), 'accept_all')

    #find the shortest path to one of the accepting states in the product automaton:
    shortest_path = nx.shortest_path(product_automaton, source=initial_state, target=final_state, method='dijkstra')
    draw_grid_map(environment_columns, environment_rows, initial_state, obstacles, constraint_locations, shortest_path, 'shortest path')
    print(shortest_path)