import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import copy

path = "inputs/large/large-14.in"
G, s = read_input_file(path)

D = {}
D[1] = 0
D[2] = 0
D[6] = 0
D[11] = 1
D[12] = 1
D[16] = 1
room = 2
for i in range(40):
    if i in D:
        continue
    D[i] = room
    D[i + 10] = room
    room += 1
D[41] = room
D[44] = room
room += 1
D[42] = room
D[45] = room
room += 1
D[46] = room
D[43] = room
room += 1
D[49] = room
D[47] = room
room += 1
D[40] = room
D[48] = room
room += 1
k = len(set(D.values()))
assert is_valid_solution(D, G, s, k)
print("Total Happiness: {}".format(calculate_happiness(D, G)))
output_path = "out/other/large-14.out"
write_output_file(D, output_path)
