from mido import MidiFile

mid = MidiFile('midiCmaj/4_4/bwv64.2_transposed.mid')

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)