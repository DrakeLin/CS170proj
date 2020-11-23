import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room
import sys

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    # TODO: your code here!
    rooms = [list(G.nodes)]

    def move(index):
        room = rooms[index]
        # if room satisfies stress requirement
        if calculate_stress_for_room(room, G) <= s / len(rooms):
            return
 
        # person to be removed
        kick = process(index)
        # remove person
        rooms[index].remove(kick)
        # create new room if necessary
        if index == len(rooms) - 1:
            rooms.append([])
        # add person to new room
        rooms[index + 1].append(kick)
        # check next room for validity
        move(index + 1)
        
         
    def process(index):
        r = rooms[index]
        ret = {}
        for i in r:
            ret[i] = 0
            for j in r:
                if i == j:
                    continue
                ret[i] += G.edges[i,j]["happiness"] - G.edges[i,j]["stress"]
                # ret[i] += G.edges[i,j]["happiness"]
                # ret[i] += -G.edges[i,j]["stress"]
        return min(ret, key = lambda x: ret[x])


    finished = False
    while not finished:
        finished = True
        for i in range(len(rooms)):
            room = rooms[i]
            if calculate_stress_for_room(room, G) > s / len(rooms):
                move(i)
                finished = False

    D = {}
    for i in range(len(rooms)):
        r = rooms[i]
        for n in r:
            D[n] = i
    k = len(rooms)
    ret = D


    max_happiness = calculate_happiness(ret, G)
    print(max_happiness)

    improved = True
    while improved:
        improved = False
        for i in D:
            for j in D:
                if i == j:
                    continue
                D[i], D[j] = D[j], D[i]
                if is_valid_solution(D, G, s, k):
                    if calculate_happiness(D, G) > max_happiness:
                        max_happiness = calculate_happiness(D, G)
                        ret = {}
                        for key in D:
                            ret[key] = D[key]
                        improved = True
                D[i], D[j] = D[j], D[i]

                temp, D[i] = D[i], D[j]
                if is_valid_solution(D, G, s, k):
                    if calculate_happiness(D, G) > max_happiness:
                        max_happiness = calculate_happiness(D, G)
                        ret = {}
                        for key in D:
                            ret[key] = D[key]
                        improved = True
                D[i] = temp
        D = ret
    return ret, k

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
