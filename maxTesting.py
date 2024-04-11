from mido import MidiFile
import numpy as np
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc import osc_server
from typing import List, Any
import argparse
from readMidi import readInput
from prefixTree import*
import os
from readMidi import readMidi, writeMidi

notes = []
duration_list = []
'''
mid = MidiFile("seq_sc.mid")
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)
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

def test(address: str, *osc_arguments: List[Any]) -> None:
    path = "input_sequence.mid"
    notes, note_on, note_off = readInput(path)
    print(notes)
    for i in range(len(notes) % 12):
        if i == len(notes) % 12 - 1:
            index = len(notes) - (len(notes) % 12 * 12)
            curr_sequence = notes[-index - 1:-1]
        else:
            curr_sequence = notes[i*12: i*12+12]
        Bach_tree.generate(curr_sequence)
    writeMidi(Bach_tree.generated, note_on, note_off)
    client.send_message("/max", 1)
    Bach_tree.reset()


parser = argparse.ArgumentParser()
f.add_argument("--portClient", type=int, default=5008, help="The port the OSC server is listening on")
parser.add_argument("--listenClient", type=int, default=7401, help="listening port")
dispatcher = Dispatcher()
dispatcher.map("/*", test)
server = ThreadingOSCUDPServer(("127.0.0.1", 7401), dispatcher)
client = udp_client.SimpleUDPClient("127.0.0.1", 5008)
client.send_message("/max", 1)
server.serve_forever()
