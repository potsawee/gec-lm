import random
import sys
import os
sys.path.insert(0,'/home/alta/BLTSpeaking/ged-pm574/gec-lm/scripts/')

import m2processing_adapt

def read_oneline_sent(path):
    with open(path, 'r') as file:
        lines = file.readlines()

    return lines

def split_data(path_m2, path_src, path_tgt, outdir, seed=25):
    sentences_src = read_oneline_sent(path_src)
    sentences_tgt = read_oneline_sent(path_tgt)
    sent_chunks = m2processing_adapt.read(path_m2)

    assert len(sentences_src) == len(sent_chunks), "number of src sentences error"
    assert len(sentences_tgt) == len(sent_chunks), "number of tgt sentences error"

    combined = list(zip(sentences_src, sentences_tgt, sent_chunks))
    random.seed(seed)
    random.shuffle(combined)

    sentences_src[:], sentences_tgt[:], sent_chunks[:] = zip(*combined)

    test_percent = 0.2

    l = len(sent_chunks)
    a = int(l * test_percent)

    for i in range(5):
        outdirx = outdir + 'set' + str(i+1) + '/'

        if not os.path.exists(outdirx):
            os.makedirs(outdirx)

        test_src = sentences_src[a*i:a*(i+1)]
        test_tgt = sentences_tgt[a*i:a*(i+1)]
        test_sent_chunks = sent_chunks[a*i:a*(i+1)]

        train_src = sentences_src[:a*i] + sentences_src[a*(i+1):]
        train_tgt = sentences_tgt[:a*i] + sentences_tgt[a*(i+1):]
        train_sent_chunks = sent_chunks[:a*i] + sent_chunks[a*(i+1):]

        print('--------------------------------')
        print('train_src:', len(train_src))
        print('train_tgt:', len(train_tgt))
        print('train_chunk:', len(train_sent_chunks))
        print('test_src:', len(test_src))
        print('test_tgt:', len(test_tgt))
        print('test_chunk:', len(test_sent_chunks))
        print('--------------------------------')

        out_m2 = outdirx + 'test.m2'
        out_src = outdirx + 'test.gec.src'
        out_tgt = outdirx + 'test.gec.tgt'
        write_output(test_src, test_tgt, test_sent_chunks, out_m2, out_src, out_tgt)

        out_m2 = outdirx + 'train.m2'
        out_src = outdirx + 'train.gec.src'
        out_tgt = outdirx + 'train.gec.tgt'
        write_output(train_src, train_tgt, train_sent_chunks, out_m2, out_src, out_tgt)

def write_output(src, tgt, sent_chunks, out_m2, out_src, out_tgt):
    with open(out_m2, 'w') as file:
        for chunk in sent_chunks:
            for line in chunk:
                file.write(line)
                file.write('\n')
            file.write('\n')
    print('wrote: ', out_m2)

    with open(out_src, 'w') as file:
        for line in src:
            file.write(line)
    print('wrote: ', out_src)

    with open(out_tgt, 'w') as file:
        for line in tgt:
            file.write(line)
    print('wrote: ', out_tgt)

def main():
    path_m2 = 'lib/dtal-m2/nodisfl_train.clean.m2.txt'
    path_src = 'lib/dtal-m2/adapt/nodisfl_train.dot.gec.src'
    path_tgt = 'lib/dtal-m2/adapt/nodisfl_train.dot.gec.tgt'

    outdir = 'lib/adapt-data/dtal/'

    split_data(path_m2, path_src, path_tgt, outdir, seed=25)

if __name__ == '__main__':
    main()
