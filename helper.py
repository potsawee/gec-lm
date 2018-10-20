'''
This script is a collection of classes and data structures for candidate word generator
'''
import re
import pdb

class Generator(object):
    '''
    Main class for word generator
    '''
    def __init__(self):
        agid = AgidHandler()
        agid.read_agid()

class AgidHandler(object):
    '''
    Class to handle AGID
    '''
    def __init__(self, path='/home/alta/imports/agid-2016.01.19'):
        self.entries = {}
        self.path = path
        # print("object created")

    def read_agid(self):
        # main file - infl.txt
        with open(self.path+'/infl.txt', 'r') as file:
            for line in file:
                entry = AgidEntry(line)
                self.entries[entry.word] = entry

class AgidEntry(object):
    '''
    Data Structure to store an entry in the AGID file

    entry.word
    entry.pos
    entry.infl_words

    '''
    def __init__(self, line):
        items = line.strip().split(':')

        self.word = items[0].split()[0]
        self.pos = items[0].split()[1]

        infl_words = []

        for x in items[1].strip().replace(',', '|').split('|'):
            _word = re.sub(r'[\W|0-9]', '', x)
            infl_words.append(_word)

        self.infl_words = infl_words

class Network(object):
    '''
    Data structure to store 'confusion network'
    <s> and </s> are not stored in network

    ### stage-0: <s>
    stage-1: THE
    stage-2: CAT
    stage-3: SIT, SITS, SAT, SITTING
    stage-4: ON, AT, IN
    stage-5: THE
    stage-6: MAT
    ### stage-7: </s>

    '''
    def __init__(self):
        self.network = []

    def addStage(self, words):
        '''
        words = list of candidates
        '''
        self.network.append(words)

    def getNumStages(self):
        return len(self.network)

    def writeEBNF(self, path):
        with open(path, 'w') as file:
            file.write('(\n')
            file.write('\t\\<s\\>\n')

            for stage in self.network:
                # stage == words
                if len(stage) == 1:
                    file.write('\t{}\n'.format(stage[0]))
                else:
                    line = '\t({})\n'.format(' | '.join(stage))
                    file.write(line)

            file.write('\t\\<\\/s\\>\n')
            file.write(')')
