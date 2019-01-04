from __future__ import print_function

import sys
import os
from helper import *
from predict_probs import labeler_predict # a routine to call sequence_labeler

# Global paths -> will be changed so that it reads a config file
tmp = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/tmp/'
model_path = '/home/alta/BLTSpeaking/ged-pm574/clctraining-v3/lib/models/clctraining-v3.nopunc.model'
bin_path = '/home/dawna/mgb3/transcription/convert/base/bin/'
def main():

    if len(sys.argv) != 3:
        print("Usage: experiment.py file lattices")
        return

    path = sys.argv[1]
    lattices = sys.argv[2]

    sentences = []

    with open(path, 'r') as file:
        for line in file:
            sentence = line.split()
            sentences.append(sentence)

    # Write the input file into one line per word format
    tmp1 = tmp + 'tmp1.txt'
    with open(tmp1, 'w') as file:
        for sentence in sentences:
            file.write('</s>\tc\n')
            for word in sentence:
                file.write(word + '\tc\n')
            file.write('</s>\tc\n\n')
    print('write: ' + tmp1)

    sentences_prediction = labeler_predict(model_path, tmp1, c_prob=True)
    word_generator = Generator()
    ged_threshold = 0.9

    gedout = lattices + '/ged_preds.tsv'
    write_probs(sentences_prediction, gedout)

    for i, sentence_prediction in enumerate(sentences_prediction):
        network = Network()
        for w in sentence_prediction:

            if w.c_prob < ged_threshold:
                _, candidates = word_generator.find_candidates(w.word)
                network.add_stage(candidates)

            else:
                network.add_stage([w.word])

        sentence_ebnf_path = tmp + 'sentence' + str(i) + '.ebnf'
        network.write_ebnf(sentence_ebnf_path)

    # EBNF -> SLF (.lat)
    hparse = bin_path + 'HParse'
    # lattice_path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/test/task1/task1_script1.1/decode/lattices/'
    for i in range(len(sentences_prediction)):
        ebnf = tmp + 'sentence' + str(i) +  '.ebnf'
        lat = lattices + '/sentence' + str(i) + '.lat'
        command = '{} {} {}'.format(hparse, ebnf, lat)
        gzip_command = 'gzip {}'.format(lat)
        os.system(command)
        os.system(gzip_command)
        print('write: ' + lat)

    # Write SCP
    scp = lattices + '/flist.scp'
    make_scp(scp, lattices, len(sentences_prediction))


    # ------------------- Rescoring -------------------------- #
    # # Rescore to find 1-best
    # hlrescore = bin_path + 'HLRescore'
    # # n_gram_model = '/home/alta/BLTSpeaking/exp-yw396/lms/LM.grp14/lms/tg_train.lm'
    # # wordlist = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/combined.lst'
    # n_gram_model = '/home/alta/BLTSpeaking/exp-graphemic-kaldi-ar527/lms/google/fg_train.lm'
    # wordlist = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/wlists/one-billion+agaid-v1.uniq.lst'
    #
    # for i in range(len(sentences_prediction)):
    #     slf = tmp + 'sentence' + str(i) + '.slf'
    #     mlf = tmp + 'sentence' + str(i) + '.mlf'
    #     # hlrescore, output, model, wordlist, slf
    #     # command = '{} -T 1 -A -V -D -C /home/alta/BLTSpeaking/ged-pm574/gec-lm/hlrescore.cfg -X slf -i {} -n {} -f {} {}'.format(hlrescore, mlf, n_gram_model, wordlist, slf)
    #     command = '{} -C /home/alta/BLTSpeaking/ged-pm574/gec-lm/hlrescore.cfg -X slf -i {} -n {} -f {} {}'.format(hlrescore, mlf, n_gram_model, wordlist, slf)
    #     os.system(command)
    #     print('decode: ' + mlf)
    #
    # print('-------------------------------------------------------')
    # for i in range(len(sentences_prediction)):
    #     mlf = tmp + 'sentence' + str(i) + '.mlf'
    #     original = ' '.join(sentences[i])
    #     gec_out = ' '.join(mlf_to_sentence(mlf))
    #     print('orig: {}'.format(original))
    #     print('hypo: {}'.format(gec_out))
    #     print('-------------------------------------------------------')
    # ---------------------------------------------------------- #

def write_probs(sentences_prediction, path):
    with open(path, 'w') as file:
        for sentence_prediction in sentences_prediction:
            for w in sentence_prediction:
                file.write('{}\tc:{:.5f}\ti:{:.5f}\n'.format(w.word, w.c_prob, w.i_prob))
            file.write('\n')
    print('write: ' + path)


# def dev1(sentences_prediction, agid):
#     print('-------------------------------------------------------------------------')
#     print("{:20s}  {:s} {}".format('original', 'c_prob:', 'candidates (if any)'))
#     print('-------------------------------------------------------------------------')
#
#
#     for sentence_prediction in sentences_prediction:
#         for this in sentence_prediction: # this = word_prediction object
#             if this.c_prob < 0.5:
#                 if this.word in agid.entries:
#                     candidates = agid.entries[this.word].infl_words
#                     print("{:20s}  {:.4f}: {}".format(this.word, this.c_prob, ', '.join(candidates)))
#                     continue
#                 else:
#                     print("{:20s}  {:.4f}: <no-candidate-found>".format(this.word, this.c_prob))
#                     continue
#             print("{:20s}  {:.4f}".format(this.word, this.c_prob))
#         print('-------------------------------------------------------------------------')



if __name__ == "__main__":
    main()
