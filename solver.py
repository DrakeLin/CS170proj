import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import copy

# complete search for 10 people
# takes too long for 20 and 50 people
def complete_solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    rooms = []

    max_happiness = -float('inf')
    ret = None
    k = 0

    def create(nodes, mapping):
        nonlocal max_happiness
        nonlocal ret
        nonlocal k
        if nodes == []:
            mm = convert_dictionary(mapping)
            #if mapping not in rooms and is_valid_solution(mm, G, s, len(mapping)):
                #rooms.append(mapping)
            room_k = len(mapping)
            if is_valid_solution(mm, G, s, room_k):
                happiness = calculate_happiness(mm, G)
                if happiness > max_happiness:
                    max_happiness = happiness
                    ret = mm
                    k = room_k
            return
        pp = nodes[0]
        r = 0
        n = copy.deepcopy(nodes)
        n.remove(pp)
        for room in mapping:
            m = copy.deepcopy(mapping)
            m[room] = m[room] + [pp]
            mm = convert_dictionary(m)
            if is_valid_solution(mm, G, s, len(m)):
                create(n, m)
            r += 1
        m = copy.deepcopy(mapping)
        m[r] = [pp]
        create(n, m)

    nodes = list(G.nodes)
    pp = nodes[0]
    n = copy.deepcopy(nodes)
    n.remove(pp)
    mapping = {}
    mapping[0] = [pp]
    create(n, mapping)
    print("done generating everything")

    # max_happiness = -float('inf')
    # ret = None
    # k = 0

    # for room in rooms:
    #     r = convert_dictionary(room)
    #     room_k = len(room)
    #     if is_valid_solution(r, G, s, room_k):
    #         happiness = calculate_happiness(r, G)
    #         if happiness > max_happiness:
    #             max_happiness = happiness
    #             ret = r
    #             k = room_k
    return ret, k


def solve(G, s, swap):
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
                if swap == 0:
                    ret[i] += G.edges[i,j]["happiness"] - G.edges[i,j]["stress"]
                elif swap == 1:
                    ret[i] += G.edges[i,j]["happiness"]
                else:
                    ret[i] -= G.edges[i,j]["stress"]
        return min(ret, key = lambda x: ret[x])


    finished = False
    while not finished:
        finished = True
        for i in range(len(rooms)):
            room = rooms[i]
            if calculate_stress_for_room(room, G) > s / len(rooms):
                move(i)
                finished = False
                break

    D = {}
    for i in range(len(rooms)):
        r = rooms[i]
        for n in r:
            D[n] = i
    k = len(rooms)
    ret = D

    max_happiness = calculate_happiness(ret, G)
    improved = True
    print("before", max_happiness)

    def search_local(depth):
        nonlocal D
        nonlocal k
        nonlocal improved
        nonlocal max_happiness
        nonlocal ret
        if depth == 0:
            return
        for i in D:
            for j in D:
                if i == j:
                    continue
                D[i], D[j] = D[j], D[i]
                kkk = len(set(D.values()))
                if is_valid_solution(D, G, s, kkk):
                    happy = calculate_happiness(D, G)
                    if happy > max_happiness:
                        k = kkk
                        max_happiness = happy
                        ret = {}
                        for key in D:
                            ret[key] = D[key]
                        improved = True
                    search_local(depth - 1)
                D[i], D[j] = D[j], D[i]

                temp, D[i] = D[i], D[j]
                kkk = len(set(D.values()))
                if is_valid_solution(D, G, s, kkk):
                    happy = calculate_happiness(D, G)
                    if happy > max_happiness:
                        k = kkk
                        max_happiness = happy
                        ret = {}
                        for key in D:
                            ret[key] = D[key]
                        improved = True
                    search_local(depth - 1)
                D[i] = temp

    while improved:
        improved = False
        search_local(2)
        D = ret
        # for i in D:
        #     for j in D:
        #         if i == j:
        #             continue
        #         D[i], D[j] = D[j], D[i]
        #         kkk = len(set(D.values()))
        #         if is_valid_solution(D, G, s, kkk):
        #             if calculate_happiness(D, G) > max_happiness:
        #                 max_happiness = calculate_happiness(D, G)
        #                 ret = {}
        #                 for key in D:
        #                     ret[key] = D[key]
        #                 improved = True
        #                 k = kkk
        #         D[i], D[j] = D[j], D[i]

        #         temp, D[i] = D[i], D[j]
        #         kkk = len(set(D.values()))
        #         if is_valid_solution(D, G, s, kkk):
        #             if calculate_happiness(D, G) > max_happiness:
        #                 max_happiness = calculate_happiness(D, G)
        #                 ret = {}
        #                 for key in D:
        #                     ret[key] = D[key]
        #                 improved = True
        #                 k = kkk
        #         D[i] = temp
        # D = ret
    print("after:", max_happiness)
    return ret, k, max_happiness

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    #D, k = complete_solve(G, s)
    # D1, k1, h1 = solve(G, s, 0)
    # D2, k2, h2 = solve(G, s, 1)
    D3, k3, h3 = solve(G, s, 2)
    # assert is_valid_solution(D1, G, s, k1)
    # assert is_valid_solution(D2, G, s, k2)
    assert is_valid_solution(D3, G, s, k3)
    best = max([h1, h2, h3])
    if h1 == best:
        print("h1")
        D = D1
    elif h2 == best:
        print("h2")
        D = D2
    elif h3 == best:
        print("h3")
        D = D3
    D = D3
    print(D)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))


    # for i in range(1, 243):
    #     path = 'inputs/large/large-'
    #     path += str(i)
    #     path += '.in'
    #     try:
    #         test = open(path, 'r')
    #         test.close()
    #     except:
    #         continue
    #     G, s = read_input_file(path)
    #     #D, k = complete_solve(G, s)
    #     D, k = solve(G, s)
    #     assert is_valid_solution(D, G, s, k)
    #     print("Total Happiness: {}".format(calculate_happiness(D, G)))
    #     out_path = 'out/'
    #     out_path += path.split('/')[-2]
    #     out_path += '/'
    #     out_path += path.split('/')[-1]
    #     out_path = out_path.split('.')[0]
    #     out_path += '.out'
    #     write_output_file(D, out_path)


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
