import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import copy

path = "inputs/large/large-2.in"
G, s = read_input_file(path)

D = {}
room = 0
for i in range(0, 50, 10):
    if i in D:
        continue
    D[i] = room
    D[i + 4] = room
    D[i + 7] = room
    D[i + 9] = room
    room += 1
    D[i + 1] = room
    D[i + 2] = room
    D[i + 6] = room
    room += 1
    D[i + 3] = room
    D[i + 5] = room
    D[i + 8] = room
    room += 1
k = len(set(D.values()))
assert is_valid_solution(D, G, s, k)
print("Total Happiness: {}".format(calculate_happiness(D, G)))
output_path = "out/other/large-2.out"
write_output_file(D, output_path)
