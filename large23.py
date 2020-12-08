import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import copy

path = "inputs/large/large-23.in"
G, s = read_input_file(path)

D = {}
room = 0
for i in range(0, 23):
    if i in D:
        continue
    D[i] = room
    D[i + 25] = room
    room += 1
D[23] = room
D[24] = room
room += 1
D[48] = room
D[49] = room
room += 1
k = len(set(D.values()))
assert is_valid_solution(D, G, s, k)
print("Total Happiness: {}".format(calculate_happiness(D, G)))
output_path = "out/other/large-23.out"
write_output_file(D, output_path)
