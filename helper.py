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
        agid_path = '/home/alta/imports/agid-2016.01.19/infl.txt'
        self.agid = AgidHandler()
        self.agid.read_infl(agid_path)
        self.prep = Preposition()
        self.artc = Article()

    def find_candidates(self, word):
        if word in self.prep.list:
            return (True, self.prep.list)
        elif word in self.artc.list:
            return (True, self.artc.list)
        else:
            candidates = self.agid.get_candidates(word)
            if len(candidates) == 1:
                return (False, candidates)
            else:
                return (True, candidates)

class Preposition(object):
    def __init__(self):
        self.list = ['ABOUT', 'AT', 'BY', 'FOR', 'FROM', 'IN', 'OF', 'ON', 'TO', 'WITH']

class Article(object):
    def __init__(self):
        self.list = ['A', 'AN', 'THE']

class AgidHandler(object):
    '''
    Class to handle AGID
    '''
    def __init__(self):
        self.groups = {}    # groups[key] = [word1, word2, word3, word4]
        self.word_keys = {} # word_keys[word] = key
        self.current_key = 0

    def read_infl(self, path):
        # main file - infl.txt
        with open(path, 'r') as file:
            for line in file:
                #-------------------------------------#

                # remove explanations
                line = re.sub(r'{[\w\d:]+}', '', line)

                group = []
                items = line.strip().split(':')

                word1 = items[0].split()[0]
                group.append(word1)
                # pos = items[0].split()[1] -> currently not used (POS)

                for x in items[1].strip().replace(',', '|').split('|'):
                    _word = re.sub(r'[\W|0-9]', '', x)
                    group.append(_word)

                #-------------------------------------#

                exist = False
                for word in group:
                    if word in self.word_keys:
                        exist = True
                        existing_key = self.word_keys[word]
                        break
                #-------------------------------------#
                if not exist:
                    self.groups[self.current_key] = group
                    for word in group:
                        self.word_keys[word] = self.current_key
                    self.current_key += 1

                else: # this word group already exists
                    for word in group:
                        if word not in self.groups[existing_key]:
                            self.groups[existing_key].append(word)
                            self.word_keys[word] = existing_key

                #-------------------------------------#

    def get_candidates(self, word):
        if word in self.word_keys:
            key = self.word_keys[word]
            return self.groups[key]

        else: # not in AGID return the orignal word
            return [word]

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

    def add_stage(self, words):
        '''
        words = list of candidates
        '''
        self.network.append(words)

    def get_num_stages(self):
        return len(self.network)

    def write_ebnf(self, path):
        with open(path, 'w') as file:
            file.write('(\n')
            file.write('\t\\<s\\>\n')

            for stage in self.network:
                # stage == words
                if len(stage) == 1:
                    if stage[0] == '</s>':
                        pass
                    else:
                        line = '\t{}\n'.format(stage[0])
                        file.write(line.upper())
                else:
                    line = '\t({})\n'.format(' | '.join(stage))
                    file.write(line.upper())

            file.write('\t\\<\\/s\\>\n')
            file.write(')')
            print('write: ' + path)

class WordPrediction(object):
    def __init__(self):
        self.word = ''
        self.c_prob = None
        self.i_prob = None
    def __init__(self, word, c_prob, i_prob):
        self.word = word
        self.c_prob = c_prob
        self.i_prob = i_prob
    def add(self, word, c_prob, i_prob):
        self.word = word
        self.c_prob = c_prob
        self.i_prob = i_prob


def mlf_to_sentence(mlf):
    '''
    #!MLF!#
    "tmp/sentence5.rec"
    0 0 <s> 0.000000
    0 0 HE -5.737978
    0 0 IS -2.383160
    0 0 PLAY -10.001839
    0 0 TENNIS -11.317693
    0 0 </s> -2.735331
    .
    '''
    with open(mlf, 'r') as file:
        lines = file.readlines()
    words = []
    for line in lines[3:-2]:
        items = line.split()
        word = items[2].lower()
        words.append(word)

    return words
