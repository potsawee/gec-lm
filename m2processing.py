import pdb
'''
process .m2 file to .ged.tsv format
'''
def read(path):
    with open(path) as file:
        lines = file.readlines()
    sent_chunks = []
    chunk = []
    for line in lines:
        if line == '\n':
            if chunk != []:
                sent_chunks.append(chunk)
                chunk = []
        else:
            chunk.append(line.strip())

    if chunk != []:
        sent_chunks.append(chunk)

    return sent_chunks

def clean_up_m2(orig, out):
    sent_chunks = read(orig)
    new_chunks = []
    for sent_chunk in sent_chunks:
        new_chunk = []
        # s-line
        tokens = sent_chunk[0].split()[1:]

        # ---- remove '.' e.g. in NICT ---- #
        if len(tokens) == 1:
            if tokens[0] == '.':
                continue
        # --------------------------------- #

        sline = 'S {}'.format(' '.join(tokens).lower())
        sline = sline.strip('.')
        new_chunk.append(sline)
        # a-lines
        for line in sent_chunk[1:]:
            items = line.split('|||')
            corr = items[2].strip('"').lower()
            if corr == '_':
                corr = ''
            try:
                annotator = int(items[5])
            except ValueError:
                annotator = 1
            new_line = '|||'.join([items[0], items[1], corr, items[3], items[4], str(annotator)])
            new_chunk.append(new_line)
        new_chunks.append(new_chunk)

    with open(out, 'w') as file:
        for chunk in new_chunks:
            for line in chunk:
                file.write(line + '\n')
            file.write('\n')

    print('clean_up_m2 finish!')


def write_gec_txt(m2file, gectxtfile):
    sent_chunks = read(m2file)
    with open(gectxtfile, 'w') as file:
        for sent_chunk in sent_chunks:
            # retrieve S-line
            tokens = sent_chunk[0].split()[1:]

            # For the following file which has '.' at the end
            # /home/alta/BLTSpeaking/ged-kmk/dtal/data/GEM4/M2/NODISFL_train.cuedsorted.M2.txt
            # tokens = tokens[:-1]
            file.write(' '.join(tokens).lower() + '\n')
        print('write done!')

def get_gedtsv_chunk(sent_chunk):
    # handle 'S'
    tokens = sent_chunk[0].split()[1:]
    labels = ['c'] * len(tokens)
    l = len(tokens)
    # handle 'A'
    for annotation in sent_chunk[1:]:
        columns = annotation.split('|||')
        items = columns[0].split()
        num1 = int(items[1])
        num2 = int(items[2])

        if num1 < 0:
            continue
        # substitution num1 < num2
        # missing item num1 = num2
        if num1 == num2:
            if num1 == l:
                pass
            else:
                labels[num1] = 'i'
        elif num1+1 == num2:
            labels[num1] = 'i'
        elif num1 < num2:
            diff = num2 - num1
            for i in range(diff):
                if num1+i >= l:
                    pass
                else:
                    labels[num1+i] = 'i'
        else:
            pdb.set_trace()
            print('ERROR')
    return (tokens,labels)


def m2_to_gedtsv():
    # m2path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.v2.m2'
    # gedtsv = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.processed.v2.split.gedtsv'
#     m2path = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/alt/official-2014.combined-withalt.m2'
#     gedtsv = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/conll14st-test-data/exp-pm574/conll.noprocessed.gedtsv'

    m2path = 'lib/dtal-m2/nodisfl_train.clean.m2.txt'
    gedtsv = 'lib/dtal-m2/nodisfl_train.gedtsv'


    sent_chunks = read(m2path)
    gedtsv_chunks = []

    for sent_chunk in sent_chunks:
        gedtsv_chunk = get_gedtsv_chunk(sent_chunk)
        gedtsv_chunks.append(gedtsv_chunk)
    # pdb.set_trace()

    # process the tokens
    words = []
    labels = []
    new_chunks = []
    for chunk in gedtsv_chunks:
        for i in range(len(chunk[0])-1):
            word = chunk[0][i]
            label = chunk[1][i]

            # ------ this is for combine 's -> causes problems for idealised GED ---- #
            # next_word = chunk[0][i+1]
            # next_label = chunk[1][i+1]
            # if next_word == "'s":
            #     words.append(word + next_word)
            #     if label == 'i' or next_label == 'i':
            #         labels.append('i')
            #     else:
            #         labels.append('c')
            # elif word == "'s":
            #     continue
            # else:
            #     words.append(word)
            #     labels.append(label)
            # ----------------------------------------------------------------------- #
            words.append(word)
            labels.append(label)

        # last word
        if len(chunk[0]) > 0 :
            word = chunk[0][-1]
            label = chunk[1][-1]

        if word != "'s":
            words.append(word)
            labels.append(label)

        new_chunks.append((words, labels))
        words = []
        labels = []

    gedtsv_chunks = new_chunks

    # write to the output
    with open(gedtsv, 'w') as file:
        for chunk in gedtsv_chunks:
            file.write('</s>\tNA\tc\n')
            for token, label in zip(chunk[0], chunk[1]):
                file.write('{}\tNA\t{}\n'.format(token, label))
            file.write('</s>\tNA\tc\n')
            file.write('\n')

def main():
    # m2_to_gedtsv()

    # write_gec_txt(m2file='/home/alta/BLTSpeaking/ged-kmk/dtal/data/GEM4/M2/NODISFL_train.cuedsorted.M2.txt',
    #             gectxtfile='/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/dtal-m2/nodisfl_train.gec.txt')

    # clean_up_m2(orig='/home/alta/BLTSpeaking/ged-kmk/dtal/data/GEM4/M2/NODISFL_train.cuedsorted.M2.txt',
    #             out='/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/dtal-m2/nodisfl_train.clean.m2.txt')

    # 26 january 2019 - NICT-JLE
    # clean_up_m2(orig='/home/alta/NICT/M2-map/NODISFL_E_file-int.txt',
    #             out='/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/nict/m2/NODISFL_E_file-int.map.clean.txt')
    write_gec_txt(m2file='/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/nict/m2/NODISFL_E_file.map.clean.txt',
                gectxtfile='/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/nict/gec-input/NODISFL_E_file.map.gec.txt')

if __name__ == '__main__':
    main()
