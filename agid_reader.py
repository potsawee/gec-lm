import re
import pdb

class AgidReader(object):
    '''
    Class to handle AGID
    '''
    def __init__(self, path='/home/alta/imports/agid-2016.01.19'):
        self.entries = {}
        self.path = path
        print("object created")

    def read_agid(self):
        # main file - infl.txt
        with open(self.path+'/infl.txt', 'r') as file:
            for line in file:
                entry = AgidEntry(line)
                self.entries[entry.word] = entry



class AgidEntry(object):
    '''
    Data Structure to store an entry in the AGID file
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

if __name__ == "__main__":
    print('testing...')
    a = AgidReader()
    a.read_agid()
    # pdb.set_trace()
    print('done')
