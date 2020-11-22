import networkx as nx
from itertools import permutations
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
    rooms_i = [list(G.nodes)]
    
    def move(index, rooms):
        room = rooms[index]
        # if room satisfies stress requirement
        D = {}
        for i in range(len(rooms)):
            r = rooms[i]
            for n in r:
                D[n] = i
        k = len(rooms)
        if k > 10 or len(rooms[index]) == 1:
            return 0, D, k
        if is_valid_solution(D, G, s, k):
            return calculate_happiness(D, G), D, k
 
        print(index)

        happenis = 0
        maxD = {}
        maxk = 0
        for kick in room:
            newrooms = []
            for room in rooms:
                newrooms.append(room[:])
            # remove person
            newrooms[index].remove(kick)
            # create new room if necessary
            if index == len(rooms) - 1:
                newrooms.append([])
            # add person to new room
            newrooms[index + 1].append(kick)
            # check next room for validity
            if calculate_stress_for_room(newrooms[index], G) <= s/k:
                newpenis, newD, newk, = move(index + 1, newrooms)
            else:
                newpenis, newD, newk, = move(index, newrooms)
            if newpenis > happenis:
                happenis, maxD, maxk = newpenis, newD, newk
        return happenis, maxD, maxk
        
    happiness, D, k = move(0, rooms_i)

    return D, k
    


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
