"""To find the coverage of AGID using Language models to rescore
for Grammatical Error Correction
"""

from helper import Generator
from conll2speech import read
import pdb

empty_tok = '!NULL'

class m2_annotation(object):
    def __init__(self, m2line):
        # line e.g. 'A 8 9|||Nn|||diseases|||REQUIRED|||-NONE-|||0'
        columns = m2line.split('|||')
        numbers = columns[0].split()
        self.num1 = int(numbers[1])
        self.num2 = int(numbers[2])
        self.corr = columns[2] if columns[2] != '' else empty_tok
        self.id = columns[-1]


def experiment(path):
    sent_chunks = read(path)

    del_gold = 0 # deletion error proposed by annotator
    sub_gold = 0 # substitution error proposed by annotator
    complex_gold = 0 # insertion / multiple edits error proposed by annotator

    del_covered = 0 # deletion covered
    sub_covered = 0 # substitution covered
    complex_covered = 0 # complex error covered

    generator = Generator()

    for sent_chunk in sent_chunks:
        if len(sent_chunk) <= 1:
            # no annotation for this sentence
            continue

        # handle S
        words = sent_chunk[0].split()[1:]

        # handle A
        annotations = []
        for line in sent_chunk[1:]:
            a = m2_annotation(line)

            # ---- Choose annotator ---- #
            # annotator_id = '1'
            # if a.id != annotator_id:
            #     continue
            # -------------------------- #

            if a.num1 == -1 and a.num2 == -1:
                continue

            annotations.append(a)

        for ann in annotations:
            diff = ann.num2 - ann.num1
            if diff == 1: # substitution
                sub_gold += 1
                word = words[ann.num1]
                found, candidates = generator.find_candidates(word)
                if found:
                    if ann.corr in candidates:
                        sub_covered += 1
                    # else:
                    #     print(' '.join(candidates))
                    #     print(ann.corr)
                    #     pdb.set_trace()
                else:
                    if ann.corr == word:
                        sub_covered += 1


            elif diff == 0: # deletion
                del_gold += 1

            elif diff > 1: # insertion OR multiple edits
                complex_gold += 1
                _words = words[ann.num1:ann.num2]
                cand_list = []
                for w in _words:
                    found, candidates = generator.find_candidates(w)
                    if found:
                        cand_list.append(candidates)
                    else:
                        cand_list.append(w)


                # build a confusion network!
                confusion_set = build_confusion(cand_list)
                if ann.corr in confusion_set:
                    complex_covered += 1

    # ------ end of for ann in annotation ------ #

    print('del_gold = ', del_gold)
    print('sub_gold = ', sub_gold)
    print('complex_gold = ', complex_gold)
    print('del_covered = ', del_covered)
    print('sub_covered = ', sub_covered)
    print('complex_covered = ', complex_covered)
    print('------------------------------------')
    print('substitution coverage = {:.1f}'.format(sub_covered/sub_gold*100))
    print('deletion coverage = {:.1f}'.format((del_covered)/(del_gold)*100))
    print('complex coverage = {:.1f}'.format((complex_covered)/(complex_gold)*100))
    print('total coverage = {:.1f}'.format((sub_covered+del_covered+complex_covered)/(sub_gold+del_gold+complex_gold)*100))


def build_confusion(cand_list):
    timestep = len(cand_list)
    total = 1
    for c in cand_list:
        total *= len(c)
    if total > 1000000:
        print('too long --- confusion size =', total)
        return []

    mylist = cand_list[-1]
    for t in range(timestep-1):
        candidates = cand_list[timestep-t-2]
        _mylist = []
        for word in candidates:
            if word == empty_tok:
                for x in mylist:
                    _mylist.append(x)
            else:
                for x in mylist:
                    y = word + ' ' + x
                    _mylist.append(y)
        mylist = _mylist

    return mylist


def main():
    m2path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.v2.m2'
    experiment(m2path)

def dev():
    t1 = ['the', 'a']
    t2 = ['cat', 'dog', 'cow', empty_tok]
    t3 = ['sit', 'sits', 'sat']
    t4 = ['mat', 'matt', 'maths', 'floor', 'floors']
    cand_list = [t1, t2, t3, t4]

    confusion = build_confusion(cand_list)

    for x in confusion:
        print(x)
    print(len(confusion))

    return

if __name__ == '__main__':
    main()
