import sys
import os
from agid_reader import *


def main():
    path = sys.argv[1]

    sentences = []
    agid = AgidReader()
    agid.read_agid()


    with open(path, 'r') as file:
        for line in file:
            sentence = line.split()
            sentences.append(sentence)

    tmp1 = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/tmp/tmp1.txt'

    with open(tmp1, 'w') as file:
        for sentence in sentences:
            file.write('</s>\tc\n')
            for word in sentence:
                file.write(word + '\tc\n')
            file.write('</s>\tc\n\n')

    call_sequence_labeller = "./seqlab.sh {} > /dev/null 2>&1".format(tmp1)
    os.system(call_sequence_labeller)

    # input('continue? ')

    tmp2 = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/tmp/tmp2.txt'
    prob_sentences = []

    with open(tmp2, 'r') as file:
        prob_sentence = []
        for line in file:
            if line == '\n':
                prob_sentences.append(prob_sentence)
                prob_sentence = []
                continue

            c_prob = float(line.split()[-2].strip('c:'))
            prob_sentence.append(c_prob)


    print('-------------------------------------------------------------------------')
    print("{:20s}  {:s} {}".format('original', 'c_prob:', 'candidates (if any)'))
    print('-------------------------------------------------------------------------')

    for sentence, prob_sentence in zip(sentences, prob_sentences):
        for word, prob in zip(sentence, prob_sentence[1:-1]):
            if prob < 0.5:
                if word in agid.entries:
                    candidates = agid.entries[word].infl_words
                    print("{:20s}  {:.4f}: {}".format(word, prob, ', '.join(candidates)))
                    continue
                else:
                    print("{:20s}  {:.4f}: <no-candidate-found>".format(word, prob))
                    continue
            print("{:20s}  {:.4f}".format(word, prob))
        print('-------------------------------------------------------------------------')




if __name__ == "__main__":
    main()
