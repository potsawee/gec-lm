import sys
import os
from helper import *

bin_path = '/home/dawna/mgb3/transcription/convert/base/bin/'
def main():

    if len(sys.argv) != 3:
        print("Usage: gec_idealised_ged.py file lattices")
        # file = ged.tsv
        return

    path = sys.argv[1]
    lattices = sys.argv[2]

    tmp = lattices + '/tmp/'

    sentences = read_gedtsv(path)

    word_generator = Generator()

    for i, sentence in enumerate(sentences):
        network = Network()
        for w in sentence:

            if w[-1] == 'i':
                _, candidates = word_generator.find_candidates(w[0])
                network.add_stage(candidates)

            elif w[-1] == 'c':
                network.add_stage([w[0]])

            else:
                raise Exception('error --- label')

        sentence_ebnf_path = tmp + 'sentence' + str(i) + '.ebnf'
        network.write_ebnf(sentence_ebnf_path)

    # EBNF -> SLF (.lat)
    hparse = bin_path + 'HParse'
    for i in range(len(sentences)):
        ebnf = tmp + 'sentence' + str(i) +  '.ebnf'
        lat = lattices + '/sentence' + str(i) + '.lat'
        command = '{} {} {}'.format(hparse, ebnf, lat)
        gzip_command = 'gzip {}'.format(lat)
        os.system(command)
        os.system(gzip_command)
        print('write: ' + lat)

    # Write SCP
    scp = lattices + '/flist.scp'
    make_scp(scp, lattices, len(sentences))

def read_gedtsv(path):
    sentences = []
    with open(path, 'r') as file:
        sentence = []
        for line in file:
            if line == '\n':
                sentences.append(sentence)
                sentence = []
            else:
                items = line.split()
                word = items[0]
                label = items[-1]
                sentence.append((word, label))
    return sentences

if __name__ == "__main__":
    main()
