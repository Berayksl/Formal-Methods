import networkx as nx
import matplotlib.pyplot as plt


def draw_grid_map(cols, rows,current_state,obstacles,constraint_regions,path,title):
    #this function visulaizes the 2D grid map and highlights the path by adding arrows

    fig, ax = plt.subplots()

    #draw horizontal lines
    for i in range(rows + 1):
        ax.axhline(y=i, color='black', linestyle='-', linewidth=1)

    #draw vertical lines
    for j in range(cols + 1):
        ax.axvline(x=j, color='black', linestyle='-', linewidth=1)
        
    ax.set_aspect('equal') #make the cells square

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    #remove ticks:
    ax.set_xticks([])
    ax.set_yticks([])

    #paint the cells according to the regions:

    for cell in obstacles:
        row, col= cell
        ax.fill_between([row, row + 1], col + 1, col, color='red')

    for cell in constraint_regions:
        row, col= cell
        ax.fill_between([row, row + 1], col + 1, col, color='yellow')

    #ax.fill_between([initial_state[0], initial_state[0] + 1], initial_state[1] + 1, initial_state[1], color='orange')

    circle = plt.Circle((current_state[0][0] + 0.5, current_state[0][1] + 0.5), 0.3, color='purple', fill=True)
    ax.add_patch(circle)
    

    visited = []
    #add arrow signs to the path cells
    for i in range(len(path)-1):
        row1, col1= path[i][0]
        row2, col2 = path[i+1][0]
            
        direction = (row2-row1, col2-col1) #find the direction of the arrow
        if direction == (1,0):
            arrow_text = '→'
        elif direction == (-1,0):
            arrow_text = '←'
        elif direction == (0,1):
            arrow_text = '↑'
        elif direction == (0,-1):
            arrow_text = '↓'
        elif direction == (1, 1):
            arrow_text = '↗'  # Diagonal right and up
        elif direction == (1, -1):
            arrow_text = '↘'  # Diagonal right and down
        elif direction == (-1, 1):
            arrow_text = '↖'  # Diagonal left and up
        elif direction == (-1, -1):
            arrow_text = '↙'  # Diagonal left and down
        else:
            arrow_text = ''

        if 'init' in path[i][1] and path[i][0] not in visited:
            visited.append(path[i][0])
            ax.annotate(arrow_text, xy=(row1 + 0.5, col1 + 0.60), xytext=(0, 0), textcoords='offset points', ha='center', va='center', fontsize=20, color='black')
        elif path[i][0] in visited:
            ax.annotate(arrow_text, xy=(row1 + 0.3, col1 + 0.60), xytext=(0, 0), textcoords='offset points', ha='center', va='center', fontsize=20, color='blue')
        else:
            visited.append(path[i][0])
            ax.annotate(arrow_text, xy=(row1 + 0.5, col1 + 0.60), xytext=(0, 0), textcoords='offset points', ha='center', va='center', fontsize=20, color='blue')

    plt.title(title)
    manager = plt.get_current_fig_manager()
    manager.window.wm_geometry("+600+250") #location of the window (x,y)
    plt.show()
    


#Part-1:
def create_grid_graph(n, m,display):
    G = nx.grid_2d_graph(n, m, create_using=nx.DiGraph) #creates a 2d grid graph with dimensions n x m. each node is connected to the its neighbor nodes, meaning that it only allows up, down, left and right moves

    for node in G.nodes(): #add the self loops at each state
        G.add_edge(node,node)

    #add diagonal neighbor edges (if the action set contains diagonal actions)
    # directions = [(-1,-1),(1,-1),(-1,1),(1,1)]
    # for node in G.nodes():
    #     x, y = node
    #     for direction in directions:
    #         neighbor = (x + direction[0], y + direction[1])
    #         if neighbor in list(G.nodes()):
    #            G.add_edge(node,(x + direction[0], y + direction[1])) 
        
    pos = {(x, y): (x,y) for x, y in G.nodes()}

    #print the adjaceny matrix and draw the graph representation:
    if display:
        print("\nAdjacency Matrix:")
        adjacency_matrix = nx.to_numpy_array(G) #creates the adjacency matrix for the given graph
        print(adjacency_matrix)

        nx.draw(G, pos, with_labels=True, font_weight='bold',arrows = True, node_size=900, node_color='lightblue', font_color='black', font_size=8) 
        plt.title(f'{n} x {m} Grid Graph')
        plt.show()

    return G



#Part-2:
def environment_modifier(G,obstacles,constraint_location,environment_rows,display): #this function modifies the adjacency matrix of a given graph according to the obstacle regions and displays the new graph representation
    #the inputs to this function are lists of the state that are in a given region.
    
    i = 1
    for node in G.nodes():
        G.nodes[node]['label'] = 'r' + str(int(node[0]) + int(node[1]) * environment_rows + 1) #Change Later!!!
        i += 1
    
    #G.nodes[initial_state]['label'] = 'initial'

    pos = {(x, y): (x,y) for x, y in G.nodes()}


    for obstacle in obstacles: #iterate over different obstacle states
        neighbors = list(G.neighbors(obstacle))
        for neighbor in neighbors: #prune the edges between the neighbor nodes and obstacle nodes
            try:
                G.remove_edge(obstacle, neighbor)
                G.remove_edge(neighbor, obstacle)
            except:
                continue

    node_labels = nx.get_node_attributes(G, 'label')
    if display:
        nx.draw(G, pos, with_labels=False, font_weight='bold',arrows = True, node_size=900, node_color='lightblue', font_color='black', font_size=8) #draw the graph representation
        nx.draw_networkx_nodes(G, pos, nodelist=obstacles, node_color='red', node_size=900, label='obstacle') #convert the obstacle nodes to red
        nx.draw_networkx_labels(G, pos, labels=node_labels)

        #designate the regions with specified colors:
        #nx.draw_networkx_nodes(G, pos, nodelist=[initial_state], node_color='orange', node_size=900, label='Initial State')
        #nx.draw_networkx_nodes(G, pos, nodelist=[final_state], node_color='gray', node_size=900, label='Final State')
        #nx.draw_networkx_nodes(G, pos, nodelist=desired_regions, node_color='green', node_size=900)
        nx.draw_networkx_nodes(G, pos, nodelist=constraint_location, node_color='yellow', node_size=900, label='Constraint')
        

        plt.title('Modified Grid Graph')
        plt.show()

#Part-3
def find_shortest_path(G,start, end): 
#this function finds the shortest path between two states in a given region, prints the output word

    shortest_path = nx.shortest_path(G, source=start, target=end, method='dijkstra') #find the shortest path to the final state by using dijkstra's algorithm

    #Print the output word 
    output_word = ''
    for state in shortest_path:
        output_word += T_obs[state] + ','

    return shortest_path, output_word[:-1]

if __name__ == '__main__':

    #environment region locations:
    initial_state = (0,0)
    final_state = (4,3)
    obstacles = [(1,1),(3,2),(3,3)]
    desired_regions = [(2,3), (4,2)]
    chosen_desired_region = (2,3)

    #grid size parameters:
    n = 10
    m = 8

    G = create_grid_graph(n, m, display=True)
    environment_modifier(G, obstacles,desired_regions,initial_state, m, display=True)

    #Part-3, first question:
    print('\nShortest path from the initial state to final state:')
    shortest_path, output_word = find_shortest_path(G,start=initial_state,end=final_state)
    print('Output Word:',output_word)
    draw_grid_map(n,m,obstacles=obstacles,initial_state=initial_state,desired_regions=desired_regions,path=shortest_path)


    #Part-3, second question
    path_to_final,word1 = find_shortest_path(G,start=initial_state,end=final_state)
    path_to_desired,word2 = find_shortest_path(G,start=final_state,end=chosen_desired_region)
    print('\nShortest path from the initial state to the final state and then visits the chosen desired region:')
    output_word = word1[:-2] + word2
    print('Output Word:',output_word)
    shortest_path = path_to_final + path_to_desired
    draw_grid_map(n,m,obstacles=obstacles,initial_state=initial_state,desired_regions=desired_regions,path=shortest_path)

    