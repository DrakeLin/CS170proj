import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import copy

path = "inputs/large/large-18.in"
G, s = read_input_file(path)

D = {}
room = 0
for i in range(0, 9):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(9, 15):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(15, 22):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(22, 28):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(28, 30):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(30, 37):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(37, 44):
    if i in D:
        continue
    D[i] = room
room += 1
for i in range(44, 50):
    if i in D:
        continue
    D[i] = room
room += 1
k = len(set(D.values()))
assert is_valid_solution(D, G, s, k)
print("Total Happiness: {}".format(calculate_happiness(D, G)))
output_path = "out/other/large-18.out"
write_output_file(D, output_path)
