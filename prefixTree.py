import copy


class Node:
    def __init__(self, note):
        self.child = {}
        self.note = note
        self.level = None

    def __eq__(self, other):
        return self.note == other.note

    def __hash__(self):
        return hash((self.note, self.level))

    def __str__(self):
        return f"note + {self.note} + at level + {self.level}"


def fitness_func(input_sequence, target_notes, S):
    target_set = set(target_notes)
    coefficient = 0
    target_note = None
    for note in target_set:
        count1 = input_sequence.count(note)/len(input_sequence)
        count2 = target_notes.count(note)/len(target_notes)
        if (S*count2 + (1-S)*count1) > coefficient:
            coefficient = S*count2 + (1-S)*count1
            target_note = note
    return target_note


class Trie:
    def __init__(self):
        self.roots = {}
        self.library = []
        self.generated = []

    def parse_seq(self, sequence, start_index): #start index: index of the last element in the last sequence
        root_keys = [key.note for key in self.roots.keys()]
        seq_length = len(sequence)

        #iteration for number of times of parsing
        for i in range(seq_length - 1):
            curr_length = seq_length - i - 2
            curr_seq = sequence[:curr_length]
            curr_node = Node(sequence[curr_length])
            curr_node.level = 0

            if sequence[curr_length] not in root_keys:
                self.roots[curr_node] = [start_index + seq_length - i - 1]
                #print("new root", sequence[curr_length], "with coefficient", (start_index + seq_length - i - 1), "at parsing", i)
            else:
                self.roots[curr_node].append(start_index + seq_length - i - 1)
                #print("old root", sequence[curr_length], "with coefficient", (start_index + seq_length - i - 1), "at parsing", i)
            key_list = list(self.roots.keys())
            note_list = [key.note for key in key_list]
            curr_node = key_list[note_list.index(curr_node.note)]
            #iteration for number of elements
            for j in reversed(range(curr_length)):
                curr_notes = [key.note for key in curr_node.child.keys()]
                new_node = Node(curr_seq[j])
                new_node.level = curr_length-j

                if curr_seq[j] not in curr_notes:
                    curr_node.child[new_node] = [start_index + seq_length - i - 1]
                    #print("new child", curr_seq[j], "with coefficient", (
                                #start_index + seq_length - i - 1), "at index", j)
                else:
                    curr_node.child[new_node].append(start_index + seq_length - i - 1)
                    #print("old child", curr_seq[j], "with coefficient", (
                            #start_index + seq_length - i - 1), "at index", j)
                #print(curr_node.child)
                curr_list = list(curr_node.child.keys())
                curr_notes = [key.note for key in curr_node.child.keys()]
                curr_node = curr_list[curr_notes.index(new_node.note)]


    def learn(self, long_sequence):
        start_index = 0
        for segment in long_sequence:
            self.parse_seq(segment, start_index)
            start_index += len(segment)
            self.library += segment


    def generate(self, input_sequence):
        #hypertuning parameter!
        S = .5

        #if len(self.generated) >= len(input_sequence):
            #window = self.generated[-1 - int(len(input_sequence)):-1]

        generated_sequence = []
        if len(self.generated) == 0:
            generated_sequence.append(input_sequence[0])
            for i in range(1, len(input_sequence)):
                #print("enetered loop")
                #print(generated_sequence)

                ranged_input = input_sequence
                if len(input_sequence) == 12:
                    if 0 <= i < 4:
                        ranged_input = input_sequence[0:4]
                    elif 4 <= i < 8:
                        ranged_input = input_sequence[4:8]
                    elif 8 <= i < 12:
                        ranged_input = input_sequence[8:12]

                target_notes = self.search(generated_sequence)
                count = 1
                while target_notes is None:
                    target_notes = self.search(generated_sequence[count:])
                    count += 1

                target_note = fitness_func(ranged_input, target_notes, S)

                if i >= 2 and target_note == generated_sequence[i-1] and generated_sequence[i - 2]:
                    target_notes = [note for note in target_notes if note != target_note]
                    if not target_notes:
                        target_note = target_note + 2
                    else:
                        target_note = fitness_func(ranged_input, target_notes, S)


                generated_sequence.append(target_note)
        else:
            window = self.generated[-1 - int(len(input_sequence)/2):-1]
            for i in range(len(input_sequence)):

                ranged_input = input_sequence
                if len(input_sequence) == 12:
                    if 0 <= i < 4:
                        ranged_input = input_sequence[0:4]
                    elif 4 <= i < 8:
                        ranged_input = input_sequence[4:8]
                    elif 8 <= i < 12:
                        ranged_input = input_sequence[8:12]

                if i < len(input_sequence)/2:
                    target_notes = self.search(window)

                    count = 1
                    while target_notes is None:
                        target_notes = self.search(window[count:])
                        count += 1

                    target_note = fitness_func(ranged_input, target_notes, S)

                    if (i >= 2 and target_note == generated_sequence[i - 1] and generated_sequence[i - 2])\
                            or (i < 2 and target_note == window[-1] and target_note == window[-2]):
                        target_notes = [note for note in target_notes if note != target_note]
                        if not target_notes:
                            target_note = target_note + 2
                        else:
                            target_note = fitness_func(ranged_input, target_notes, S)


                    window.append(target_note)
                    generated_sequence.append(target_note)

                else:
                    target_notes = self.search(generated_sequence)
                    count = 1
                    while target_notes is None:
                        target_notes = self.search(generated_sequence[count:])
                        count += 1

                    target_note = fitness_func(ranged_input, target_notes, S)

                    if target_note == generated_sequence[i - 1] and generated_sequence[i - 2]:
                        target_notes = [note for note in target_notes if note != target_note]
                        if not target_notes:
                            target_note = target_note + 2
                        else:
                            target_note = fitness_func(ranged_input, target_notes, S)

                    generated_sequence.append(target_note)

        self.generated += generated_sequence

    def reduction_function(self, sequence):
        #Posibility by changing note in a small region
        continuable = False
        target_note = sequence[-1]
        possible_1 = target_note + 1
        possible_2 = target_note - 1
        note_list = [key.note for key in self.roots.keys()]
        if possible_1 in note_list:
            sequence[-1] = possible_1
        else:
            sequence[-1] = possible_2
        return sequence

    def search(self, sequence):
        note_count = []
        currRoot = self.roots
        for i in reversed(range(len(sequence))):
            #print(currRoot)
            currNote = sequence[i]
            #print(i, currNote)
            currKeys_note = [key.note for key in currRoot.keys()]
            if currNote not in currKeys_note:
                #print("None")
                #print(currKeys_note)
                return None

            currNode = list(currRoot.keys())[currKeys_note.index(currNote)]
            if i == len(sequence) - 1:
                note_count = currRoot[currNode]
            else:

                currCount = currRoot[currNode]
                #print(currCount)
                note_count = list(set(note_count).intersection(set(currCount)))
                #print(note_count)
            currRoot = currNode.child

        '''
        maxValue = 0
        targetNote = "C"
        for index in count:
            #deep/shallow copy:
            note_count = []
            currNote = self.library[index]
            currSequence = copy.deepcopy(sequence)
            currSequence.append(currNote)
            for i in reversed(range(len(currSequence))):
                currNote = sequence[i]
                currNode = Node(currNote)
                if i == len(sequence) - 1:
                    count = currRoot[currNode]
                else:
                    curr_NoteCount = currRoot[currNode]
                    count = list(set(count).intersection(set(curr_NoteCount)))
            if len(count) > maxValue:
                maxValue = len(count)
                targetNote = currNote
        return targetNote
        '''

        #so called "Markov", but it is actually counting numbers lol
        target_list = []
        for index in note_count:
            target_list.append(self.library[index])
        #print(note_count)
        return target_list

    def reset(self):
        self.generated = []