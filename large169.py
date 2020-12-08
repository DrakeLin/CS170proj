import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room, convert_dictionary
import sys
import copy

path = "inputs/large/large-169.in"
G, s = read_input_file(path)

D = {}
room = 0
D[0] = room
D[46] = room
room += 1
D[1] = room
D[10] = room
room += 1
D[2] = room
D[44] = room
room += 1
D[3] = room
D[22] = room
room += 1
D[4] = room
D[28] = room
room += 1
D[5] = room
D[14] = room
room += 1
D[6] = room
D[16] = room
room += 1
D[7] = room
D[17] = room
room += 1
D[8] = room
D[37] = room
room += 1
D[9] = room
D[34] = room
room += 1
D[11] = room
D[13] = room
room += 1
D[12] = room
D[47] = room
room += 1
D[15] = room
D[39] = room
room += 1
D[18] = room
D[23] = room
room += 1
D[19] = room
D[43] = room
room += 1
D[20] = room
D[24] = room
room += 1
D[21] = room
D[41] = room
room += 1
D[25] = room
D[31] = room
room += 1
D[26] = room
D[29] = room
room += 1
D[27] = room
D[49] = room
room += 1
D[30] = room
D[48] = room
room += 1
D[32] = room
D[38] = room
room += 1
D[33] = room
D[45] = room
room += 1
D[35] = room
D[36] = room
room += 1
D[40] = room
D[42] = room
room += 1
k = len(set(D.values()))
assert is_valid_solution(D, G, s, k)
print("Total Happiness: {}".format(calculate_happiness(D, G)))
output_path = "out/other/large-169.out"
write_output_file(D, output_path)
