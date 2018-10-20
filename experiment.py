from __future__ import print_function

import sys
sys.path.insert(0,'/home/alta/BLTSpeaking/ged-pm574/local/sequence-labeler')
from helper import *
from predict_probs import labeler_predict # a routine to call sequence_labeler

# Global paths -> will be changed so that it reads a config file
tmp1 = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/tmp/tmp1.txt'
tmp2 = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/tmp/tmp2.txt'
model_path = '/home/alta/BLTSpeaking/ged-pm574/clctraining-v3/lib/models/clctraining-v3.nopunc.model'

def main():

    if len(sys.argv) != 2:
        print("Usage: experiment.py file")
        return

    path = sys.argv[1]

    sentences = []
    agid = AgidHandler ()
    agid.read_agid()


    with open(path, 'r') as file:
        for line in file:
            sentence = line.split()
            sentences.append(sentence)

    # Write the input file into one line per word format
    with open(tmp1, 'w') as file:
        for sentence in sentences:
            file.write('</s>\tc\n')
            for word in sentence:
                file.write(word + '\tc\n')
            file.write('</s>\tc\n\n')


    # call_sequence_labeller = "./seqlab.sh {} > /dev/null 2>&1".format(tmp1)
    # os.system(call_sequence_labeller)
    sentences_prediction = labeler_predict(model_path, tmp1, c_prob=True)

    print('-------------------------------------------------------------------------')
    print("{:20s}  {:s} {}".format('original', 'c_prob:', 'candidates (if any)'))
    print('-------------------------------------------------------------------------')


    for sentence_prediction in sentences_prediction:
        for this in sentence_prediction: # this = word_prediction object
            if this.c_prob < 0.5:
                if this.word in agid.entries:
                    candidates = agid.entries[this.word].infl_words
                    print("{:20s}  {:.4f}: {}".format(this.word, this.c_prob, ', '.join(candidates)))
                    continue
                else:
                    print("{:20s}  {:.4f}: <no-candidate-found>".format(this.word, this.c_prob))
                    continue
            print("{:20s}  {:.4f}".format(this.word, this.c_prob))
        print('-------------------------------------------------------------------------')






if __name__ == "__main__":
    main()
