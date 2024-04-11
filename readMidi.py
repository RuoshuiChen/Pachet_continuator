from mido import MidiFile, Message, MidiFile, MidiTrack
import numpy as np


def readMidi(path):
    mid = MidiFile(path)

    note_on_time = []
    note_off_time = []
    notes = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if not msg.is_meta:
                if msg.type == "note_on":
                    notes.append(msg.note)
                    # print(msg.note)
                    # print(msg.time)
                    note_on_time.append(msg.time)
                if msg.type == "note_off":
                    note_off_time.append(msg.time)
                    # print(msg.note)
                    # print(msg.time)

    note_on_time = np.array(note_on_time)
    note_off_time = np.array(note_off_time)
    duration_list = np.subtract(note_off_time, note_on_time) / 1024

    currCount = 0
    currNotes = []
    training_sequence = []
    for i in range(len(duration_list)):
        # print(notes[i], duration_list[i])
        if duration_list[i] < 0:
            currCount += abs(duration_list[i])
        else:
            currCount += duration_list[i]
            currNotes.append(notes[i])
        if currCount >= 4:
            # print(currNotes)
            if (len(currNotes) <= 3) and len(training_sequence) >= 1:
                training_sequence[-1] += currNotes
            else:
                training_sequence.append(currNotes)
            currCount = 0
            currNotes = []
        elif (i == len(duration_list) - 1) and (currCount < 4):
            training_sequence[-1] += currNotes
            currCount = 0
            currNotes = []

    return training_sequence


def writeMidi(sequence, note_on, note_off):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)


    for i in range(len(sequence)):
        currNote = sequence[i]
        #currDuration = duration_list[i]
        if i >= len(note_on):
            curr_noteOn = note_on[i]
        else:
            curr_noteOn = 0

        if i >= len(note_off):
            curr_noteOff = note_off[i]
        else:
            curr_noteOff = 256
        for j in range(2):
            if j == 0:
                track.append(Message("note_on", note=currNote, velocity=74, time=0))
            else:
                track.append(Message("note_off", note=currNote, velocity=74, time=400))

    mid.save('continuator.mid')


def readInput(path):
    mid = MidiFile(path)
    note_on_time = []
    note_off_time = []
    notes = []
    duration_list = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if not msg.is_meta:
                if msg.type == "note_on":
                    notes.append(msg.note)
                    #duration_list.append(341)
                    note_on_time.append(msg.time)
                elif msg.type == "note_off":
                    note_off_time.append(msg.time)
    #note_on_time = np.array(note_on_time)
    #note_off_time = np.array(note_off_time)
    #duration_list = np.subtract(note_off_time, note_on_time)

    return notes, note_on_time, note_off_time
