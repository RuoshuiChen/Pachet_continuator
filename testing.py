from prefixTree import*
import os
from readMidi import readMidi, writeMidi
import unittest

'''
tree = Trie()
collection = [["A","B","C","D"],["A","B","B","C"],["A","B", "B", "D"]]


tree.parse_seq(["A","B","C","D"], 0)
tree.parse_seq(["A","B","B","C"], 4)
tree.parse_seq(["A","B", "B", "D"], 8)

tree.learn(collection)
Note = tree.search(["A", "B"])
b_child = list(tree.roots.keys())[1].child
b_child_child = list(b_child.keys())[1].child
'''

'''setup stage1: midi file to learning sequence'''
directory = 'midiCmaj/4_4'
learning_sequence = []
for root, dirs, files in os.walk(directory):
    for filename in files:
        #print(os.path.join(root, filename))
        path = os.path.join(root, filename)
        if ".mid" not in path:
            continue
        curr_sequence = readMidi(path)
        #print(curr_sequence)
        learning_sequence += curr_sequence

#print(learning_sequence)

'''setup stage2: csv to learning sequence'''

'''train the model'''
Bach_tree = Trie()
Bach_tree.learn(learning_sequence)
print(learning_sequence)
#print(Bach_tree.roots)

'''generate'''
input_sequence1 = [64, 60, 62, 64, 67, 65, 65, 69, 67, 67, 72, 71]
input_sequence2 = [72, 67, 64, 60, 62, 64, 65, 67, 69, 67, 65, 64]
Bach_tree.generate(input_sequence1)
Bach_tree.generate(input_sequence2)

duration_list = [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512]
#print(Bach_tree.generated)
writeMidi(Bach_tree.generated, duration_list)
